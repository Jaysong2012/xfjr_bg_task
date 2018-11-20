#coding: utf-8
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_MAX_INSTANCES, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from pytz import utc
class Scheduler:
    jobstores = {
        'default': MemoryJobStore(),
        'default_test': MemoryJobStore(),
    }
    executors = {
        'default': ThreadPoolExecutor(200),
        'processpool': ProcessPoolExecutor(10),
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 60,
    }
    @staticmethod
    def get_sched():
        scheduler = BackgroundScheduler()
        return scheduler