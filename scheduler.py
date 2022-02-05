import datetime
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

from app import db
from app.models import Tasks
from common.log_utils import logFactory
from jobs.jobs import Jobs

scheduler = BlockingScheduler(timezone='Asia/Shanghai')


class TaskScheduler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.logger = logFactory("task_scheduler").log
        self.jobs = Jobs()

    def job(self):
        self.logger.info("reset and run rss_job")
        Tasks.reset_tasks()
        self.jobs.pick_up_rss_task()
        db.session.commit()
        self.logger.info("reset and run rss_job done!")

    def run(self) -> None:
        scheduler.add_job(
            self.job, 'interval', minutes=10, next_run_time=datetime.datetime.now())
        scheduler.start()


def run_task_scheduler():
    task_scheduler = TaskScheduler()
    task_scheduler.run()


if __name__ == '__main__':
    run_task_scheduler()
