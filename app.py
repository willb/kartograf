from flask import Flask
from flask import request
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import requests

import folium

class AddressForm(FlaskForm):
    address = StringField('address', validators=[DataRequired()])

app = Flask(__name__)
app.config["SECRET_KEY"] = "baricades misterieuses"

@app.route('/map')
@app.route('/map/')
def index():
    lat = float(request.args.get("lat", "43.0730556"))
    lon = float(request.args.get("lon", "-89.4011111"))
    folium_map = folium.Map(location=(lat, lon), zoom_start=14)
    _map = folium_map._repr_html_()
    return render_template('map.html', themap=_map)

@app.route('/lookup', methods=["GET"])
def querypage():
    form = AddressForm()
    return render_template('lookup.html', form=form)
    pass

@app.route('/lookup', methods=["POST"])
def lookup():
    form = AddressForm()
    if form.validate_on_submit():
        "https://nominatim.openstreetmap.org/search?"
        return "ok!"
        
    return "no way"

