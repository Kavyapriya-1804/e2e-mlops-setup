import os
import pandas as pd
from datetime import datetime
import argparse

from feature_store.feature_store import FeastFeatureStore
from feature_store.exec_feature_store import ExecuteFeatureStore

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

class CreateOnlineFeatures:
    def __init__(self):
        self._feature_store = None
        self._entity_df = None

    def set_feature_store(self, path: str) -> FeastFeatureStore:
        self._feature_store = FeastFeatureStore(path)

        return self._feature_store
    
    def set_entity_df(self, path: str) -> pd.DataFrame:
        self._entity_df = self._feature_store.get_entity_dataframe(path)

        return self._entity_df
    
    def get_historical_data(self, features) -> pd.DataFrame:
        historical_df = self._feature_store.get_historical_features(self._entity_df, features)

        return historical_df
    
    def get_online_df(self):
        exec_feature_store = ExecuteFeatureStore()

        online_df = (exec_feature_store.get_online_features(
                fstore=self._feature_store,
                entity_df=self._entity_df[["house_id"]]
            )
        )

        return online_df
    
    def materialize(self, incremental: bool, start_date: datetime, end_date: datetime):
        self._feature_store.materialize(
            incremental=incremental,
            start_date=start_date,
            end_date=end_date
        )

    
def parse_datetime(dt_str):
    # Convert to ISO format by replacing space with T
    dt_str = dt_str.replace(' ', 'T')
    # Truncate microseconds to 6 digits if more
    if '.' in dt_str:
        base, frac = dt_str.split('.')
        frac = frac[:9]
        dt_str = f"{base}.{frac}"
    return datetime.fromisoformat(dt_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create online features script")
    parser.add_argument("--increment", action="store_true", help="Enable incremental materialization")
    parser.add_argument("--start_date", type=str, help="Start date for materialization (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="End date for materialization (YYYY-MM-DD)")
    args = parser.parse_args()

    features=[
        "house_features:area",
        "house_features:bedrooms",
        "house_features:mainroad"
    ]

    create_online_feature = CreateOnlineFeatures()

    feature_store_path = os.path.join(str(PROJECT_ROOT) + "/feature_store/feature_repo")
    create_online_feature.set_feature_store(feature_store_path)

    online_datasource_path = os.path.join(str(PROJECT_ROOT) + "/data/house_target.parquet")
    create_online_feature.set_entity_df(online_datasource_path)

    # historical_data = create_online_feature.get_historical_data(features)
    # print("\nHistorical data\n")
    # print(historical_data.head())


    start_date = parse_datetime(args.start_date) if args.start_date else None
    end_date = parse_datetime(args.end_date) if args.end_date else None

    create_online_feature.materialize(
        incremental=args.increment, 
        start_date=start_date, 
        end_date=end_date
    )
    print("Incremental materialization completed for ", start_date, " to ", end_date)
    # python ./create_online_feature.py --start_date "2025-12-24 18:08:04.022307617"  --end_date "2025-12-24 18:08:04.022308000"

    # print(args.increment)
    # print(args.start_date)
    # print(args.end_date)

