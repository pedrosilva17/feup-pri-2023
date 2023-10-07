import wikipediaapi
import requests
import json
import glob
import pandas as pd
import string
import nltk
import contractions
import re
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from textwrap import wrap
import matplotlib.pyplot as plt

def main():
    
    # list all csv files only
    all_files = glob.glob('datasets/*.{}'.format('csv'))
    info_files = glob.glob('info/*.{}'.format('csv'))
    ihme_files = glob.glob('datasets/IHME-*.{}'.format('csv'))

    # if global.csv does not exist, generate it
    if not ('datasets/global.csv' in all_files):
        globaldf = generate_global_csv(ihme_files)
    else:
        print('global.csv already exists\nReading global.csv')
        globaldf = pd.read_csv('datasets/global.csv')
        if not ('info/cause_maxvals.csv' in info_files) and not ('info/country_maxvals.csv' in all_files):
            dataset_description(globaldf)
        else:
            print('cause_maxvals.csv and country_maxvals.csv already exist')

    # if cause_description.csv does not exist, generate it
    if not ('datasets/cause_description.csv' in all_files):
        generate_causes_csv(globaldf)
    else:
        print('cause_description.csv already exists')

    # if countries.csv does not exist, generate it
    if not ('datasets/countries.csv' in all_files):
        generate_countries_csv(globaldf)
    else:
        print('countries.csv already exists')

def generate_global_csv(csv_files):
    print('Generating global.csv')

    globaldf = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)

    numberdf = globaldf.loc[globaldf['metric_id'] == 1]

    # TODO: collapse rows and remove useless columns

    numberdf.to_csv('datasets/global.csv', index=False)

    dataset_description(numberdf)

    print('global.csv generated')
    return numberdf

def generate_causes_csv(globaldf):
    print("Generating cause_description.csv")
    causes = globaldf["cause_name"].unique()
    
    descriptions = []
    wiki = wikipediaapi.Wikipedia('Mozilla/5.0', 'en')
    cause_description = pd.DataFrame(columns=['cause_name', 'description']);
    for cause in causes:
        page = wiki.page(cause)
        if page.exists():
            description = page.summary
            cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
            description = fix_description(description)
            generate_wordcloud(description, cause)
            descriptions += description
    
    generate_wordcloud(descriptions, "global")

    cause_description.to_csv('datasets/cause_description.csv', index=False)

    print("cause_description.csv generated")

def generate_countries_csv(globaldf):
    print("Generating countries.csv")
    countries = globaldf["location_name"].unique()

    countrydf = pd.DataFrame(columns=['country', 'code'])

    for country in countries:
        cca3_r = requests.get(url = f'https://restcountries.com/v3.1/name/{country}')

        if cca3_r.status_code == 200:
            cca3_data = cca3_r.json()
            cca3 = cca3_data[0]['cca3']
        else:
            continue
        
        gjson_r = requests.get(url = f'http://inmagik.github.io/world-countries/countries/{cca3}.geojson')

        if gjson_r.status_code == 200:
            gjson = gjson_r.json()
        else:
            continue
        
        try:
            with open(f'gjsons/{cca3}.geojson', 'x', encoding='utf-8') as f:
                json.dump(gjson, f, ensure_ascii=False, indent=4)
        except FileExistsError:
            print("GEOJSON already exists")

        countrydf = countrydf._append({'country': country, 'code': cca3}, ignore_index=True)
    
    countrydf.to_csv('datasets/countries.csv', index=False)
    print("countries.csv generated")

def fix_description(description):
    cleaned_string = contractions.fix(description).lower().translate(str.maketrans('', '', string.punctuation)).replace('\n', '')
    word_list = re.findall('\w+', cleaned_string)
    
    stopwords = nltk.corpus.stopwords.words('english')
    words = []

    for word in word_list:
        if word not in stopwords:
            words.append(word)

    return words

def generate_wordcloud(description, cause):
    fdist = nltk.FreqDist(word for word in description)
    
    if cause == "global":
        df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
        df_fdist.columns = ['Term', 'Frequency']
        df_fdist = df_fdist.sort_values(by=['frequency'], ascending=False)
        df_fdist.to_csv('datasets/global_word_frequency.csv', index=True)

    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(fdist)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f"wordclouds/{cause.replace('/', '_')}.png", bbox_inches='tight', pad_inches=0)
    plt.close()

def dataset_description(df):
    print(f"Dataset description:\n{df.describe()}")

    print("Generating csv for max values for each cause")
    idx = df.groupby('cause_name')['val'].idxmax()
    cause_maxvals = df.loc[idx]
    cause_maxvals.to_csv('info/cause_maxvals.csv', index=False)

    print("Generating csv for max values for each country")
    idx = df.groupby('location_name')['val'].idxmax()
    country_maxvals = df.loc[idx]
    country_maxvals.to_csv('info/country_maxvals.csv', index=False)

if __name__ == '__main__':
    nltk.download("stopwords")
    nltk.download("punkt")
    main()