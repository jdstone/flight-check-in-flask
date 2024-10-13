from app import scheduler
# from app.extensions import scheduler
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, current_app
import logging
import app.southwest
from config import config


bp = Blueprint('checkin', __name__, url_prefix='/')

def my_job():
    print('this is my job')


# scheduler.add_job('mydatejob', my_job, run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
# scheduler.add_job(id='my_job1', func=my_job, trigger="date", run_date=datetime(2024, 10, 12, 20, 5, 0), replace_existing=True)

# if scheduler.scheduler.get_job('my_job7'):


# if not scheduler.get_job('my_job10'):
#     scheduler.add_job(id='my_job10', func=my_job, trigger="date", run_date=datetime(2024, 11, 15, 11, 39, 0))
# if not scheduler.get_job('my_job1'):
#     scheduler.add_job(id='my_job1', func=my_job, trigger="date", run_date=datetime(2024, 11, 29, 15, 50, 0))
# scheduler.add_job(id='my_job4', func=my_job, trigger="date", run_date=datetime(2024, 11, 13, 11, 39, 0))
print(f"My JOB: {scheduler.scheduler.get_job('my_job10')}")
# for job in scheduler.get_jobs():
#     print(f"My JOB: {scheduler.get_job(job)}")

# print("PRINTING JOBS...")
# scheduler.scheduler.print_jobs()
# scheduler.scheduler.get_jobs()
# scheduler.scheduler.remove_jobstore('default')
# scheduler.scheduler.remove_jobstore('SQlite')
# scheduler.scheduler.remove_all_jobs()

# scheduler.print_jobs()
# scheduler.get_jobs()
# scheduler.remove_jobstore('default')
# scheduler.remove_jobstore('SQlite')
# scheduler.remove_all_jobs()

# while True:
#     scheduler.scheduler.print_jobs()
#     time.sleep(15)

# scheduler.scheduler.remove_jobstore('default')
# scheduler.scheduler.remove_jobstore('SQlite')
# scheduler.scheduler.remove_all_jobs()


@bp.post("/schedule-checkin")
def create_job(flight_date, flight_time, conf_number, first_name, last_name):
    job_id = conf_number
    # job_id = "my_job"
    run_time = calculate_checkin_time(flight_date, flight_time)
    # run_time = calculate_checkin_time('11/22/24', '13:45')
    print(run_time)
    if not scheduler.get_job(job_id):
        scheduler.add_job(
            id=job_id,
            func=app.southwest.checkin_review,
            args=(conf_number, first_name, last_name),
            trigger="date",
            run_date=run_time
        )

def calculate_checkin_time(flight_date, flight_time):
    # concat date and time together
    flight_datetime = f"{flight_date} {flight_time}"
    # convert time string to datetime object
    checkin_datetime = datetime.strptime(flight_datetime, '%m/%d/%y %H:%M')
    checkin_datetime = checkin_datetime - timedelta(hours=23, minutes=59, seconds=55)

    return checkin_datetime

# create_job('11/22/24', '13:45', 'W34322', 'Johnny', 'Appleseed')
# scheduler.scheduler.print_jobs()

