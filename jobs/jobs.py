from multiprocessing.pool import ThreadPool

from sqlalchemy import and_

from app import db
from app.models import Tasks, Threads
from common import constants
from common.common_utils import Utils
from common.log_utils import logFactory
from parsers.parsers import Parsers


class Jobs(object):
    def __init__(self):
        self.logger = logFactory("jobs").log

    def pick_up_rss_task(self):
        ids = []
        tasks = Tasks.query.filter(and_(
            Tasks.type == constants.TASK_TYPE_RSS,
            Tasks.status == constants.TASK_STATUS_WATTING,
        )).all()

        task_count = len(tasks)
        self.logger.info(f"pick_up_rss_task({task_count})")

        if task_count == 0:
            return

        for task in tasks:
            ids.append(task.id)

        pool = ThreadPool(
            processes=int(Utils.read_config("process")))
        pool.map(self.add_thread, ids)
        pool.close()
        pool.join()

    def add_thread(self, task_id):
        task = Tasks.query.filter_by(id=int(task_id)).first()

        try:
            task.status = constants.TASK_STATUS_RUNNING
            db.session.commit()

            rss = task.rss
            pack_rss = Parsers.rss_parser(rss)

            if not pack_rss:
                raise RuntimeError(f"{rss} parse error")

            for item in pack_rss:
                self.handle_rss(item, task)

            task.status = constants.TASK_STATUS_SUCCESS
            db.session.commit()

        except Exception as err:
            db.session.rollback()

            self.logger.exception(err)

            task.status = constants.TASK_STATUS_WARNING
            db.session.commit()

        finally:
            db.session.close()
            db.session.remove()

    def handle_rss(self, item, task):
        try:
            post_url = item.get("post_url")
            result = Utils.check_link(post_url)
            thread = Threads.query.filter_by(post_url=post_url).first()

            if not result and thread:
                Threads.delete_thread(thread)
                return

            if not result:
                self.logger.info(f"check link false {post_url}")
                return

            author_name = task.author_name
            category = task.category
            title = item.get("title")
            summary = item.get("summary")
            post_url = item.get("post_url")

            if not thread:
                Threads.add_thread(
                    author_name=task.author_name,
                    title=title,
                    post_url=post_url,
                    summary=summary,
                    category=category,
                    publish_time=Utils.str2datetime(item.get("published")),
                    update_time=Utils.str2datetime(item.get("updated"))
                )
            elif thread.title != title or thread.summary != summary or thread.author_name != author_name or thread.category != category:
                Threads.update_thread(
                    thread=thread,
                    author_name=task.author_name,
                    title=title,
                    post_url=post_url,
                    summary=summary,
                    category=category,
                    publish_time=Utils.str2datetime(item.get("published")),
                    update_time=Utils.str2datetime(item.get("updated"))
                )

        except Exception as err:
            self.logger.exception(err)
