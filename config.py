from urllib.parse import quote_plus as urlquote

from common.common_utils import Utils


class Config(object):
    config = Utils.read_config("db")

    host = config.get("host")
    user = config.get("user")
    passwd = urlquote(config.get("pass"))
    port = int(config.get("port"))
    dbnm = config.get("dbnm")

    SQLALCHEMY_DATABASE_URI \
        = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{dbnm}?charset=utf8mb4'

    SQLALCHEMY_POOL_SIZE = 1000
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 30
    SQLALCHEMY_TRACK_MODIFICATIONS = False
