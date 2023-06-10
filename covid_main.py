import pandas as pd
import requests
import zipfile
import os
import numpy as np

def main():

    url = 'https://arcgis.com/sharing/rest/content/items/a8c562ead9c54e13a135b02e0d875ffb/data'

    response = requests.get(url)
    open('./data/zeskrapowane.zip', 'wb').write(response.content)

    with zipfile.ZipFile('./data/zeskrapowane.zip', 'r') as zip_ref:
        zip_ref.extractall('./data/archiwum')

    fullpaths = []
    for root, dirs, files in os.walk('./data/archiwum/'):
        for file in files:
            if file.endswith((".csv")):
                fullpath = os.path.join(root, file)
                fullpaths.append(fullpath)

    dfs = []
    for file in fullpaths:
        df = pd.read_csv(file, encoding='windows-1250', sep=';')
        df = df.iloc[:,df.columns.isin(['wojewodztwo','liczba_przypadkow', 'liczba_na_10_tys_mieszkancow','teryt','liczba_wszystkich_zakazen','liczba_wszystkich_zakazen_na_10_tys_mieszkancow'])]
        df['Date'] = pd.to_datetime(file[16:24])-pd.Timedelta(days=1)
        df.columns = ['region', 'number_of_cases', 'number_of_cases_for_10k','teryt', 'date']
        df['region'] = ['Cały kraj',
            'Dolnośląskie',
            'Kujawsko-pomorskie',
            'Lubelskie',
            'Lubuskie',
            'Łódzkie',
            'Małopolskie',
            'Mazowieckie',
            'Opolskie',
            'Podkarpackie',
            'Podlaskie',
            'Pomorskie',
            'Śląskie',
            'Świętokrzyskie',
            'Warmińsko-mazurskie',
            'Wielkopolskie',
            'Zachodniopomorskie']
        
        df = df.iloc[:,~df.columns.isin(['teryt'])]
        dfs.append(df)


    merged_df = pd.concat(dfs, ignore_index=True)

    merged_df.to_csv('./data/covid.csv')



if __name__ == '__main__':
    main()