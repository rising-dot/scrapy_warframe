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
    scheduler.add_job(send_request, 'cron', hour='*', jitter=120)

    scheduler.start()
    reactor.run()




#  'cron', day_of_week='mon-sun', hour='*', start_date='2019-06-13 14:00:00', jitter=120) --run 2 time only on a thusday
#  'cron', hour='*', start_date='2019-06-13 21:00:00', jitter=120)                        --did not run
#  'cron', day_of_week='thu-wed', hour='*', start_date='2019-06-13 22:00:00', jitter=120) --did not run

#  'interval', hours=1, start_date='2019-06-14 22:45:00', jitter=120)                     --did not run
#  'interval', hours=1, jitter=120)                                                       --did not run


# 'cron', hour='*', jitter=120)















