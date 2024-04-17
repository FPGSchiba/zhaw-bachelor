import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime


class Download:
    def __init__(self, url, cache_path='cache.csv', timeout=600):
        self.url = url
        self.cache_path = cache_path
        self.timeout = timeout

    def fetching_data(self):
        # Check if cached file exists and is within the timeout interval
        if os.path.exists(self.cache_path):
            file_mod_time = datetime.fromtimestamp(os.stat(self.cache_path).st_mtime)
            current_time = datetime.now()
            if (current_time - file_mod_time).total_seconds() < self.timeout:
                print('Loading data from cache. HRHR')
                df = pd.read_csv(self.cache_path)
                df['Month'] = pd.to_datetime(df['Timestamp']).dt.month_name()
                df['Weekday'] = pd.to_datetime(df['Timestamp']).dt.day_name()
                print(df.head())
                return pd.read_csv(self.cache_path)

        # If no valid cache, download the data
        print('Downloading data. ROFL')
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.cache_path, 'wb') as file:
                file.write(response.content)
            df = pd.read_csv(self.cache_path)
            df['Month'] = pd.to_datetime(df['Timestamp']).dt.month_name()
            df['Weekday'] = pd.to_datetime(df['Timestamp']).dt.day_name()
            print(df.head())
            return pd.read_csv(self.cache_path)
        else:
            print('Failed to download data. LOL')
            return None


class DataAnalyzer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def calculate_statistics(self):
        # Calculate and print basic statistics (mean, variance, etc.) for both columns
        stats = self.dataframe.describe()
        print(stats)

    def visualize_data(self, column_name):
        # Check if the column exists in the dataframe
        if column_name in self.dataframe.columns:
            # Visualize the distribution of values in the specified column
            self.dataframe[column_name].plot(kind='hist', bins=50, log=True)
            plt.title(f'Distribution of {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Frequency')
            plt.show()
        else:
            print(f'Column {column_name} does not exist in the dataframe. MEGALOL')


def main():
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_frequenzen_hardbruecke/download/frequenzen_hardbruecke_2024.csv'

    downloader = Download(url)
    df = downloader.fetching_data()

    if df is not None:
        # Filter for "Einsteiger" and "Aussteiger"
        df_filtered = df.iloc[:, :2]
        df_filtered.columns = ['In', 'Out']

        analyzer = DataAnalyzer(df_filtered)
        analyzer.calculate_statistics()
        analyzer.visualize_data('In')
        analyzer.visualize_data('Out')
    else:
        print('LOL, Failed to load data.')


if __name__ == '__main__':
    main()
