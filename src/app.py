"""
    This service aims to request the DVF API in order to retrieve all housing sales made in France
    Whith this data , any client woul be able to look at housing market done in certain city, streets ...

    """

from flask import Flask, make_response, jsonify, request
import requests
from helper.validate_params import getValidCityParam
from helper.build_URL import buildURL
from model.city import City


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def helloWorld():
    return "You are requesting the DVF service - entitled for providing historical housing transactions in France"


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
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            # Create City
            if data["nb_resultats"] > 0:
                city = City(data)

                result = {"current_avg_price_sq_meter_house": city.current_avg_price_sq_meter_house,
                          "current_avg_price_sq_meter_apartment": city.current_avg_price_sq_meter_apartment,
                          "city_name": city.name,
                          "city_postalCode": city.postalCode,
                          "city_inseeCode": city.inseeCode,
                          "city_latitude": city.gps_latitude,
                          "city_longitude": city.gps_longitude
                          }

                # return make_response(city.historical.to_json(orient="records"), 200)
                return make_response(jsonify(result), 200)
        else:
            raise Exception("Recherche introuvable")
    except Exception as e:
        return make_response("Error occured", 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
