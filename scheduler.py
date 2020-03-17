from apscheduler.schedulers.background import BackgroundScheduler
import logging

from db.models import clear_unbanned_users

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler({
    # 'apscheduler.jobstores.default': {
    #     'type': 'sqlalchemy',
    #     'url': 'sqlite:///dcgc_channels.db'
    # },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})


def scheduler_init():
    if not scheduler.running:
        scheduler.start()
        scheduler.add_job(
            func=clear_unbanned_users,
            trigger='interval',
            minutes=2,
        )
