import requests
import pandas as pd
import plotly
import plotly.graph_objs as go
import json


def get_ip_location(ip_address, geo_api_key):
    send_url = "http://api.ipstack.com/{}?access_key={}"
    try:
        req = requests.get(send_url.format(ip_address, geo_api_key), timeout=2)
    except Exception as e:
        raise Http404("Geocoder resolve issue!")

    if req.ok and "ip" in req.json():
        ip_geo_spec = req.json()
        lat = ip_geo_spec['latitude']
        long = ip_geo_spec['longitude']
        lat_long = {'lat': lat, 'long': long}
    else:
        ip_geo_spec = dict(ERROR='API Request to Geocoder has failed!')
    return ip_geo_spec

def visitors_stats(mongo):        
    df = pd.DataFrame(list(mongo.db.ips.find()))
    grouped = df.groupby(['country_name','city']).size().sort_values(ascending=False).reset_index(name="count").groupby('city')

    layout = dict(title='Visitors Count by Country&City',
                  #plot_bgcolor="peachpuff",
                  paper_bgcolor="peachpuff", barmode='stack') 
    plot_data = [go.Bar(dict(x=values['country_name'],y=values['count'], name=key)) for key,values in grouped]
    return json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder), layout