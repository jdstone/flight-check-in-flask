# Automatic Flight Check-in

:warning: ~~This software no longer functions for its intended use and is available for a proof of concept only.~~

Although this app no longers functions for its intended use, you can still see how it works by using the accompanying [test suite](https://github.com/jdstone/flight-check-in-test-suite). See readme instructions there on how to set this up.

## TL;DR

I rewrote my [automatic flight check-in](https://github.com/jdstone/flight-check-in) web app (originally written in PHP). This was purely an exercise to learn Python and Flask because the API that this and the PHP version utilizes is no longer publicly available. Because of this, the software can no longer successfully check a passenger in.

Basically, the user enters their passenger and flight details (date and time), and the app will create a scheduled job that runs at exactly 23 hours, 59 minutes, and 55 seconds before the actual flight departs, which subsequently checks in the passenger to their [Southwest] flight.

## Details

The process is pretty much the same as it is with the PHP app described previously, with a couple improvements. I've also learned something, that due to the API no longer being available, I can't verify.

### Improvements

  - **Scheduler:** Previously, the app used Cron in Linux to process the passenger check-in to the flight. Cron was limited to only checking in on the minute and couldn't refine down to the granularity of seconds. But now I can.

    I use [APScheduler](https://github.com/agronholm/apscheduler/) and [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler/) to create a scheduled job that runs 23 hours, 59 minuets, and 55 seconds prior to your flight departure date/time. Example: if your flight is on 12/25/2024 at 7:45:00 am, the scheduled job is created and scheduled to run at 12/24/2024 7:45:05 am.

### Something I learned

  - Some of the header information I send with the API request is probably not required. It was sent with the original request when checking in through Southwest.com, so at the time I just assumed the information was required.

## Usage/Installation

1. Clone this repository
2. `cd flight-check-in`
3. `python3 -m venv .`
4. `pip install -r requirements.txt`
5. `flask run`

### API endpoints

* /sw/checkin

  Perform a check-in directly with Southwest and bypass using the frontend.
  `curl --header "Content-Type: application/json" --request POST --data '{"conf_number":"W89156","first_name":"Johnny","last_name":"Appleseed"}' http://127.0.0.1:5000/sw/checkin/`

* /schedule/checkin

  Schedule a check-in with the scheduler, and the scheduler will run the check-in job 23 hours, 59 minutes, and 55 seconds prior to flight departure date/time (for example below, job will run at 13:37:05 on 12/1/2024)
  `curl --header "Content-Type: application/json" --request POST --data '{"first_name":"Johnny","last_name":"Appleseed","conf_number":"W89156","flight_date":"2025-12-01","flight_time":"13:37"}' http://127.0.0.1:5000/schedule/checkin/`

