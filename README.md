# E2E-MLOps-setup

DagsHub URL: https://dagshub.com/kavyajg1804/e2e-mlops-setup

## Initial DVC Setup
```bash
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
```

## MLOps Facets
1. **Data Preprocessing**
   - Data Ingestion
   - Data Inspection
   - Missing Values Handling
   - Data Analysis
   - Data Encoding

2. **Feature Store**
   - Source Data Features Creation
     - Entity (define File source for Entity)
     - FeatureView
     - Fields
   - Stores: Offline (training data), Online (low-latency inference), Registry DB (metadata from definitions.py)

3. **Model Training**
   - Choose Algorithm (Classification/Regression/Clustering)
   - Hyperparameter Tuning (e.g., GridSearchCV)
   - Train Model
   - Test Model
   - Record Metrics
   - Configure MLflow for Experiments (Artifacts, Logs, etc.)
   - Register Best Model
   - Get Model URI (e.g., models:/m-f62614b649314420ae86474de8f97c84)

4. **Model Serving**
   - Write Service Logic
   - Load Model (creates BentoML model, e.g., house_price_model:6bzww2xbmcqla2si)
   - Serve Model (http://localhost:3000)
   - Build Server
   - Containerize Server

5. **Model Monitoring**
   - Create Workspace → Project → Report → Dashboards
   - View UI: `evidently ui --workspace "House Price Monitoring Workspace"`

6. **CI/CD**
   - Define Workflow in `.github/workflows/*.yml`
   - Optional: Branch Protection Rules for PR Validation

## Useful Code Snippets
### Reload Classes in Notebook
```python
import importlib
import model.house_model
importlib.reload(model.house_model)
```

### Reconnect Paths in Notebook
```python
import sys
from pathlib import Path
import os

PROJECT_ROOT = Path().resolve().parents[1]
print(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))
```

## Tips
- To export env in terminal: `export $(cat .env)`

## BentoML Commands
- Deploy to BentoCloud: `bentoml deploy house_service:5hsejhxbm2ine2si -n ${DEPLOYMENT_NAME}`
- Update Deployment: `bentoml deployment update --bento house_service:5hsejhxbm2ine2si ${DEPLOYMENT_NAME}`
- Containerize: `bentoml containerize house_service:5hsejhxbm2ine2si`
- Push to BentoCloud: `bentoml push house_service:5hsejhxbm2ine2si` 
