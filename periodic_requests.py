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
                      hours=1, start_date='2019-06-03 18:00:00', jitter=120)

    scheduler.start()
    reactor.run()



# if __name__ == '__main__':
#     scheduler = TwistedScheduler(timezone=pytz.utc)
#     scheduler.add_job(send_request, 'interval', hours=1, start_date='2019-06-02 20:00:00')
#     scheduler.start()
#     reactor.run()



# minutes=40, jitter=120) ----- no go
# minutes=30, jitter=120) ----- no go

# minutes=20, jitter=120) ----- good to go
# minutes=30)             ----- good to go
