import requests


def getAdminProfile(token):
    #get the profile data of superadmin 
    url = "http://user:5000/profile/admin"
    headers = {
        "authToken" : token
    }
    response = requests.get(url, headers=headers)
    return response.json()

def getVendorProfile(token):
    #get profile data of Vendor user(restaurant owner/admin)
    url = "http://user:5000/profile/vendor"
    headers = {
        "authToken" : token
    }
    response = requests.get(url, headers=headers)
    return response.json()

def getUserProfile(token):
    #get profile data of Normal users/customers
    url = "http://user:5000/profile"
    headers = {
        "authToken" : token
    }
    response = requests.get(url, headers=headers)
    return response.json()