# e2e-mlops-setup

STEPS:
## dvc new initial setup
dvc init
dvc remote add origin https://dagshub.com/kavyajg1804/e2e-mlops-setup.dvc
dvc remote default origin
dvc add data
dvc remote modify origin --local auth basic
dvc remote modify origin --local user "kavyajg1804"
dvc remote modify origin --local password "YOUR_TOKEN"
git add .
git commit -m "data-versioning-setup-completed"
git push -u origin main


<!-- to reload classes in ipynb -->
import importlib
import model.house_model
importlib.reload(model.house_model)

<!-- to reconnect paths in ipynb -->
import sys
from pathlib import Path
import os

PROJECT_ROOT = Path().resolve().parents[1]
print(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

## TIPS:
1. to export env in terminal => export $(cat .env)

## FACETS:
1. Data Pre processing
    1. Data Ingestion
    2. Data Inspection
    3. Missing values handled
    4. Data Analysis
    5. Data Encoding
2. Feature Store
    1. Source data features creation
        1. Entity (also define File source for Entity)
        2. FeatureView
        3. Fields
    2. we got offline store(training data), online store(low latency inferencing), registry db (meta data from definitions.py)

