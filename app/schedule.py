from app import scheduler
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app
from app.southwest import checkin_review

bp = Blueprint('schedule', __name__, url_prefix='/')


@bp.post("/schedule-checkin")
def get_passenger_data():
    if request.is_json:
        data = request.get_json()
        flight_date = data['flight_date']
        flight_time = data['flight_time']
        conf_number = data['conf_number']
        first_name = data['first_name']
        last_name = data['last_name']
        # flight_date sent in format: MM/DD/YY
        # flight_time sent in format: HH:MM
        return create_job(flight_date, flight_time, conf_number, first_name, last_name)

    return {"get_passenger.error": "Request must be JSON"}, 415

def create_job(flight_date, flight_time, conf_number, first_name, last_name):
    job_id = conf_number
    run_time = calculate_checkin_time(flight_date, flight_time)

    if not scheduler.get_job(job_id):
        scheduler.add_job(
            id=job_id,
            func=checkin_review,
            args=(conf_number, first_name, last_name),
            trigger="date",
            run_date=run_time
        )
        current_app.logger.info(f"Check-in scheduled for {conf_number}, {run_time}")

        return {"scheduler.job_created": "Success"}

    current_app.logger.error(f"Job id {job_id} already exists")

    return {"shceduler.error": f"Job id {job_id} already exists"}

def calculate_checkin_time(flight_date, flight_time):
    # concat date and time together
    flight_datetime = f"{flight_date} {flight_time}"
    # convert time string to datetime object
    checkin_datetime = datetime.strptime(flight_datetime, '%m/%d/%y %H:%M')
    checkin_datetime = checkin_datetime - timedelta(hours=23, minutes=59, seconds=55)

    return checkin_datetime

