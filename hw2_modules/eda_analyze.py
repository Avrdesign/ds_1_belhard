import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame


class EdaAnalyze:
    def __init__(self, dataset):
        self.df = dataset

    def head_list(self) -> DataFrame:  # Print datasets headers
        return self.df.head()

    def info(self) -> DataFrame:  # Print datasets info
        return self.df.info()

    def missing_value_report(self) -> DataFrame:  # Print datasets missing values
        report = self.df.isnull().sum()
        return report[report > 0]

    def show_all_distributions(self):    # Print all columns
        for column in self.df.select_dtypes(include="number").columns:
            plt.figure(figsize=(5, 5))
            sns.histplot(data=self.df, x=column, kde=True)
            plt.title(f'Distribution of {column}')
            plt.show()

    def show_select_distributions(self, *col_names):   # Print only select columns
        list_col_names = []
        for n in col_names:
            list_col_names.append(n)
        for column in self.df.select_dtypes(include="number").columns:
            if column not in list_col_names:
                continue
            plt.figure(figsize=(5, 5))
            sns.histplot(data=self.df, x=column, kde=True)
            plt.title(f'Distribution of {column}')
            plt.show()

    def draw_pie_distribution(self, item: str):
        total_items = self.df[item].value_counts()
        total_items.plot(kind="pie", autopct='%11.1f%%')
        plt.title(f' Distribution', fontsize=17)
        plt.ylabel("")
        plt.show()

    def filling_missing_values(self, method='median', column='',  # Fill datasets missing values
                               create_new_data=True, output_csv='output.csv'):
        if column not in self.df.columns:
            raise ValueError(f'Column is not in data')
        df_filled = self.df.copy()
        if method == 'median':
            fill_value = df_filled[column].median()
        elif method == 'mean':
            fill_value = df_filled[column].mean()
        else:
            raise ValueError('Incorrect method. Either median or mean.')
        df_filled[column] = df_filled[column].fillna(fill_value)
        if create_new_data is True:
            df_filled.to_csv(output_csv, index=False)
            print(f"Recovered dataset file saved as: {output_csv}")
        return True
