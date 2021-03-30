"""
    This service aims to request the DVF API in order to retrieve all housing sales made in France
    Whith this data , any client woul be able to look at housing market done in certain city, streets ...

    """

from flask import Flask, make_response, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import requests
from helper.validate_params import getValidCityParam
from helper.build_URL import buildURL
from model.city import City
from typing import List, Dict


app = Flask(__name__)

### Swagger specific ###
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API DVF (Demande de valeur Fonciere)"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### End Swagger specifics ###

BASE_URL = "http://api.cquest.org/dvf"

# Routes
def getCityExtract(arguments) -> List:
    """Return GET response to DVF external API
    """

    try:
        args = getValidCityParam(arguments)

        if not isinstance(args,str):
            URL = buildURL(BASE_URL , args)
        else:
            raise Exception(args)
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()

            if data["nb_resultats"] > 0:
                return data
            else:
                return "No result Found"
        else:
            raise Exception (f"Error {response.status_code}")

    except Exception as e:
        # print("".join(e.args))
        return make_response("".join(e.args), 400)


@app.route('/', methods=['GET', 'POST'])
def helloWorld():
    return "You are requesting the DVF service - entitled for providing historical housing transactions in France"


@app.route('/city/summary', methods=['GET'])
def getCitySummary():
    """Return a summary of information regarding a city (avg price per sq meter, admin infor of the city)

    Raises:
        Exception: "Error occured"

    Returns:
        Dict: key-value pairs of information
    """

    # Get raw data from DVF API
    data = getCityExtract(request.args)

    # Compute summary data
    if isinstance(data, Dict):
        city = City(data)

        result = {"current_avg_price_sq_meter_house": city.current_avg_price_sq_meter_house,
            "current_avg_price_sq_meter_apartment": city.current_avg_price_sq_meter_apartment,
            "city_name": city.name,
            "city_postalCode": city.postalCode,
            "city_inseeCode": city.inseeCode,
            "city_latitude": city.gps_latitude,
            "city_longitude": city.gps_longitude
            }
        
        return make_response(jsonify(result), 200)
    else:
        return make_response(data, 404)  # No result Found


@app.route("/city/history", methods=['GET'])
def getCityHistory() -> List:
    """Return the list of historical housing data of a specific city

    Returns:
        List: list of historical housing sales
    """

    # Get raw data from DVF API
    data = getCityExtract(request.args)

    # Compute 






if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
