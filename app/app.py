import helpers.helpers as helpers
import os, logging
import random, string
from traceback import print_exc

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
from pprint import pprint

version_numbers = [str(os.getenv("CI_COMMIT_REF_SLUG")), str(os.getenv("CI_COMMIT_SHORT_SHA"))]
app_version = ":".join(version_numbers)

app = Flask(__name__)
app.config["MONGO_URI"] = str(os.getenv("MONGO_URI"))
mongo = PyMongo(app)

#app.config["SECRET_KEY"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
app.config["SECRET_KEY"] = str(os.getenv("APP_SECRET_KEY"))
csrf = CSRFProtect(app)

geo_api_key = str(os.getenv("GEO_API_KEY"))
maps_api_key = str(os.getenv("MAPS_API_KEY"))
log = logging.getLogger()

# Add prometheus wsgi middleware to route /metrics requests
metrics = PrometheusMetrics(app, group_by="endpoint")


@app.route("/")
def index():
    ip_data = helpers.get_ip_data(request, mongo, geo_api_key)
    return render_template(
        "ip_localizator/index.html",
        # ip_data={k: v for k, v in ip_data.items() if not k.startswith("_")},
        ip_data={k: v for k, v in ip_data.items()},
        maps_api_key=maps_api_key,
    )


@app.route("/ip_stats")
def ip_stats():
    cities_data, cities_layout, browser_data, browser_layout = helpers.visitors_stats(mongo)
    return render_template(
        "ip_localizator/ip_stats.html",
        cities_data=cities_data,
        cities_layout=cities_layout,
        browser_data=browser_data,
        browser_layout=browser_layout,
    )


@app.route("/about")
def about():
    return render_template("ip_localizator/about.html", nodename=os.uname().nodename, app_version=app_version)


@app.route("/login", methods=["POST"])
def login():
    return render_template("ip_localizator/logged-in.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()
