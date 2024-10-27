# Automatic Flight Check-in

:warning: This software no longer functions and is available for a proof of concept only.

## TL;DR

I rewrote my [automatic flight check-in](https://github.com/jdstone/flight-check-in) web app (originally written in PHP). This was purely an exercise to learn Python and Flask because the API that this and the PHP version utilizes is no longer publicly available. Basically, the user enters their passenger and flight details (date and time), and the app will create a scheduled job that runs at exactly 23 hours, 59 minutes, and 55 seconds before the actual flight departs, which subsequently checks in the passenger to their [Southwest] flight.

## Details

The process is pretty much the same as it is with the PHP app described previously, with a couple improvements. I've also learned something, that due to the API no longer being available, I can't verify.

### Improvements

  - **Scheduler:** Previously, the app used Cron in Linux to process the passenger check-in to the flight. Cron was limited to only checking in on the minute and couldn't refine down to the granularity of seconds. But now I can.
  
  I use [APScheduler](https://github.com/agronholm/apscheduler/) to create a scheduled job that runs 23 hours, 59 minuets, and 55 seconds prior to your flight departure date/time. Example: if your flight is on 12/25/2024 at 7:45:00 am, the scheduled job is created and scheduled to run at 12/24/2024 7:45:05 am.

### Something I learned

  - Some of the header information I send with the API request is probably not required. It was sent with the original request when checking in through Southwest.com, so at the time I just assumed the information was required.

