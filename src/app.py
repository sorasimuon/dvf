"""
    This service aims to request the DVF API in order to retrieve all housing sales made in France
    Whith this data , any client woul be able to look at housing market done in certain city, streets ...

    """

from flask import Flask, make_response, jsonify, request
import requests
from helper.validate_params import getValidCityParam
from helper.build_URL import buildURL


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def helloWorld():
    return "Hello World !!!"


@app.route('/city', methods=['GET'])
def getCityExtract():
    """get DVF for a specific city

    Returns:
        application/json: List of DVF in the specific city
    """
    # Get the URL to request
    args = getValidCityParam(request.args)
    BASE_URL = "http://api.cquest.org/dvf"
    URL = buildURL(BASE_URL, args)

    # Request the DVF of the city
    response = requests.get(URL)

    return make_response((jsonify(response.json()), 200))


# http: // api.cquest.org/dvf?code_commune = 77268


if __name__ == "__main__":
    app.run(port=9002, debug=True)
