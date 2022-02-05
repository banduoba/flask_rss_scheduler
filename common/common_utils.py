import datetime
import json
import os
from time import mktime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Utils(object):
    @staticmethod
    def ret_true(msg=None):
        if msg:
            return Utils.json_dumps({"status": True, "message": msg})
        return Utils.json_dumps({"status": True})

    @staticmethod
    def ret_false(msg=None):
        if msg:
            return Utils.json_dumps({"status": False, "message": msg})
        return Utils.json_dumps({"status": False})

    @staticmethod
    def json_dumps(json_obj):
        return json.dumps(json_obj, ensure_ascii=False)

    # 将 rss_together 改为你的工程名
    @staticmethod
    def get_project_root_path():
        return os.path.abspath(os.path.dirname(__file__)).split("rss_together")[0] + "rss_together"

    @staticmethod
    def check_link(link):
        try:
            if not link.startswith("http") and not link.startswith("https"):
                return False

            request_headers = Utils.get_req_headers()
            response = requests.get(link, headers=request_headers, timeout=10)
            if response.status_code != 200:
                return False

            return True
        except:
            return False

    @staticmethod
    def get_req_headers():
        return {
            "User-Agent": UserAgent(path=Utils.get_project_root_path() + "/0.1.11").random,
        }

    @staticmethod
    def read_config(item_name, path=None):
        if path is None:
            path = os.path.join(Utils.get_project_root_path(), "config/config.json")

        return Utils.read_file(path, _json=True).get(item_name)

    @staticmethod
    def read_file(path, _json=False):
        with open(path, "r", encoding="utf-8") as file:
            if _json:
                return json.load(file)
            return file.read()

    @staticmethod
    def write_file(path, data, _json=False, method="w"):
        with open(path, method, encoding="utf-8") as file:
            if _json:
                file.write(json.dumps(data, ensure_ascii=False))
            else:
                file.write(data)

    @staticmethod
    def get_cache_path():
        return Utils.get_project_root_path() + "/cache"

    @staticmethod
    def parser_rss_time(param):
        return datetime.datetime.fromtimestamp(mktime(param)).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def str2datetime(param):
        return datetime.datetime.strptime(param, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def database2_json(objs):
        list = []
        for obj in objs:
            item = obj.to_json()
            list.append(item)

        return list

    @staticmethod
    def strip_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
