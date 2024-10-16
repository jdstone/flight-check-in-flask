from app import scheduler
# from app.extensions import scheduler
from datetime import datetime, timedelta
from flask import Blueprint
import app.southwest


bp = Blueprint('checkin', __name__, url_prefix='/')

def my_job():
    print('this is my job')


# if not scheduler.get_job('my_job1'):
#     scheduler.add_job(id='my_job1', func=my_job, trigger="date", run_date=datetime(2024, 11, 29, 15, 50, 0))

# scheduler.add_job(id='my_job1', func=my_job, trigger="date", run_date=datetime(2024, 11, 14, 22, 39, 0))
# print(f"My JOB: {scheduler.get_job('my_job1')}")

# scheduler.scheduler.remove_jobstore('default')
# scheduler.scheduler.remove_jobstore('SQlite')
# scheduler.scheduler.remove_all_jobs()

# scheduler.remove_jobstore('default')
# scheduler.remove_jobstore('SQlite')
# scheduler.remove_all_jobs()

# while True:
#     scheduler.scheduler.print_jobs()
#     time.sleep(15)



@bp.post("/schedule-checkin")
def create_job(flight_date, flight_time, conf_number, first_name, last_name):
    job_id = conf_number
    run_time = calculate_checkin_time(flight_date, flight_time)
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

