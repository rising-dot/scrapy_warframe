
import requests, pytz
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor


def send_requests():
    requests.post("https://agile-scrubland-59074.herokuapp.com/schedule.json", data={
        'project': 'default',
        'spider': 'statistics'
    })

if __name__ == '__main__':
    scheduler = TwistedScheduler(timezone=pytz.utc)
    scheduler.add_job(send_requests, 'interval', hours=1, start_date='2019-05-27 14:00:00')
    scheduler.start()
    reactor.run()
