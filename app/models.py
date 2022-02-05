import datetime

import tldextract
from sqlalchemy import Text, Index

from app import db
from common import constants
from common.common_utils import Utils
from common.log_utils import logFactory

logger = logFactory("models_tasks").log


class Tasks(db.Model):
    __tablename__ = "tasks"

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        item["create_time"] = \
            item["create_time"].strftime("%Y-%m-%d %H:%M:%S")
        item["last_update_time"] = \
            item["last_update_time"].strftime("%Y-%m-%d %H:%M:%S")
        return item

    @staticmethod
    def add_task(
            author_name, rss, category, type=constants.TASK_TYPE_RSS, status=constants.TASK_STATUS_WATSTAT
    ):
        try:
            task = Tasks(
                author_name=author_name,
                rss=rss,
                type=type,
                category=category,
                status=status
            )
            db.session.add(task)
            db.session.commit()
            db.session.close()
            db.session.remove()

            logger.info(f"add task author_name({author_name}), rss({rss}), category({rss})")
            return True
        except Exception as err:
            logger.exception(err)
            db.session.rollback()

        return False

    @staticmethod
    def reset_tasks():
        try:
            tasks = Tasks.query.filter(
                Tasks.status != constants.TASK_STATUS_WATSTAT
            ).all()

            for task in tasks:
                task.status = constants.TASK_STATUS_WATTING

            db.session.commit()
            db.session.close()
            db.session.remove()

            logger.info(f"reset_task({len(tasks)})")
            return True
        except Exception as err:
            logger.exception(err)
            db.session.rollback()

        return False

    @staticmethod
    def is_exist(rss):
        val = tldextract.extract(rss)
        domain = f"{val.subdomain}.{val.domain}.{val.suffix}"
        if Tasks.query.filter(Tasks.rss.like("%" + domain + "%")).first():
            return True
        return False

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    author_name = db.Column(db.String(64), nullable=False)
    type = db.Column(db.Integer, default=constants.TASK_TYPE_RSS)
    status = db.Column(db.Integer, default=0)
    rss = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    __table_args__ = (
        Index("idx_unique", 'rss', unique=True),
        Index("idx_author_name", "author_name"),
        Index("idx_status", "status"),
        Index("idx_category", "category"),
    )


class Threads(db.Model):
    __tablename__ = "threads"

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        item["update_time"] = \
            item["update_time"].strftime("%Y-%m-%d")
        item["publish_time"] = \
            item["publish_time"].strftime("%Y-%m-%d")
        return item

    @staticmethod
    def add_thread(author_name, title, post_url, summary, category, publish_time, update_time):
        try:
            summary = Utils.strip_html(summary)
            thread = Threads(
                author_name=author_name,
                post_url=post_url,
                title=title,
                summary=summary[:300],
                category=category,
                publish_time=publish_time,
                update_time=update_time
            )
            db.session.add(thread)
            db.session.commit()

            logger.info(f"add thread {post_url}")
        except Exception as err:
            logger.exception(err)
            db.session.rollback()

    @staticmethod
    def update_thread(thread, author_name, title, post_url, summary, category, publish_time, update_time):
        try:
            thread.title = title
            thread.author_name = author_name
            thread.summary = summary[:300]
            thread.category = category
            thread.publish_time = publish_time
            thread.update_time = update_time
            logger.info(f"change thread {post_url}")
            db.session.commit()
        except Exception as err:
            logger.exception(err)
            db.session.rollback()

    @staticmethod
    def delete_thread(thread):
        try:
            logger.info(f"delete thread {thread.post_url}")
            db.session.delete(thread)
            db.session.commit()
        except Exception as err:
            logger.exception(err)
            db.session.rollback()

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    author_name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    post_url = db.Column(db.String(256), nullable=False)
    summary = db.Column(Text, default="无摘要")
    category = db.Column(db.String(64), nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)
    publish_time = db.Column(db.DateTime, default=datetime.datetime.now)

    __table_args__ = (
        Index("idx_unique", 'post_url', unique=True),
        Index("idx_author_name", "author_name"),
        Index("idx_title", "title"),
        Index("idx_category", "category"),
    )
