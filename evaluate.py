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
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['cause_name'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

if __name__ == '__main__':
    QUERIES_NAME = [
        "cancer_lump",
        "china_cancer"
    ]

    QUERIES = [
        "http://localhost:8983/solr/causes/query?q=description:%22cancer%22%20description:%22lump%22&q.op=AND&indent=true&useParams=",
        "http://localhost:8983/solr/causes/query?q=location_name:%22China%22%20description:%22cancer%22&q.op=AND&indent=true&sort=val%20desc&useParams=",
    ]

    QRELS = [
        "qrels_cancer.txt",
        "qrels_cancer.txt"
    ]

    for idx, query in enumerate(QUERIES):
        QRELS_FILE = QRELS[idx]
        QUERY_NAME = QUERIES_NAME[idx]
        QUERY_URL = query

        # Read qrels to extract relevant documents
        relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
        # Get query results from Solr instance
        results = requests.get(QUERY_URL).json()['response']['docs']


        # Define metrics to be calculated
        evaluation_metrics = {
            'ap': 'Average Precision',
            'p10': 'Precision at 10 (P@10)'
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
