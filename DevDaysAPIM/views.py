"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from DevDaysAPIM import app
import requests

BASE_URL = "https://team22fhirserver.azurehealthcareapis.com/"

def getAuth():
    clientId = "e0794595-ba4c-4606-970b-f683a45c0df6"
    secret = "jQCkPYtv2Qezy~-_OFI7.Y0oI6rt.3fT0s"
    redirect = "https://www.getpostman.com/oauth2/callback"
    # grant type -> Authorization Code
    auth = "https://login.microsoftonline.com/b3d5c713-586f-449f-a7de-45c3283de364/oauth2/v2.0/authorize"
    token = "https://login.microsoftonline.com/b3d5c713-586f-449f-a7de-45c3283de364/oauth2/v2.0/token"
    scope = "https://team22fhirserver.azurehealthcareapis.com/daemon"

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlNzWnNCTmhaY0YzUTlTNHRycFFCVEJ5TlJSSSIsImtpZCI6IlNzWnNCTmhaY0YzUTlTNHRycFFCVEJ5TlJSSSJ9.eyJhdWQiOiJodHRwczovL3RlYW0yMmZoaXJzZXJ2ZXIuYXp1cmVoZWFsdGhjYXJlYXBpcy5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9iM2Q1YzcxMy01ODZmLTQ0OWYtYTdkZS00NWMzMjgzZGUzNjQvIiwiaWF0IjoxNTkyNDE1MzM4LCJuYmYiOjE1OTI0MTUzMzgsImV4cCI6MTU5MjQxOTIzOCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhQQUFBQU5aNVBtT3lPMTBWM3ZxRVMrazhNOXdaMnB2US9ITTVsdU5FdFJyRC95TE4rOWpROFdaVjhKQ2I0QmpVemxmT0YrUGovc2dJeDEwTXU3bVV1WGUzcGN6ZTFHTVlVQkdCdUxnYVZUV1lIcFowPSIsImFtciI6WyJwd2QiXSwiYXBwaWQiOiJlMDc5NDU5NS1iYTRjLTQ2MDYtOTcwYi1mNjgzYTQ1YzBkZjYiLCJhcHBpZGFjciI6IjEiLCJlbWFpbCI6IkRldmRheXN0ZWFtMjJAb3V0bG9vay5jb20iLCJmYW1pbHlfbmFtZSI6InRlYW0gMjIiLCJnaXZlbl9uYW1lIjoiRmhpciBkZXYgZGF5cyIsImlkcCI6ImxpdmUuY29tIiwiaXBhZGRyIjoiNjguMTM0LjE3Mi45NyIsIm5hbWUiOiJGaGlyIGRldiBkYXlzIHRlYW0gMjIiLCJvaWQiOiIyNWE3ZWJiMi00NTA2LTRiZjMtODNhZS1mY2RiMGU2YjAwYzEiLCJzY3AiOiJkYWVtb24iLCJzdWIiOiJPdm9fSUpnbHV5MWV4OUFfRUZFSjMwY3RNMkM5RjBYWjRfaTVBSGoxNUNRIiwidGlkIjoiYjNkNWM3MTMtNTg2Zi00NDlmLWE3ZGUtNDVjMzI4M2RlMzY0IiwidW5pcXVlX25hbWUiOiJsaXZlLmNvbSNEZXZkYXlzdGVhbTIyQG91dGxvb2suY29tIiwidXRpIjoidElybm4tM20yRXUzYzM1ZV9RYmtBQSIsInZlciI6IjEuMCJ9.ZIV7H_PdwNapVTWJ5xnpeFriG9YPEydsJhptoCsk4AG_kl73j7M-7Mbvd0qLFhx3ZTtKcGy7me0w68IkBaKMLKPfMyYh9Ui0gJPfx9Z8Qxbo6mbPoDveipvshV985aS8R2i8cEXouEmMAL76k8hwIbt3ljdIxZ9vVUwh80-jDGDteBgOrS7g4DGvrts7fXx9wCnktt6liHLAga0lTLwG8Hk_WR26JlVgWV9rlCDjBhLuet8W7spb5d_QxGcLukjUrrTN451pHWloc7JNVDhmM1WU4N-buE_BanXi-0FpUeUUS2FkJdQBVucFlPEFGaZ7mgF5Ur-eSZSFbztqFXHQrA"
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

@app.route('/api/<resource>')
@app.route('/api/<resource>/<id>')
def PassThrough(resource, id=""):
    r = requests.request(request.method, f'{BASE_URL}{resource}/{id}', headers=getAuth())
    result = r.json()
    print(result)
    return jsonify({"status": r.status_code, "message": result})

@app.route('api/ExplanationOfBenefit')
def EoB(patient):
    r = requests.get(BASE_URL+"ExplanationOfBenefit", headers = getAuth())
    result = r.json
    returnBundle = {"entry": []}
    for entry in result["entry"]:
        if patient in entry["patient"]["reference"]:
            returnBundle["entry"].append(entry)
    return returnBundle

@app.route('api/TrendAnalysis')
def ObsBundle(patient):
    r = requests.get(BASE_URL+"Observation", headers = getAuth())
    result = r.json
    returnBundle = {"entry": []}
    for entry in result["entry"]:
        if patient in entry["patient"]["reference"]:
            returnBundle["entry"].append(entry)
    return returnBundle
