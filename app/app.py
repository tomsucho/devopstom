import helpers.helpers as helpers
import os
import logging
from traceback import print_exc

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
from IPy import IP
from datetime import datetime
from pprint import pprint

app = Flask(__name__)
app.config['MONGO_URI'] = str(os.getenv('MONGO_URI'))
mongo = PyMongo(app)
geo_api_key = str(os.getenv('GEO_API_KEY'))
log = logging.getLogger()
# Add prometheus wsgi middleware to route /metrics requests
metrics = PrometheusMetrics(app, group_by='endpoint')

@app.route("/")
@metrics.counter('requests_count_by_ip', 'Request counts by client IP',
                   labels={'CustomerIP': lambda: request.headers.getlist("X-Real-IP")[0]})
def home():
    ip_data = dict(request={
        "request_time": datetime.now(),
        "request_user_agent": str(request.headers.getlist("User-Agent")[0])
    })
    try:
        if IP(request.headers.getlist("X-Real-IP")[0]).iptype() == 'PUBLIC':
            client_ip_addr = request.headers.getlist("X-Real-IP")[0]
            ip_geo_data = helpers.get_ip_location(client_ip_addr, geo_api_key)
            ip_data['ip_geo_data'] = ip_geo_data
            # pprint(ip_data)
            mongo.db.ips.insert_one({
                **ip_data["request"],
                **ip_data["ip_geo_data"]
            })
        else:
            ip_data['ip_geo_data'] = {"ip": "local"}
    except Exception as e:       
        print_exc()
        ip_data['ip_geo_data'] = {"ip": "local"}
    return render_template('ip_localizator/index.html', ip_data={k: v for k, v in ip_data.items() if not k.startswith("_")})


@app.route("/ip_stats")
def ip_stats():
    cities_data, cities_layout = helpers.visitors_by_city(mongo)
    countries_data, countries_layout = helpers.visitors_by_country(mongo)
    return render_template('ip_localizator/ip_stats.html', 
                           cities_plot_data=cities_data,
                           cities_plot_layout=cities_layout,
                           countries_plot_data=countries_data,
                           countries_plot_layout=countries_layout,
                           )

@app.route("/about")
def about():
    return render_template('ip_localizator/about.html')


if __name__ == '__main__':
    app.run()
