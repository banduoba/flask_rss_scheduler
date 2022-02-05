import datetime
import os
import random

from flask import render_template, request

from app import app
from app.models import Tasks, Threads
from common.common_utils import Utils
from common.log_utils import logFactory

logger = logFactory("web").log


def pre():
    web = Utils.read_config("web")

    data = {
        "web": web,
        "people": record_people()
    }

    return data


def record_people():
    people_path = Utils.get_project_root_path() + "/cache/people.txt"
    if not os.path.exists(people_path):
        Utils.write_file(people_path, "0")

    people = Utils.read_file(people_path)
    people = int(people) + 1
    Utils.write_file(people_path, str(people))

    return people


@app.route('/')
def index():
    data = pre()

    num = 10
    new_categorys = []
    categorys = Utils.read_config("categorys")
    for category in categorys:
        new_categorys.append({
            "category": category,
            "size": random.randint(10, 30)
        })

    try:
        page = request.args.get("page", 1)
        arg_category = request.args.get("category", "")
    except Exception:
        page = 1
        arg_category = ""

    task_count = Tasks.query.count()
    thread_count = Threads.query.count()

    data.update({
        "nav_active": "index",
        "categorys": new_categorys,
        "task_count": task_count,
        "thread_count": thread_count
    })

    try:
        end_data = datetime.date(year=2023, month=1, day=1)

        filters = [Threads.publish_time < end_data]
        if arg_category and len(arg_category) != 0:
            filters.append(
                Threads.category == arg_category
            )
        threads = Threads.query \
            .order_by(Threads.publish_time.desc()).filter(*filters) \
            .offset(int(num) * (int(page) - 1)) \
            .limit(num)
        threads = Utils.database2_json(threads)
    except Exception:
        threads = []

    return render_template("index.html", data=data, threads=threads, page=int(page) + 1, cur_categpry=arg_category)
