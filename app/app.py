import helpers.helpers as helpers

from flask import Flask, render_template, request
from flask_pymongo import PyMongo

from IPy import IP

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://data_admin:secretx@mongodb:27017/ip_data?authSource=admin'
mongo = PyMongo(app)

@app.route("/")
def home():
    client_ip_addr = request.remote_addr if IP(request.remote_addr).iptype() == 'PUBLIC' else '188.122.0.220'
    ip_geo_data  = helpers.get_ip_location(client_ip_addr)
    if not mongo.db.ips.find_one({"ip": client_ip_addr}):
        mongo.db.ips.insert_one(ip_geo_data)
    
    return render_template('ip_localizator/index.html', ip_geo_data=ip_geo_data )

@app.route("/ip_stats")
def ip_stats(): 
    return render_template('ip_localizator/ip_stats.html')

if __name__ == '__main__':
    app.run(debug=True)
