from flask import Blueprint, request, current_app
from app import scheduler
import requests, json


bp = Blueprint('southwest', __name__, url_prefix='/')


@bp.post("/checkin")
def get_passenger_data():
    if request.is_json:
        data = request.get_json()
        conf_number = data['conf_number']
        first_name = data['first_name']
        last_name = data['last_name']
        return checkin_review(conf_number, first_name, last_name)
    return {"error": "Request must be JSON"}, 415

def checkin_review(conf_number, first_name, last_name):
    with scheduler.app.app_context():
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

        current_app.logger.info("A review checkin has occurred.")

        return checkin_confirm(headers, response_review_data)


def checkin_confirm(headers, response_review_data):
    if response_review_data['data']['searchResults']['token']:
        with scheduler.app.app_context():
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
                current_app.logger.info("A confirm checkin has occurred.")
                return json_data
            return {"error": "Check-in was not successful"}
        return {"error": "Check-in was not successful"}, 404

