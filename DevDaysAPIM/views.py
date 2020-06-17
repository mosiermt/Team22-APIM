"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DevDaysAPIM import app
import requests

BASE_URL = "https://team22fhirserver.azurehealthcareapis.com/"

def getAuth():
    clientId = "e0794595-ba4c-4606-970b-f683a45c0df6"
    secret = "jQCkPYtv2Qezy~-_OFI7.Y0oI6rt.3fT0s"
    callback = "http://localhost:5000/callback"

    queryString = "?response_type=token&client_id={clientId}&scope=https%3A%2F%2Fteam22fhirserver.azurehealthcareapis.com%2Fdaemon&redirect_uri=https%3A%2F%2Flocalhost%3A5000%2Fcallback"

    response = requests.get("https://login.microsoftonline.com/b3d5c713-586f-449f-a7de-45c3283de364/oauth2/v2.0/authorize"+queryString)
    result = response.text
    print(result)
    token = ""
    return {"Authorization": f"Bearer {token}"}

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route(f'/api/ExplanationOfBenefit/<patient>')
def EoB(patient):
    r = requests.get(BASE_URL+"ExplanationOfBenefit", headers = getAuth())
    result = r.json()
    returnBundle = {"entry": []}
    for entry in result["entry"]:
        if patient in entry["patient"]["reference"]:
            returnBundle["entry"].append(entry)
    return returnBundle