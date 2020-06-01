import helpers.helpers as helpers
import os

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from IPy import IP
from datetime import datetime
from pprint import pprint

app = Flask(__name__)
app.config['MONGO_URI'] = str(os.getenv('MONGO_URI'))
mongo = PyMongo(app)

@app.route("/")
def home():
    if IP(request.headers.getlist("X-Real-IP")[0]).iptype() == 'PUBLIC':
        client_ip_addr = request.headers.getlist("X-Real-IP")[0]
        ip_geo_data = helpers.get_ip_location(client_ip_addr)
        ip_data = dict(request=
            {
                "request_time": datetime.now(),
                "request_user_agent": str(request.headers.getlist("User-Agent")[0])
            }
        )
        ip_data['ip_geo_data'] = ip_geo_data
        # pprint(ip_data)
        mongo.db.ips.insert_one(ip_data)
    else:
        ip_geo_data = {"ip": "local"}
    return render_template('ip_localizator/index.html', ip_data={k:v for k,v in ip_data.items() if not k.startswith("_")} )

@app.route("/ip_stats")
def ip_stats():
    return render_template('ip_localizator/ip_stats.html')

@app.route("/about")
def about():
    return render_template('ip_localizator/about.html')

if __name__ == '__main__':
    app.run()
