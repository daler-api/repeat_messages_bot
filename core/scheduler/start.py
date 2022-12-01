from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'}, job_defaults={'misfire_grace_time': 15*60})
scheduler.add_jobstore(DjangoJobStore(), "default")


def start():
    scheduler.start()
    print("Стартанул")
