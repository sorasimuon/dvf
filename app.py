from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
import json
import pandas as pd
import logging

# Create App
app = Flask(__name__)

# Middlewares
CORS(app)
api = Api(app)

@app.route('/', methods=['GET'])
def helloWorld():
    return make_response(jsonify({"data": "Hello World"}), 200)


@app.route("/city", methods=["GET"])
def getCityInfo():
    '''
        Get information regarding a city
    '''


    args ={}
    for k, v in request.args.items():
        args[k] = v
    print (args)

    df = pd.read_csv("./data/laposte_hexasmal.csv",delimiter=";")

    # print(type(df["Nom_commune"]))
    if request.args['insee']:
        result = {'result':df[df["Code_commune_INSEE"] == request.args['insee']].to_dict()}
    elif request.args['name']:
        result = {'result':df[df["Nom_commune"] == request.args['name']].to_dict()}
    else:
        return make_response("Error: Missing or incorrect parameters", 200)

    return make_response(result, 200)


# Run server
if __name__ == "__main__":

    app.run(port=9002, debug=True)


