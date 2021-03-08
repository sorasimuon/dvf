import requests
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta


class City:
    """
    Class City : contains information summary of the city
    - name : name of the city
    - postalCode: postal code of the city
    - insee: INSEE code of the city
    -
    """

    def __init__(self, data) -> None:
        """Constructor

        Args:
            city_name (str): city name
        """
        # Get Basic Information from the result[0]
        self.historical = self.cleanData(data)
        self.name = data["resultats"][0]["commune"]
        self.postalCode = data["resultats"][0]["code_postal"]
        self.inseeCode = data['resultats'][0]["code_commune"]
        self.gps_latitude = data['resultats'][0]["lat"]
        self.gps_longitude = data['resultats'][0]["lon"]
        self.current_avg_price_sq_meter_house = self.computeCurrentAVGPriceSQMeter(
            "Maison")
        self.current_avg_price_sq_meter_apartment = self.computeCurrentAVGPriceSQMeter(
            "Appartement")

    def cleanData(self, data: dict) -> DataFrame:
        """
        Clean the data and keep only valuable data

        Args:
            data (dict): [description]

        Returns:
            float: [description]
        """
        try:
            df = pd.DataFrame(data["resultats"],)
            # Filter only 1 year transactions
            end_date = datetime.today()
            start_date = end_date - timedelta(weeks=260)

            df["date_mutation"] = pd.to_datetime(df["date_mutation"])
            df = df[(df["date_mutation"] >= start_date)
                    & (df["date_mutation"] <= end_date)]
            df["date_mutation"] = df["date_mutation"].dt.strftime("%Y-%m-%d")

            df = df[["surface_relle_bati", "valeur_fonciere",
                     "date_mutation", "type_local"]]
            df = self.computeAVGPriceSQMeter(df)

            # Filter out only Apprtement and Maison type_local
            df = df[df["type_local"].isin(["Appartement", "Maison"])]

            # Filter out data if price_sq_meter > 1.5 * average
            average = df["price_sq_meter"].mean()
            df = df[df["price_sq_meter"] < 1.5 * average]

            # df.to_csv("extract_{}.csv".format(data["resultats"][0]["commune"]))

            #  Round up values
            df["valeur_fonciere"] = round(df["valeur_fonciere"])

            return df
        except Exception as e:
            print(e)

    def computeCurrentAVGPriceSQMeter(self, type_local) -> float:
        """
        Compute the average price sq/meter

        Args:
            type_local (str): type local (eg: "Maison" or "Appartement")

        Returns:
            float: [description]
        """
        # Filter by type_local
        df = self.historical[self.historical['type_local'] == type_local]
        print(df)

        # if dataframe is empty
        if len(df) == 0:
            return 0

        #  Compute the price per sq meter
        result = df["price_sq_meter"].mean()
        print(f"Price avg {type_local} = {result}")
        return result

    @ staticmethod
    def computeAVGPriceSQMeter(data):
        data["price_sq_meter"] = round(data["valeur_fonciere"] /
                                       data['surface_relle_bati'])
        return data
