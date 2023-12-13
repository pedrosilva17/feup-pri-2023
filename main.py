import wikipediaapi, requests, json, glob, string, nltk, contractions, re, os, random
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from warnings import simplefilter
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from textwrap import wrap

def main():
    
    # list all csv files only
    generated_files = glob.glob('datasets/generated/*.{}'.format('csv'))
    generated_json_files = glob.glob('datasets/generated/*.{}'.format('json'))
    ihme_files = glob.glob('datasets/IHME-*.{}'.format('csv'))
    countries = []
    causes = []

    # if global.csv does not exist, generate it
    if not ('datasets/generated/global.json' in generated_json_files):
        globaldf = generate_global_json(ihme_files)
    else:
        print('global.json already exists\nReading global.json')
        globaldf = pd.read_json('datasets/generated/global.json')
        if not ('datasets/generated/sample.json' in generated_json_files):
                print('Generating sample.json')
                sampledf = globaldf.sample(n=100)
                sampledf.dropna(subset=['description'], inplace=True)
                id_columns = [column for column in sampledf.columns if re.search("^[a-zA-Z]*_id$", column) is not None]
                sampledf.drop(id_columns, axis = 'columns', inplace = True)
                sampledf.to_json('datasets/generated/sample.json', orient="table")
        else:
            print('sample.json already exists')
        dataset_description(globaldf)
    """ commented out for quicker generation
    characterize_dataset(globaldf)
    # if cause_description.csv does not exist, generate it
    if not ('datasets/generated/cause_description.csv' in generated_files):
        causes = generate_causes_csv(globaldf)
    else:
        print('cause_description.csv already exists')

    # if countries.csv does not exist, generate it
    if not ('datasets/generated/countries.csv' in generated_files):
        countries = generate_countries_csv(globaldf)
    else:
        print('countries.csv already exists')

    if (len(countries) != 0) or (len(causes) != 0):
        generate_individual_csvs(globaldf, causes, countries)
    else:
        print('Couldn\'t generate individual csvs')
    """
def generate_global_json(csv_files):
    print('Generating global.json')

    globaldf = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)

    numberdf = globaldf.loc[globaldf['metric_id'] == 1]

    causes = numberdf["cause_name"].unique()
    wiki = wikipediaapi.Wikipedia('Mozilla/5.0')
    cause_description = pd.DataFrame(columns=['cause_name', 'description'])

    for cause in causes:
        page = wiki.page(cause)
        # we have a "direct hit" for this cause
        if page.exists():
            description = page.summary
            cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
        else:
            # directly search wikipedia
            url = 'https://en.wikipedia.org/w/index.php'
            headers = {
                'Accept' : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'User-Agent': 'Mozilla/5.0',
            }
            strip_cause = cause.lower().replace('other ', '')
            parameters = {'search': strip_cause }
            resp = requests.get(url, headers = headers, params = parameters)

            # we may have a "direct hit" from removing "other"
            if re.search("^https://en.wikipedia.org/wiki/" , resp.url):
                page = wiki.page(strip_cause)
                if page.exists():
                    description = page.summary
                    cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
            else:
                # it wasn't a "direct hit", but we already have a valid search string on the first result
                soup = BeautifulSoup(resp.text, 'html.parser')

                search = soup.find_all('div', {"class":'mw-search-result-heading'})
                search = re.sub(r'\([^)]*\)', '', search[0].text)

                page = wiki.page(search)
                if page.exists():
                    description = page.summary
                    cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
    
    countries = numberdf["location_name"].unique()
    countries_cca3 = pd.DataFrame(columns=['location_name', 'cca3'])
    error_countries = {
        "Venezuela (Bolivarian Republic of)": "VEN",
        "Taiwan (Province of China)": "TWN",
        "Iran (Islamic Republic of)": "IRN",
        "Iraq (Republic of)": "IRQ",
        "Ireland (Republic of)": "IRL",   
        "Bolivia (Plurinational State of)": "BOL",
        "Micronesia (Federated States of)": "FSM",
    }

    for country in countries:
        cca3_r = requests.get(url = f'https://restcountries.com/v3.1/name/{country}')

        if country == "China":
            cca3 = "CHN"
            countries_cca3 = countries_cca3._append({'location_name': country, 'cca3': cca3}, ignore_index=True)
        elif cca3_r.status_code == 200:
            cca3_data = cca3_r.json()
            cca3 = cca3_data[0]['cca3']
            countries_cca3 = countries_cca3._append({'location_name': country, 'cca3': cca3}, ignore_index=True)
        else:
            if country in error_countries:
                cca3 = error_countries[country]
                countries_cca3 = countries_cca3._append({'location_name': country, 'cca3': error_countries[country]}, ignore_index=True)
            else:
                print("Couldn't find cca3 for", country)
                continue

        gjson_r = requests.get(url = f'http://inmagik.github.io/world-countries/countries/{cca3}.geojson')

        if gjson_r.status_code == 200:
            print("Found GEOJSON for", cca3, country)
            gjson = gjson_r.json()
        else:
            print("Couldn't find GEOJSON for", cca3, country)
            continue
        
        try:
            with open(f'gjsons/{cca3}.json', 'x', encoding='utf-8') as f:
                json.dump(gjson, f, ensure_ascii=False, indent=4)
        except FileExistsError:
            print("GEOJSON already exists", cca3, country)

    numberdf['cca3'] = numberdf['location_name'].map(countries_cca3.set_index('location_name')['cca3'])
    numberdf['description'] = numberdf['cause_name'].map(cause_description.set_index('cause_name')['description'])

    sampledf = numberdf.sample(n=10000)
    id_columns = [column for column in numberdf.columns if re.search("^[a-zA-Z]*_id$", column) is not None]

    sampledf.drop(id_columns, axis = 'columns', inplace = True)

    numberdf.to_json('datasets/generated/global.json', orient='records')
    sampledf.to_json('datasets/generated/sample.json', orient='records')

    dataset_description(numberdf)

    print('global.json generated')
    return numberdf

