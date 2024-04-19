import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime


class Download:
    """
    Handles the downloading and caching of data from a specified URL.

    Attributes:
        url (str): The URL to fetch data from.
        cache_path (str): Path to the cache file where data is stored.
        timeout (int): Time in seconds to consider the cached data as valid.
    """

    def __init__(self, url, cache_path='cache.csv', timeout=600):
        """
        Initializes the Download class with URL, cache path, and timeout.

        Args:
            url (str): URL from which to download the data.
            cache_path (str, optional): File path for storing the downloaded data. Defaults to 'cache.csv'.
            timeout (int, optional): Timeout in seconds for the cache validity. Defaults to 600.
        """
        self.url = url
        self.cache_path = cache_path
        self.timeout = timeout

    def fetching_data(self):
        """
        Fetches data from the specified URL or cache based on the file's modification time and timeout.

        Returns:
            DataFrame: A pandas DataFrame containing the downloaded or cached data.
        """
        if os.path.exists(self.cache_path):
            file_mod_time = datetime.fromtimestamp(os.stat(self.cache_path).st_mtime)
            current_time = datetime.now()
            if (current_time - file_mod_time).total_seconds() < self.timeout:
                df = pd.read_csv(self.cache_path)
                if 'Timestamp' in df.columns:
                    df['Month'] = pd.to_datetime(df['Timestamp']).dt.month_name()
                    df['Weekday'] = pd.to_datetime(df['Timestamp']).dt.day_name()
                else:
                    print('Warning: Timestamp column not found in the cached data.')
                return df

        # If no valid cache, download the data
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.cache_path, 'wb') as file:
                file.write(response.content)
            df = pd.read_csv(self.cache_path)
            if 'Timestamp' in df.columns:
                df['Month'] = pd.to_datetime(df['Timestamp']).dt.month_name()
                df['Weekday'] = pd.to_datetime(df['Timestamp']).dt.day_name()
            else:
                print('Warning: Timestamp column not found in the cached data.')
            return df
        else:
            print('Failed to download data. LOL')
            return None


class DataAnalyzer:
    """
    Analyzes data from a DataFrame including statistics calculation, visualization, and aggregation.

    Attributes:
        dataframe (DataFrame): The data to analyze.
    """

    def __init__(self, dataframe):
        """
        Initializes the DataAnalyzer with a DataFrame.

        Args:
            dataframe (DataFrame): The DataFrame to analyze.
        """
        self.dataframe = dataframe

    def calculate_statistics(self):
        """
        Calculates and prints statistical data of the DataFrame.
        """
        stats = self.dataframe.describe()

    def visualize_data(self, column_name):
        """
        Visualizes the distribution of the specified column in the DataFrame using a histogram.

        Args:
            column_name (str): Name of the column to visualize.
        """
        if column_name in self.dataframe.columns:
            self.dataframe[column_name].plot(kind='hist', bins=50, log=True)
            plt.title(f'Distribution of {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Frequency')
            plt.show()
        else:
            print(f'Column {column_name} does not exist in the dataframe. MEGALOL')

    def aggregate_data(self):
        """
        Aggregates data by weekday and calculates the sum of 'In' and 'Out' columns, then divides by 1000.

        Returns:
            DataFrame: The aggregated DataFrame.
        """
        aggregated = self.dataframe.groupby('Weekday').agg({'In': 'sum', 'Out': 'sum'}).reset_index()
        aggregated['In'] = aggregated['In'] / 1000
        aggregated['Out'] = aggregated['Out'] / 1000
        return aggregated

    def plot_weekday_averages(self, df_aggregated):
        """
        Plots the aggregated data showing the sum of 'In' and 'Out' per weekday, in thousands.

        Args:
            df_aggregated (DataFrame): The aggregated data to plot.
        """
        df_aggregated['Total'] = df_aggregated['In'] + df_aggregated['Out']
        df_sorted = df_aggregated.sort_values(by='Total', ascending=False)
        df_sorted = df_sorted.drop(columns=['Total'])
        ax = df_sorted.plot(x='Weekday', kind='bar', stacked=True)
        ax.set_title('Summe von Ein- und Aussteiger pro Wochentag (in Tausend)')
        ax.set_xlabel('Wochentag')
        ax.set_ylabel('Anzahl')
        ax.legend(['Einsteiger', 'Aussteiger'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def main():
    """
    Main function to execute the steps: download data, analyze, and visualize.

    It creates an instance of Download to fetch the data from a URL, checks if data was successfully
    fetched, and if so, proceeds with analysis and visualization using the DataAnalyzer class.
    It performs aggregation of data by weekday, visualizes the results, filters for 'In' and 'Out',
    and then calculates statistics and visualizes histograms for these columns.
    """
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_frequenzen_hardbruecke/download/frequenzen_hardbruecke_2024.csv'

    downloader = Download(url)
    df = downloader.fetching_data()

    if df is not None:
        analyzer = DataAnalyzer(df)
        df_aggregated = analyzer.aggregate_data()
        analyzer.plot_weekday_averages(df_aggregated)
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
