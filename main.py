from helpers.convertor import convertor
from PredictionModel import predictor
def predict(req_dict):
    data_dict = convertor(req_dict)
    return predictor(data_dict)