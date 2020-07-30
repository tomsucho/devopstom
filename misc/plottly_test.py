# coding: utf-8
import pymongo
import pandas as pd
import plotly
import plotly.graph_objs as go
import json

client = pymongo.MongoClient('mongodb://data_admin:secretx@localhost:27017/ip_data?authSource=admin')
db = client.ip_data
ips = db.ips
df = pd.DataFrame(list(db.ips.find()))
# df.groupby(['country_name','city']).size().reset_index(name="count")
# data = df.groupby(['country_name','city']).size().reset_index(name="count")
# plot_data = [go.Bar(x=data['city'],y=data['count'])]
#fig = go.Figure(plot_data)
#pyo.plot(fig)
#json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)

grouped = df.groupby(['country_name','city']).size().reset_index(name="count").groupby('country_name')
#grouped = df.groupby('country_name')
# for key,value in grouped:
#     print(f"{key}:{value['city']}")

plot_data = [go.Bar(dict(x=values['city'],y=values['count'], name=key)) for key,values in grouped]
layout = go.Layout(barmode='stack')
fig = go.Figure(data=plot_data,layout=layout)
iplot(fig)