def generate_causes_csv(globaldf):
    print("Generating cause_description.csv")
    causes = globaldf["cause_name"].unique()
    
    descriptions = []
    info_causes = []
    wiki = wikipediaapi.Wikipedia('Mozilla/5.0')
    cause_description = pd.DataFrame(columns=['cause_name', 'description']);
    for cause in causes:
        page = wiki.page(cause)
        if page.exists():
            description = page.summary
            cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
            info_causes.append(cause)
            description = fix_description(description)
            generate_graphs(description, cause)
            descriptions += description
        else:
            url = 'https://en.wikipedia.org/w/index.php'
            headers = {
                'Accept' : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'User-Agent': 'Mozilla/5.0',
            }
            strip_cause = cause.lower().replace('other ', '')
            parameters = {'search': strip_cause }
            resp = requests.get(url, headers = headers, params = parameters)

            if re.search("^https://en.wikipedia.org/wiki/" , resp.url):
                page = wiki.page(strip_cause)
                if page.exists():
                    description = page.summary
                    cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
                    info_causes.append(cause)
                    description = fix_description(description)
                    generate_graphs(description, cause)
                    descriptions += description
            else:
                soup = BeautifulSoup(resp.text, 'html.parser')

                search = soup.find_all('div', {"class":'mw-search-result-heading'})
                search = re.sub(r'\([^)]*\)', '', search[0].text)

                page = wiki.page(search)
                if page.exists():
                    description = page.summary
                    cause_description = cause_description._append({'cause_name': cause, 'description': description}, ignore_index=True)
                    info_causes.append(cause)
                    description = fix_description(description)
                    generate_graphs(description, cause)
                    descriptions += description
    
    generate_graphs(descriptions, "global")

    cause_description.to_csv('datasets/generated/cause_description.csv', index=False)

    print("cause_description.csv generated")

    return info_causes

def generate_countries_csv(globaldf):
    print("Generating countries.csv")
    countries = globaldf["location_name"].unique()
    info_countries = []

    all_countrydf = pd.DataFrame(columns=['country', 'code'])

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

        all_countrydf = all_countrydf._append({'country': country, 'code': cca3}, ignore_index=True)

        info_countries.append((country, cca3))

    all_countrydf.to_csv('datasets/generated/countries.csv', index=False)
    print("countries.csv generated")

    return info_countries

