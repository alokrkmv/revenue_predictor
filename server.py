'''
Author : 
Date :
'''

#import main Flask class and request object
import ast
import json
import decimal

from flask import Flask, request,Response 
from flask_cors import CORS

from main import predict



#create the Flask app

app = Flask(__name__) 
CORS(app)

@app.route('/health-check')
def health_check():
    return 'Server is Up and running'

@app.route('/predictor',methods=['POST'])
def predictor():
    req_data = request.json
    req_data = ast.literal_eval(req_data)
    resp_data = predict(req_data)
    decimal.getcontext().rounding = decimal.ROUND_DOWN
    c = decimal.Decimal(resp_data)
    resp_data = float(round(c,4))
    resp_data = json.dumps({"res":resp_data})
    resp = Response(resp_data, status=200, mimetype='application/json')
    return resp
    

if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000