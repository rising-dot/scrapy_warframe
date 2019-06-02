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
    scheduler.add_job(send_request, 'interval',
                      minutes=40, jitter=120)

    scheduler.start()
    reactor.run()



# if __name__ == '__main__':
#     scheduler = TwistedScheduler(timezone=pytz.utc)
#     scheduler.add_job(send_request, 'interval', hours=1, start_date='2019-06-02 09:45:00')
#     scheduler.start()
#     reactor.run()