def generate_individual_csvs(globaldf, causes, countries):
    for (country, cca3) in countries:
        countrydf = globaldf.loc[globaldf['location_name'] == country]
    
        countrydf.to_csv(f"datasets/generated/countries/{cca3}.csv", index=False)
    
    for year in globaldf['year'].unique():
        yeardf = globaldf.loc[globaldf['year'] == year]
        
        yeardf.to_csv(f"datasets/generated/year/{year}.csv", index=False)

    for cause in causes:
        causedf = globaldf.loc[globaldf['cause_name'] == cause]

        causedf.to_csv(f"datasets/generated/causes/{cause.replace('/', '_')}.csv", index=False)

def fix_description(description):
    cleaned_string = contractions.fix(description).lower().translate(str.maketrans('', '', string.punctuation)).replace('\n', '')
    word_list = re.findall('\w+', cleaned_string)
    
    stopwords = nltk.corpus.stopwords.words('english')
    words = []

    for word in word_list:
        if word not in stopwords:
            words.append(word)

    return words

def generate_graphs(description, cause):
    fdist = nltk.FreqDist(word for word in description)
    
    if cause == "global":
        df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
        df_fdist.columns = ['Frequency']
        df_fdist = df_fdist.sort_values(by=['Frequency'], ascending=False)
        df_fdist.to_csv('datasets/generated/global_word_frequency.csv', index=True)

    generate_bars(fdist, cause)
    generate_wordcloud(fdist, cause)

def color_func(word, font_size, position, orientation, random_state=None,
                **kwargs):
    return f"hsl({random.randint(0, 20)}, 100%, {random.randint(60, 100)}%)"

def generate_wordcloud(fdist, cause):
    wc = WordCloud(width=800, height=400, max_words=20, stopwords=nltk.corpus.stopwords.words('english'), color_func=color_func).generate_from_frequencies(fdist)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f"wordclouds/{cause.replace('/', '_')}.png", bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_bars(fdist, cause):
    series = pd.Series(dict(fdist.most_common(20)))

    fig, ax = plt.subplots(figsize=(10,10))
    plot = sns.barplot(x=series.index, y=series.values, ax=ax, palette="flare", hue=series.index)
    plt.xticks(rotation=30);

    plot.set(xlabel = "Term", ylabel = "Frequency", title = f"Most common terms for {cause.lower()}")
    plot.figure.savefig(f"graphs/{cause.replace('/', '_')}.png", bbox_inches='tight', pad_inches=0)
    plt.close()

def dataset_description(df):
    f = open("datasets/generated/dataset_description.txt", "w")
    f.write(str(df.describe()))
    f.write("\n\n")
    for column in df.columns:
        f.write(f"{column}:\n")
        f.write(str(df[column].describe()))
        f.write("\n")
        f.write(f"# unique entries {column}: {str(len(df[column].unique()))}")
        f.write("\n\n")
    f.write("\n\n")
    f.write(f"{df['cause_name'].unique()}")

    f.close()

    idx = df.groupby('cause_name')['val'].idxmax()
    cause_maxvals = df.loc[idx]
    cause_maxvals.to_csv('datasets/generated/cause_maxvals.csv', index=False)

    idx = df.groupby('location_name')['val'].idxmax()
    country_maxvals = df.loc[idx]
    country_maxvals.to_csv('datasets/generated/country_maxvals.csv', index=False)

    idx = df.groupby('year')['val'].idxmax()
    year_maxvals = df.loc[idx]
    year_maxvals.to_csv('datasets/generated/year_maxvals.csv', index=False)

    year_maxvals['val'] = year_maxvals['val'].astype(int)
    plot = sns.barplot(x='year', y='val', data=year_maxvals)
    plt.xticks(rotation=30);

    plot.set(xlabel = "Year", ylabel = "Deaths", title = f"Number of deaths by year")
    plot.figure.savefig(f"datasets/generated/deaths_year.png", bbox_inches='tight', pad_inches=0)
    plt.close()
    
def characterize_dataset(df):
    top_mortality_ranking(df)
    return

def top_mortality_ranking(df):
    df = df.loc[df['year'] == 2019]
    pd.options.display.float_format = '{:.2f}'.format
    df = df[['cause_name', 'val', 'upper', 'lower']].groupby(['cause_name']).sum()
    ranking = df.nlargest(10, 'val')
    ranking.to_csv(f'datasets/generated/top_10_deadliest_diseases.csv')
    
    
if __name__ == '__main__':
    nltk.download("stopwords")
    nltk.download("punkt")
    simplefilter(action = 'ignore', category = FutureWarning)
    main()