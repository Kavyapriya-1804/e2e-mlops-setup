import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

# Abstract base class for analysis strategies
class AnalsisStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame, feature: str):
        pass
                      

# Concrete strategies
class NumericalUnivariateAnalysis(AnalsisStrategy):
    def analyze(self, df: pd.DataFrame, feature: str):
        plt.figure(figsize=(10, 6))
        sns.histplot(df[feature], bins=10 , kde=True)
        # plt.show()
        path = os.path.join(os.path.dirname(__file__), f'../data/plots/{feature}_histogram.png')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)

class CategoricalUnivariateAnalysis(AnalsisStrategy):
    def analyze(self, df: pd.DataFrame, feature: str):
        plt.figure(figsize=(10, 6))
        sns.catplot(x=df[feature], kind="count")
        # plt.show()
        path = os.path.join(os.path.dirname(__file__), f'../data/plots/{feature}_countplot.png')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)

class BivariateHeatmapAnalysis(AnalsisStrategy):
    def analyze(self, df: pd.DataFrame, feature: str):
        sns.heatmap(df[feature].corr(), annot=True)
        path = os.path.join(os.path.dirname(__file__), f'../data/plots/correlation_heatmap.png')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)


# Context class
class AnalysisContext:
    # def __init__(self, strategy: AnalsisStrategy):
    #     self._strategy = strategy

    def set_strategy(self, strategy: AnalsisStrategy):
        self._strategy = strategy

    def execute_analysis(self, df: pd.DataFrame, feature: str):
        self._strategy.analyze(df, feature)
        