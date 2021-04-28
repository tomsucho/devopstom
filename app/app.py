import helpers.helpers as helpers
import os, logging
import random, string
from traceback import print_exc

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
from IPy import IP
from datetime import datetime
from pprint import pprint

version_numbers = [str(os.getenv("CI_COMMIT_REF_SLUG")), str(os.getenv("CI_COMMIT_SHORT_SHA"))]
app_version = ":".join(version_numbers)

app = Flask(__name__)
app.config["MONGO_URI"] = str(os.getenv("MONGO_URI"))
mongo = PyMongo(app)

app.config["SECRET_KEY"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
csrf = CSRFProtect(app)

geo_api_key = str(os.getenv("GEO_API_KEY"))
maps_api_key = str(os.getenv("MAPS_API_KEY"))
log = logging.getLogger()

# Add prometheus wsgi middleware to route /metrics requests
metrics = PrometheusMetrics(app, group_by="endpoint")


@app.route("/")
# @metrics.counter('requests_count_by_ip', 'Request counts by client IP',
#                    labels={'CustomerIP': lambda: request.headers.getlist("X-Real-IP")[0]})
def home():
    ip_data = dict(
        request={"request_time": datetime.now(), "request_user_agent": str(request.headers.getlist("User-Agent")[0])}
    )
    try:
        if IP(request.headers.getlist("X-Real-IP")[0]).iptype() == "PUBLIC":
            client_ip_addr = request.headers.getlist("X-Real-IP")[0]
            ip_geo_data = helpers.get_ip_location(client_ip_addr, geo_api_key)
            ip_data["ip_geo_data"] = ip_geo_data
            mongo.db.ips.insert_one({**ip_data["request"], **ip_data["ip_geo_data"]})
        else:
            ip_data["ip_geo_data"] = {"ip": "local"}
    except Exception as e:
        log.error(f"Exception has occured: {e}")
        ip_data["ip_geo_data"] = {"ip": "local"}
    return render_template(
        "ip_localizator/index.html",
        ip_data={k: v for k, v in ip_data.items() if not k.startswith("_")},
        maps_api_key=maps_api_key,
    )


@app.route("/ip_stats")
def ip_stats():
    data, layout = helpers.visitors_stats(mongo)
    return render_template("ip_localizator/ip_stats.html", data=data, layout=layout)

@app.route("/about")
def about():
    return render_template("ip_localizator/about.html", nodename=os.uname().nodename, app_version=app_version)

@app.route("/login", methods = ['POST'])
def login():
    return render_template("ip_localizator/logged-in.html")

if __name__ == "__main__":
    app.run()
