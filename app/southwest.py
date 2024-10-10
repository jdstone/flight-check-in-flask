from flask import Blueprint, jsonify
import requests, json

bp = Blueprint('southwest', __name__, url_prefix='/')

confNumber = ""
firstName = ""
lastName = ""

@bp.post("/checkin")
def checkin_review(confNumber, firstName, lastName):
    apiUrl = "https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/review"
    requestReviewData = {
        "confirmationNumber": confNumber,
        "passengerFirstName": firstName,
        "passengerLastName": lastName,
        "application": "air-check-in",
        "site": "southwest",
    }
    headers = {
        "authorization": "null null",
        "origin": "https://www.southwest.com",
        "x-api-idtoken": "null",
        "x-api-key": "l7xx944d175ea25f4b9c903a583ea82a1c4c",
        "x-channel-id": "southwest",
        "accept-encoding": "gzip, deflate, br",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
    }

    reviewHeaders = {
        "referer": f"https://www.southwest.com/air/check-in/review.html?confirmationNumber={confNumber}&passengerFirstName={firstName}&passengerLastName={lastName}",
        "Content-Length": str(len(str(requestReviewData))),
    }
    reviewHeaders = {**headers, **reviewHeaders}

    response = requests.post(apiUrl, json=requestReviewData, headers=reviewHeaders)
    responseReviewData = json.loads(response.text)

    return checkin_confirm(headers, responseReviewData)


def checkin_confirm(headers, responseReviewData):
    if responseReviewData['data']['searchResults']['token']:
        apiUrl = "https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/confirmation"
        requestConfirmData = {
            "token": responseReviewData['data']['searchResults']['token'],
            "confirmationNumber": responseReviewData['data']['searchResults']['reservation']['confirmationNumber'],
            "passengerFirstName": responseReviewData['data']['searchResults']['reservation']['travelers'][0]['firstName'],
            "passengerLastName": responseReviewData['data']['searchResults']['reservation']['travelers'][0]['lastName'],
            "application": "air-check-in",
            "site": "southwest",
        }

        confirmHeaders = {
            "referer": "https://www.southwest.com/air/check-in/confirmation.html?drinkCouponSelected=false",
            "Content-Length": str(len(str(requestConfirmData)))
        }
        confirmHeaders = {**headers, **confirmHeaders}

        response = requests.post(apiUrl, json=requestConfirmData, headers=confirmHeaders)
        responseConfirmData = json.loads(response.content)
        if responseConfirmData['success']:
            data = {
                    "flightBoardingGroup": responseConfirmData['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroup'],
                    "flightBoardingGroupPos": responseConfirmData['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroupPosition'],
                    "firstName": responseConfirmData['data']['searchResults']['travelers'][0]['firstName'],
                    "lastName": responseConfirmData['data']['searchResults']['travelers'][0]['lastName'],
                    "confNumber": responseConfirmData['data']['searchResults']['confirmationNumber'],
                    "token": responseConfirmData['data']['searchResults']['token'],
                }
            json_data = json.dumps(data, indent=4)
            return json_data

