import requests, pytz
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor


def send_request():
    requests.post("https://intense-dawn-47768.herokuapp.com/schedule.json", data={
        'project': 'default',
        'spider': 'statistics'
    })


if __name__ == '__main__':
    scheduler = TwistedScheduler(timezone=pytz.utc)
    scheduler.add_job(send_request, 'interval', minutes=27, start_date='2019-07-02 10:05:00', jitter=120)  # active before 30min

    scheduler.start()
    reactor.run()


#########################      --did not run
#  'cron', hour='*', jitter=120)                                                          --did not run
#  'cron', day_of_week='mon-sun', hour='*', start_date='2019-06-13 14:00:00', jitter=120) --run 2 time only on a thusday
#  'cron', hour='*', start_date='2019-06-13 21:00:00', jitter=120)                        --did not run
#  'cron', day_of_week='wed-tue', hour='*', start_date='2019-06-27 22:30:00', jitter=120)  # active before 30min
#########################      --did not run


#  'interval', hours=1, start_date='2019-06-14 22:45:00', jitter=120)                     --did not run
#  'interval', hours=1, jitter=120)                                                       --did not run
#  'interval', minutes=20, start_date='2019-06-16 08:00:00', jitter=120)                  --did not run

#  'interval', minutes=59, start_date='2019-06-17 16:00:00', jitter=120)                  --run only once   active before 30min



#minutes


# 'interval', minutes=59, start_date='2019-06-18 12:00:00', jitter=120)  # active before 30 min  run only once


# 'interval', minutes=18, start_date='2019-06-26 20:00:00', jitter=120)









