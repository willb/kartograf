from flask import Flask, request, render_template, url_for, redirect

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import requests

import folium

class AddressForm(FlaskForm):
    start_address = StringField('Start address', validators=[DataRequired()])
    end_address = StringField('End address', validators=[DataRequired()])

app = Flask(__name__)
app.config["SECRET_KEY"] = "baricades misterieuses"

def resolve_address(address, endpoint="https://nominatim.openstreetmap.org"):
    api = f"{endpoint}/search"

    result = requests.get(api, params={"q": address, "format" : "jsonv2"})
    result_struct = result.json()[0]
    return (result_struct["lat"], result_struct["lon"])


def resolve_duration_and_distance(start_lon, start_lat, end_lon, end_lat, endpoint="http://127.0.0.1:5000"):
    api = f"{endpoint}/table/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"

    result = requests.get(api, params={"annotations": "duration,distance"})
    max_duration = max([x for xs in result.json()['durations'] for x in xs])
    max_distance = max([x for xs in result.json()['distances'] for x in xs])

    return (max_duration, max_distance)

def icon_for_color(color="red"):
    return folium.map.Icon(color=color)

@app.route('/map')
@app.route('/map/')
def index():
    lat1 = float(request.args.get("lat1", request.args.get("lat", "40.7769271")))
    lon1 = float(request.args.get("lon1", request.args.get("lon", "-73.873965")))
    
    lat2 = float(request.args.get("lat2", "40.768082"))
    lon2 = float(request.args.get("lon2", "-73.981893"))

    duration, distance = resolve_duration_and_distance(lon1, lat1, lon2, lat2)

    folium_map = folium.Map(location=(lat1, lon1), zoom_start=14)

    start_marker = folium.Marker([lat1, lon1], popup="Route start", icon=icon_for_color(color="lightblue")).add_to(folium_map)
    end_marker = folium.Marker([lat2, lon2], popup="Route end", icon=icon_for_color(color="red")).add_to(folium_map)
    
    _map = folium_map._repr_html_()
    return render_template('map.html', themap=_map, trip_distance=distance, trip_duration=duration)

@app.route('/lookup', methods=["GET"])
def querypage():
    form = AddressForm()
    return render_template('lookup.html', form=form)

@app.route('/lookup', methods=["POST"])
def lookup():
    form = AddressForm()
    if form.validate_on_submit():
        start_query = form.start_address.data
        end_query = form.end_address.data
        start_lat, start_lon = resolve_address(start_query)
        end_lat, end_lon = resolve_address(end_query)

        return redirect(url_for("index", lat1=start_lat, lon1=start_lon, lat2=end_lat, lon2=end_lon))

    return "no way"

