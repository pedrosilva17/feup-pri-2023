# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)


@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = []
    relevant_count = 0

    for idx, doc in enumerate(results):
        print(doc['cause_name'])
        if doc['cause_name'] in relevant:
            relevant_count += 1
            precision_at_k = relevant_count / (idx + 1)
            precision_values.append(precision_at_k)

    if not precision_values:
        return 0.0

    return sum(precision_values)/len(precision_values)

@metric
def p20(results, relevant, n=20):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['cause_name'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

if __name__ == '__main__':
    QUERIES_NAME = [
        "incurable_cancer_smp",
        "incurable_cancer_boost_smp",
        "complex_cond_smp",
        "complex_cond_boost_smp",
    ]

    QUERIES = [
        "http://localhost:8983/solr/causes/select?defType=edismax&indent=true&q.op=OR&q=cancer%20!cure&qf=description%20cause_name&rows=20&useParams=",
        "http://localhost:8983/solr/causes/select?bq=year%3A[2012%20TO%202019]&defType=edismax&indent=true&q.op=OR&q=cancer%20!cure&qf=description%20cause_name%5E20&rows=20&useParams=",
        "http://localhost:8983/solr/causes/select?defType=edismax&df=description&indent=true&q.op=AND&q=val%3A%5B100%20TO%20*%5D%20(fever%20OR%20headache)%20!cancer&qf=description&useParams=&rows=20",
        "http://localhost:8983/solr/causes/select?bq=year%3A%5B2012%20TO%202019%5D&defType=edismax&df=description&indent=true&q.op=AND&q=val%3A%5B100%20TO%20*%5D%20(fever%20OR%20headache)%20!cancer&qf=description&useParams=&rows=20"
    ]

    QRELS = [
        "qrels_cancer.txt",
        "qrels_cancer.txt",
        "qrels_complex.txt",
        "qrels_complex.txt",
    ]

    for i, query in enumerate(QUERIES):
        QRELS_FILE = QRELS[i]
        QUERY_NAME = QUERIES_NAME[i]
        QUERY_URL = query

        # Read qrels to extract relevant documents
        relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
        # Get query results from Solr instance
        results = requests.get(QUERY_URL).json()['response']['docs']


        # Define metrics to be calculated
        evaluation_metrics = {
            'ap': 'Average Precision',
            'p20': 'Precision at 20 (P@20)'
        }

        # Calculate all metrics and export results as LaTeX table
        df = pd.DataFrame([['Metric','Value']] +
            [
                [evaluation_metrics[m], calculate_metric(m, results, relevant)]
                for m in evaluation_metrics
            ]
        )

        with open(f'evaluation/results_{QUERY_NAME}.tex','w') as tf:
            tf.write(df.to_latex())

        # PRECISION-RECALL CURVE
        # Calculate precision and recall values as we move down the ranked list
        precision_values = [
            len([
                doc 
                for doc in results[:idx]
                if doc['cause_name'] in relevant
            ]) / idx 
            for idx, _ in enumerate(results, start=1)
        ]

        recall_values = [
            len([
                doc for doc in results[:idx]
                if doc['cause_name'] in relevant
            ]) / len(relevant)
            for idx, _ in enumerate(results, start=1)
        ]

        print(precision_values, recall_values)

        precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

        # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
        recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
        recall_values = sorted(set(recall_values))

        # Extend matching dict to include these new intermediate steps
        for idx, step in enumerate(recall_values):
            if step not in precision_recall_match:
                if recall_values[idx-1] in precision_recall_match:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
                else:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

        disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
        disp.plot()
        plt.savefig(f'evaluation/precision_recall_{QUERY_NAME}.png', format="png")
