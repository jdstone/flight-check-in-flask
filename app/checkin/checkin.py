from app.checkin import bp
from app.checkin.forms import CheckinForm
from app.schedule import create_job
from flask import render_template, request


@bp.route("/", methods=['GET', 'POST'])
def checkin():
    form = CheckinForm()

    if form.validate_on_submit():
        passenger_first_name = request.form['first_name']
        passenger_last_name = request.form['last_name']
        flight_conf_number = request.form['conf_num']
        flight_date = request.form['flight_date']
        flight_time = request.form['flight_time']
        error = None

        if not passenger_first_name:
            error = "First name is required"
        elif not passenger_last_name:
            error = "Last name is required"
        elif not flight_conf_number:
            error = "Flight confirmation number is required"
        elif not flight_date:
            error = "Flight departure date is required"
        elif not flight_time:
            error = "Flight departure time is required"

        if error is None:
            return create_job(flight_date, flight_time, flight_conf_number, passenger_first_name, passenger_last_name)
        else:
            return error

    return render_template('checkin/checkin.html.j2', form=form)

