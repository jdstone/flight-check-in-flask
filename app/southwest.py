from app import scheduler
from flask import Blueprint, request, current_app
import json
import requests

bp = Blueprint('southwest', __name__)


@bp.post("/checkin/")
def get_passenger_data():
    if request.is_json:
        data = request.get_json()
        conf_number = data['conf_number']
        first_name = data['first_name']
        last_name = data['last_name']
        current_app.logger.debug(f"'conf_number': {conf_number}, 'first_name': {first_name}, 'last_name': {last_name}")

        return checkin_review(conf_number, first_name, last_name)

    return {"error": "Passenger request must be made in JSON"}, 415


def checkin_review(conf_number, first_name, last_name):
    with scheduler.app.app_context():
        api_url = current_app.config['SW_REVIEW_API_URL']

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
        if 'data' not in response_review_data:
            # if code '403050700' is received from Southwest review check-in
            if str(response_review_data['code'])[:3] == "403":
                current_app.logger.critical("FORBIDDEN response (HTTP 403) received from Southwest Review API")
            else:
                current_app.logger.critical(f"Southwest API response: {response_review_data['code']}")
        else:
            current_app.logger.info(f"A review check-in for {conf_number}, passenger {first_name} {last_name} has occurred.")

            return checkin_confirm(headers, response_review_data, conf_number, first_name, last_name)

    current_app.logger.critical("There was a problem with the scheduler app context")

    return {"error": "Something went wrong"}


def checkin_confirm(headers, response_review_data, conf_number, first_name, last_name):
    if 'data' in response_review_data and \
      'searchResults' in response_review_data['data'] and \
      'token' in response_review_data['data']['searchResults']:

        with scheduler.app.app_context():
            api_url = current_app.config['SW_CONFIRM_API_URL']

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

            if 'success' in response_confirm_data:
                data = {
                        "flightBoardingGroup": response_confirm_data['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroup'],
                        "flightBoardingGroupPos": response_confirm_data['data']['searchResults']['travelers'][0]['boardingBounds'][0]['boardingSegments'][0]['boardingGroupPosition'],
                        "firstName": first_name,
                        "lastName": last_name,
                        "confNumber": conf_number,
                        "token": response_confirm_data['data']['searchResults']['token'],
                }
                json_data = json.dumps(data, indent=4)
                current_app.logger.info(f"A confirm check-in for {conf_number}, passenger {first_name} {last_name} has occurred.")

                return json_data
            else:
                # if code '403050700' is received from Southwest confirm check-in
                if str(response_confirm_data['code'])[:3] == "403":
                    current_app.logger.critical("FORBIDDEN response (HTTP 403) received from Southwest Confirm API")
                else:
                    current_app.logger.critical(f"Southwest API response: {response_confirm_data['code']}")

                return {"error": f"UNSUCCESSFUL check-in for {conf_number}, passenger {first_name} {last_name}"}, 404

        current_app.logger.critical("There was a problem with the scheduler app context")

        return {"error": "Something went wrong"}
    else:
        current_app.logger.critical(f"UNSUCCESSFUL confirm check-in for {conf_number}, passenger {first_name} {last_name}.")

        return {"error": "Review response JSON object does not exist and passenger could not be checked in"}

