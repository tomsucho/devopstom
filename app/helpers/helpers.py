import requests
import pandas as pd
import plotly
import plotly.graph_objs as go
import json


def get_ip_location(ip_address, geo_api_key):
    send_url = "http://api.ipstack.com/{}?access_key={}"
    try:
        req = requests.get(send_url.format(ip_address, geo_api_key), timeout=2)
        if req.ok:
            ip_geo_spec = req.json()            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API Request to Geocoder has failed! MSG: {e}")
        ip_geo_spec = dict(ERROR='API Request to Geocoder has failed!')

    return ip_geo_spec

def visitors_stats(mongo):  
    plot_data = []
    layout = {}
    try:
        db_collection = list(mongo.db.ips.find())
    except Exception as e:
        print(f"ERROR: Fetching data from MongoDB has failed! MSG: {e}")
    
    if db_collection:        
        df = pd.DataFrame(db_collection)
        grouped = df.groupby(['country_name','city']).size().sort_values(ascending=False).reset_index(name="count").groupby('city')
        plot_data = [go.Bar(dict(x=values['country_name'],y=values['count'], name=key)) for key,values in grouped]
        layout = dict(title='Visitors Count by Country&City',
                  #plot_bgcolor="peachpuff",
                  paper_bgcolor="peachpuff", barmode='stack')

    return json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder), layout