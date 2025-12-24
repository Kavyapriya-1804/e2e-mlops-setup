import pandas as pd
from abc import ABC, abstractmethod

# Strategy design pattern
class DataInspection(ABC):
    def inspect(self, df: pd.DataFrame): 
        pass


class DatatypeInspection(DataInspection):
    def inspect(self, df: pd.DataFrame):
        print("Datatypes and non null columns : ")
        print(df.info())

    
class SummaryDataInspection(DataInspection):
    def inspect(self, df: pd.DataFrame):
        print("Summary for numerical variables : ")
        print(df.describe().transpose())

        print("Summary for categorical variables : ")
        print(df.describe(include=["O"]).transpose())


class DataInspector:
    # def __init__(self, strategy: DataInspection):
    #     self._strategy = strategy

    def set_strategy(self, strategy: DataInspection):
        self._strategy = strategy

    def inspect(self, df: pd.DataFrame):
        self._strategy.inspect(df)

