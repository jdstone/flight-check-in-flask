from flask import Blueprint, jsonify, current_app
import requests, json


bp = Blueprint('southwest', __name__, url_prefix='/')

conf_number = ""
first_name = ""
last_name = ""

@bp.post("/checkin")
def checkin_review(conf_number, first_name, last_name):
    sw_url = "https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/review"
    api_url = current_app.config['SW_REVIEW_API_URL'] or sw_url

    request_review_data = {
        "confirmationNumber": conf_number,
        "passengerFirstName": first_name,
        "passengerLastName": last_name,
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

    review_headers = {
        "referer": f"https://www.southwest.com/air/check-in/review.html?confirmationNumber={conf_number}&passengerFirstName={first_name}&passengerLastName={last_name}",
        "Content-Length": str(len(str(request_review_data))),
    }
    review_headers = {**headers, **review_headers}

    response = requests.post(api_url, json=request_review_data, headers=review_headers)
    response_review_data = json.loads(response.text)

    return checkin_confirm(headers, response_review_data)


def checkin_confirm(headers, response_review_data):
    if response_review_data['data']['searchResults']['token']:
        sw_url = "https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/confirmation"
        api_url = current_app.config['SW_CONFIRM_API_URL'] or sw_url

        request_confirm_data = {
            "token": response_review_data['data']['searchResults']['token'],
            "confirmationNumber": response_review_data['data']['searchResults']['reservation']['confirmationNumber'],
            "passengerFirstName": response_review_data['data']['searchResults']['reservation']['travelers'][0]['firstName'],
            "passengerLastName": response_review_data['data']['searchResults']['reservation']['travelers'][0]['lastName'],
            "application": "air-check-in",
            "site": "southwest",
        }

        confirm_headers = {
            "referer": "https://www.southwest.com/air/check-in/confirmation.html?drinkCouponSelected=false",
            "Content-Length": str(len(str(request_confirm_data)))
        }
        confirm_headers = {**headers, **confirm_headers}

        response = requests.post(api_url, json=request_confirm_data, headers=confirm_headers)
        response_confirm_data = json.loads(response.content)
        if response_confirm_data['success']:
            data = {
                    "flightBoardingGroup": response_confirm_data['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroup'],
                    "flightBoardingGroupPos": response_confirm_data['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroupPosition'],
                    "firstName": response_confirm_data['data']['searchResults']['travelers'][0]['firstName'],
                    "lastName": response_confirm_data['data']['searchResults']['travelers'][0]['lastName'],
                    "confNumber": response_confirm_data['data']['searchResults']['confirmationNumber'],
                    "token": response_confirm_data['data']['searchResults']['token'],
                }
            json_data = json.dumps(data, indent=4)
            return json_data

