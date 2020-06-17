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


def triggerAlert(patientID, patientName):
    eobs = requests.get(f'{BASE_URL}ExplanationOfBenefit', headers=getAuth())
    eobList = eob.json()
    practitionerID = ""


    for eob in eobList["entry"]:
        if patientID in eob["patient"]["reference"]:
            if practitionerID != "":
                practitionerID = eob["provider"]["reference"].split(':')[-1]

    practitioner = requests.get(f'{BASE_URL}Practitioner/{practitionerID}', headers=getAuth())
    practitioner = practitioner.json()
    practitionerName = practitioner["name"][0]["prefix"][0] + ' ' + practitoiner["name"][0]["given"][0] + ' ' + practitioner["name"][0]["family"]
    email = practitioner["telecom"][0]["value"]


    headers = {
            "Content-Type": "application/json"
        }
    body = {
            "patientName": patientName,
            "patientID": patientID,
            "practitionerEmail": email,
            "practitionerName": practitionerName
        }
    r = request.post("https://prod-12.northcentralus.logic.azure.com:443/workflows/62a70a0642614461b3ec9c2767ee9236/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=XfeJAedegM-_xuZO42gleTI3wxojaxmXYsxEKZphp0E", json=body, headers=headers)
    return True


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/monitor/<patient>')
def monitor(patient):
    r = requests.request(request.method, f'{BASE_URL}Observation', headers=getAuth())
    result = r.json()
    filtered = []

    for entry in result["entry"]:
        if patient in entry["subject"]["reference"]:
            filtered.append(entry)

    #average
    #gather all datapoints into a list of tuples

    return jsonify({"status": r.status_code, "message": filtered})


@app.route('/api/Observation')
@app.route('/api/Observation/<id>')
def Observation(id=""):
    if request.method == "POST" or request.method == "PUT":
        body = request.json
        if body["resourceType"] == "Observation" and body["category"]["coding"][0]["code"] == "vital-signs":
            if body["code"]["coding"][0]["code"] == "8867-4":
                #heart rate limits
                if body["valueQuantity"]["value"] >= 85 or body["valueQuantity"]["value"] <= 30:
                    triggerAlert(body["subject"]["reference"].split('/')[-1], body["subject"]["display"])
    
    r = requests.request(request.method, f'{BASE_URL}Observation/{id}', headers=getAuth(), json=request.json)
    return jsonify({"status": r.status_code, "message": r.json()})


@app.route('/api/<resource>')
@app.route('/api/<resource>/<id>')
def PassThrough(resource, id=""):
    r = requests.request(request.method, f'{BASE_URL}{resource}/{id}', headers=getAuth())
    result = r.json()
    print(result)
    return jsonify({"status": r.status_code, "message": result})
