from flask import jsonify

def successResponse(message="",code=200):
    return jsonify({
        "code": code,
        "message": message,
        "status": True,
    }),code

def errorResponse(message="",code=400):
    return jsonify({
        "code": code,
        "message": message,
        "status" :False,
    }),code

def successWithResponse(data="",message="",code=200):
    return jsonify({
        "code": code,
        "data":data,
        "message": message,
        "status" :True,
    }),code

