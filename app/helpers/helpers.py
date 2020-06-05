import requests

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