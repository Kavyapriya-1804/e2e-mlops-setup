import bentoml

class BentoModel:
    def __init__(self):
        self.model_name = None

    def import_model(self, name:str, model_uri:str):
        model = bentoml.mlflow.import_model(name, model_uri)
        self.model_name = ":".join([model.tag.name, model.tag.version])
        return self.model_name
    
    def load_model(self, model_name:str=None):
        if model_name is None:
            model_name = self.model_name
        bento_model = bentoml.mlflow.load_model(model_name)
        return bento_model
    
    def get_model(self, model_name:str=None):
        if model_name is None:
            model_name = self.model_name
        bento_model = bentoml.models.get(model_name)
        runner = bento_model.to_runner()
        runner.init_local()
        return runner
    
    def predict(self, bento_model, testdata):
        prediction = bento_model.predict(testdata)
        return prediction
    
if __name__ == "__main__":
    bento_model = BentoModel()
    model_name = bento_model.import_model("house_price_model", "models:/m-f62614b649314420ae86474de8f97c84")
    print(model_name)