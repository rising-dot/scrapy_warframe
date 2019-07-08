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
    scheduler.add_job(send_request, 'interval', minutes=27, start_date='2019-07-07 20:00:00', jitter=120)  # active before 30min

    scheduler.start()
    reactor.run()







