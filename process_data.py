from eda.data_ingestor import DataIngestorFactory
from eda.data_inspection import DataInspector, DatatypeInspection, SummaryDataInspection
from eda.missing_values_handling import MissingValueContext, DropMissingValueStrategy, FillMissingValueStrategy
from eda.data_analysis import AnalysisContext, NumericalUnivariateAnalysis, CategoricalUnivariateAnalysis, BivariateHeatmapAnalysis
from eda.data_encoding import DataEncoding

import pandas as pd
import numpy as np


class DataProcessing:
    def __init__(self):
        self.df = None

    def load_data(self, file_path:str) -> pd.DataFrame:
        file_type = file_path[-4:]
        data_ingestor_factory = DataIngestorFactory()
        ingestor = data_ingestor_factory.get_data_ingestor(file_type)
        df = ingestor.ingest(file_path)

        return df
    
    def data_inspection(self, df: pd.DataFrame):
        data_inspector = DataInspector()

        data_inspector.set_strategy(DatatypeInspection())
        data_inspector.inspect(df)

        data_inspector.set_strategy(SummaryDataInspection())
        data_inspector.inspect(df)

    def missing_value_handling(self, df: pd.DataFrame):
        missing_value_handler = MissingValueContext()

        missing_value_handler.set_strategy(DropMissingValueStrategy())
        missing_value_handler.check_missing(df)
        missing_value_handler.execute_handling(df)

        missing_value_handler.set_strategy(FillMissingValueStrategy())
        missing_value_handler.execute_handling(df)

    def data_analysis(self, df: pd.DataFrame):
        data_analysis = AnalysisContext()

        data_analysis.set_strategy(NumericalUnivariateAnalysis())
        data_analysis.execute_analysis(df, "price")

        data_analysis.set_strategy(CategoricalUnivariateAnalysis())
        data_analysis.execute_analysis(df, "guestroom")

        data_analysis.set_strategy(BivariateHeatmapAnalysis())
        int_cols = df.select_dtypes(include=np.number).columns
        data_analysis.execute_analysis(df, int_cols)

    def data_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
        cat_columns = ['furnishingstatus']
        numerical_columns = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']

        encode = DataEncoding()
        bin_df = encode.binary_encoding(df, binary_columns)
        cat_df = encode.categorical_encoding(bin_df, cat_columns)
        num_df = encode.numerical_scaling(cat_df, numerical_columns)

        return num_df




if __name__ == "__main__":
    data_processing = DataProcessing()
    df = data_processing.load_data("/Users/Kavyapriya/AI_Learnings/e2e-mlops-setup/data/Housing.csv")
    print(df.head())
    print("\n====\n")
    
    data_processing.data_inspection(df)
    print("\n====\n")

    data_processing.missing_value_handling(df)
    print("Missing values handled")
    print("\n===\n")

    # data_processing.data_analysis(df)
    # print("Data Analysis completed")
    # print("\n===\n")

    encoded_df = data_processing.data_encoding(df)
    print("Data encoding completed\n")
    print(encoded_df)
    encoded_df.to_csv("data/Housing_processed.csv")
    print("\n===\n")

    