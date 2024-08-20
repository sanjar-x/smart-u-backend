from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from ..cache.redis.client import pool

scheduler = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
jobstore = RedisJobStore()
scheduler.add_jobstore(jobstore=jobstore)


# @scheduler.scheduled_job("interval", seconds=10)
# def synchronizer():
#     print("scheduled_job_1")


# # Job running at a specific date and time
# @scheduler.scheduled_job("date", run_date="2024-07-21 11:00:00")
# def scheduled_job_2():
#     print("scheduled_job_2")


# # Job running daily at 23:44:00
# @scheduler.scheduled_job("cron", day_of_week="mon-sun", hour=23, minute=44, second=0)
# def scheduled_job_3():
#     print("scheduled_job_3")
