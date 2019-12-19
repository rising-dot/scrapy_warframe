import requests, pytz
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor





# def no_sleep():
#     requests.get("https://intense-dawn-47768.herokuapp.com")
#


def send_request():
    requests.post("https://intense-dawn-47768.herokuapp.com/schedule.json", data={
        'project': 'default',
        'spider': 'statistics'
    })


if __name__ == '__main__':
    scheduler = TwistedScheduler(timezone=pytz.utc)
    #scheduler.add_job(send_request, 'interval', minutes=29, jitter=60)


    ##################################      Run every hour       ##################################################
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour='1-23', jitter=60)
    ########################################################################################


    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=0, minute=3, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=0, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=1, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=2, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=3, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=4, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=5, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=6, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=7, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=8, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=9, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=10, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=11, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=12, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=13, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=14, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=15, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=16, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=17, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=18, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=19, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=20, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=21, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=22, minute=29, jitter=60)
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour=23, minute=29, jitter=60)


    scheduler.start()
    reactor.run()


#   https://apscheduler.readthedocs.io/en/latest/modules/triggers/combining.html


# git init
#
# git add .
#
# git commit -m "initial commit"
#
# git push heroku master
#
#
# heroku ps:scale clock=1

# heroku logs --tail
























