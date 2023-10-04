import wikipediaapi
import requests
import json
import glob
import pandas as pd

def main():
    
    # list all csv files only
    csv_files = glob.glob('datasets/*.{}'.format('csv'))

    # if global.csv does not exist, generate it
    if not ('datasets/global.csv' in csv_files):
        globaldf = generate_global_csv(csv_files)
    else:
        print('global.csv already exists\nReading global.csv')
        globaldf = pd.read_csv('datasets/global.csv')

    # if cause_description.csv does not exist, generate it
    if not ('datasets/cause_description.csv' in csv_files):
        generate_causes_csv(globaldf)
    else:
        print('cause_description.csv already exists')

    # if countries.csv does not exist, generate it
    if not ('datasets/countries.csv' in csv_files):
        generate_countries_csv(globaldf)
    else:
        print('countries.csv already exists')

def generate_global_csv(csv_files):
    print('Generating global.csv')

    globaldf = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)

    # TODO: collapse rows and remove useless columns

    globaldf.to_csv('datasets/global.csv', index=False)

    print('global.csv generated')
    return globaldf

def generate_causes_csv(globaldf):
    print("Generating cause_description.csv")
    causes = globaldf["cause_name"].unique()
    # causesdf = pd.DataFrame(causes, columns=['cause_name'])
    # causesdf.to_csv('datasets/causes.csv', index=False)

    wiki = wikipediaapi.Wikipedia('Mozilla/5.0', 'en')
    cause_description = pd.DataFrame(columns=['cause_name', 'description']);
    for cause in causes:
        page = wiki.page(cause)
        cause_description = cause_description._append({'cause_name': cause, 'description': page.summary}, ignore_index=True) 

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



if __name__ == '__main__':
    main()