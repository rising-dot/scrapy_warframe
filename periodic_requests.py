import requests, pytz
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor





def no_sleep():
    requests.get("https://intense-dawn-47768.herokuapp.com")



def send_request():
    requests.post("https://intense-dawn-47768.herokuapp.com/schedule.json", data={
        'project': 'default',
        'spider': 'statistics'
    })


if __name__ == '__main__':
    scheduler = TwistedScheduler(timezone=pytz.utc)

    scheduler.add_job(no_sleep, 'interval', minutes=10, jitter=120)
    scheduler.add_job(send_request, 'interval', minutes=28, jitter=120)

    scheduler.start()
    reactor.run()

