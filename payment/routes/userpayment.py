
from flask import render_template
from payment import app
import json
import requests
from payment.functions.responsehelper import *
from payment.functions.auth import getUserProfile
from werkzeug.exceptions import HTTPException
import os


@app.route('/user/payment/<oid>', methods=['GET'])
def khalti_Payment(oid):
    request = requests.get(os.environ.get('getorder')+oid)
    data =request.json()["data"]
    #print(data)
    # return "True"
    if "bbsmCart"  in data:
        productName=data["bbsmCart"]["productList"][0]["name"]
        productUrl=data["bbsmCart"]["productList"][0]["productImage"][0]
    else:
        productName=data["restCart"]["foodList"][0]["food_name"]
        productUrl=data["restCart"]["foodList"][0]["food_image"][0]
    if 'bbsmPrice' in data:
        price=data["bbsmPrice"]
    else:
        price=data["restPrice"]
    send={"AuthKeyPublic":os.environ.get('AuthKeyPublic'),"productIdentity":data["id"],"productName":productName,"amount":price,"productUrl":productUrl,"oid":oid}
    #return send
    return render_template("khalti.html",send=send)




@app.route('/khalti/verifyorder/<oid>/<kid>', methods=['GET'])
def user_payment(oid=None,kid=None):
    request = requests.get(os.environ.get('getorder')+oid)
    data =request.json()["data"]
    #print(data)
    if 'bbsmPrice' in data:
        price=data["bbsmPrice"]
    else:
        price=data["restPrice"]
    url = "https://khalti.com/api/v2/payment/status/"
    payload = {
    "token": kid,
    "amount": price
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.environ.get('AuthKey')
    }

    response = requests.get(url, payload, headers = headers)
    response = response.json()
    if response["amount"] == price*10:
        # update order paid status here
        payload={"paidStatus":"True"}
        requests.put(os.environ.get('updateorder')+oid,json.dumps(payload),headers=headers)
        return successResponse( message="Payment status verified")
    elif response["amount"] == data["restPrice"]:
        # update order paid status here
        payload={"paidStatus":"True"}
        requests.put(os.environ.get('updateorder')+oid,json.dumps(payload),headers=headers)
        return successResponse( message="Payment status verified")
    else:
        return errorResponse( message="Payment status not verified")
    
    
   

@app.errorhandler(HTTPException or Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response