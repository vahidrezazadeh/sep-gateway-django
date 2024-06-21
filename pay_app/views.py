from django.shortcuts import render
from django.http import HttpResponse
import time
import math
import requests
import json

token_api_url = "https://sep.shaparak.ir/onlinepg/onlinepg"
verify_url = "https://sep.shaparak.ir/verifyTxnRandomSessionkey/ipg/VerifyTransaction"

TerminalId = ""  # SET Your Terminal Id HERE
RedirectURL = "http://localhost:8000/pay/verify-saman"  # SET CALLBACK URL THERE


def go_to_gateway(req):
    ResNum = math.floor(time.time()*1000)  # شماره پیگیری
    phoneNumber = '09217820205'
    amount = 10000
    data = {
        "Action": "Token",
        "Amount": amount,
        "Wage": 0,
        "TerminalId": TerminalId,
        "ResNum": ResNum,
        "RedirectURL": RedirectURL,
        "CellNumber": phoneNumber,
    }
    print(data)
    result = requests.post(token_api_url, data)
    resObj = json.loads(result.text)
    if "status" not in resObj:
        return HttpResponse("ERROR : "+result.text)
    if resObj["status"] == 1:
        return render(req, 'goToGateway.html', {'token': resObj['token']})

    return HttpResponse("ERROR CODE : "+str(resObj['status']))


def verify(req):
    if req.POST != "POST":
        return HttpResponse("METHOD ERROR")
    print(req.Post)
    state = req.POST.get("State", "Failed")

    if state != "OK":
        return HttpResponse("ERROR STATUS : "+state)

    RefNum = req.POST.get("RefNum")

    data = {
        "TerminalNumber": TerminalId,
        "RefNum": RefNum
    }

    result = requests.post(verify_url, data)

    resObj = json.loads(result.text)

    print(resObj)

    if "Success" not in resObj:
        return HttpResponse("Success Not Found")

    if resObj["Success"] == False:
        return HttpResponse("Transaction Failed ")

    print(resObj["TransactionDetail"])
    return HttpResponse("eyval , poolo gereftim.")
