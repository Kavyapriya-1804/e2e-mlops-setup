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
