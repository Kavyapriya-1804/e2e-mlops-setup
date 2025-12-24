import os
import pandas as pd
from feature_store.feature_store import FeastFeatureStore
from feature_store.exec_feature_store import ExecuteFeatureStore

from create_online_feature import CreateOnlineFeatures
from model_training.house_model import HousePriceModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":
    create_online_feature = CreateOnlineFeatures()

    feature_store_path = os.path.join(str(PROJECT_ROOT) + "/feature_store/feature_repo")
    create_online_feature.set_feature_store(feature_store_path)

    online_datasource_path = os.path.join(str(PROJECT_ROOT) + "/data/house_target.parquet")
    create_online_feature.set_entity_df(online_datasource_path)

    entity_df = create_online_feature.get_entity_df()
    target = entity_df["price"]
    print(target)

    # online_df = create_online_feature.get_online_df()
    online_df = pd.read_csv("data/Housing_processed.csv")
    # online_features = online_df.drop(labels=["house_id"], axis=1)
    online_features = online_df[["bedrooms",  "mainroad", "area"]]
    # online_features.dropna()
    print(online_features)

    model = HousePriceModel()
    model.train_model(features=online_features, target=target)
    print("Model trained\n")
    model.configure_mlflow()
    print("MLflow configured successfully\n")
    model_info = model.register()
    print("Model registered successfully\n")
    print(f"Model URI: {model_info.model_uri}")

