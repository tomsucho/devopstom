import string
from flask_pymongo import PyMongo
import requests
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import logging
from typing import Type
from IPy import IP
from datetime import datetime
from user_agents import parse

from requests.sessions import Request

log = logging.getLogger()


def get_ip_location(ip_address, geo_api_key):
    send_url = "http://api.ipstack.com/{}?access_key={}"
    try:
        req = requests.get(send_url.format(ip_address, geo_api_key), timeout=2)
        if req.ok:
            ip_geo_spec = req.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request to Geocoder has failed! MSG: {e}")
        ip_geo_spec = dict(ERROR="API Request to Geocoder has failed!")

    return ip_geo_spec


def get_ip_data(request: Type[Request], mongo: PyMongo, geo_api_key: string):
    ip_data = dict(
        request={"request_time": datetime.now(), "request_user_agent": str(request.headers.getlist("User-Agent")[0])}
    )
    if "X-Real-IP" in request.headers and IP(request.headers.getlist("X-Real-IP")[0]).iptype() == "PUBLIC":
        try:
            client_ip_addr = request.headers.getlist("X-Real-IP")[0]
            ip_geo_data = get_ip_location(client_ip_addr, geo_api_key)
            ip_data["ip_geo_data"] = ip_geo_data
            mongo.db.ips.insert_one({**ip_data["request"], **ip_data["ip_geo_data"]})
        except Exception as e:
            log.error(f"Exception has occured: {e}")
            ip_data["ip_geo_data"] = {"IP": "local"}
    else:
        ip_data["ip_geo_data"] = {"IP": "local"}
    return ip_data


def visitors_stats(mongo):
    cities_data, browser_data = [], []
    cities_layout, browser_layout = {}, {}
    try:
        df = pd.DataFrame(mongo.db.ips.find({}, {"_id": 0, "request_user_agent": 1, "country_name": 1, "city": 1}))
    except Exception as e:
        logging.error(f"Fetching data from MongoDB has failed! MSG: {e}", e)
    else:
        if not df.empty:
            grouped_cities = (
                df.groupby(["country_name", "city"])
                .size()
                .sort_values(ascending=False)
                .reset_index(name="count")
                .groupby("city")
            )

            top_countries = list(
                df.groupby(["country_name"])
                .size()
                .sort_values(ascending=False)
                .reset_index(name="count")
                .head(30).country_name
            )

            filter_top = grouped_cities.head()['country_name'].isin(top_countries)
            grouped_cities = grouped_cities.head()[filter_top].groupby('city')

            cities_data = [
                go.Bar(dict(x=values["country_name"], y=values["count"], name=key)) for key, values in grouped_cities
            ]
            cities_layout = dict(
                title="Visitors by Country & City (Top30)",
                plot_bgcolor="peachpuff",
                paper_bgcolor="peachpuff",
                barmode="stack",
            )

            df["browser_family"] = df["request_user_agent"].apply(lambda x: parse(x).browser.family)
            browser_groupping = df.groupby("browser_family").size().sort_values().reset_index(name="count")
            browser_data = [
                dict(
                    type="pie",
                    values=[val for val in browser_groupping["count"]],
                    labels=[key for key in browser_groupping["browser_family"]],
                )
            ]
            browser_layout = dict(title="Visitors by Browser Type", paper_bgcolor="peachpuff")

    return (
        json.dumps(cities_data, cls=plotly.utils.PlotlyJSONEncoder),
        cities_layout,
        browser_data,
        browser_layout,
    )
