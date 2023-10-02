import wikipediaapi
import glob
import pandas as pd

def main():
    
    # list all csv files only
    csv_files = glob.glob('datasets/*.{}'.format('csv'))

    if not ('datasets/global.csv' in csv_files):
        causes = generate_global_csv(csv_files)

        wiki = wikipediaapi.Wikipedia('Mozilla/5.0', 'en')
        cause_description = pd.DataFrame(columns=['cause_name', 'description']);
        for cause in causes:
            page = wiki.page(cause)
            cause_description = cause_description._append({'cause_name': cause, 'description': page.summary}, ignore_index=True) 

        cause_description.to_csv('datasets/cause_description.csv', index=False)    
    else:
        print('global.csv already exists')

def generate_global_csv(csv_files):
    print('Generating global.csv')

    globaldf = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)

    # TODO: collapse rows and remove useless columns

    globaldf.to_csv('datasets/global.csv', index=False)

    causes = globaldf["cause_name"].unique()
    causesdf = pd.DataFrame(causes, columns=['cause_name'])
    causesdf.to_csv('datasets/causes.csv', index=False)


    print('global.csv generated')
    return causes

if __name__ == '__main__':
    main()