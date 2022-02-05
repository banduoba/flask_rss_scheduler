import socket
import ssl

import feedparser

from common.common_utils import Utils
from common.log_utils import logFactory

ssl._create_default_https_context = ssl._create_unverified_context
socket.setdefaulttimeout(5)

logger = logFactory("parsers").log


class Parsers(object):
    @staticmethod
    def rss_parser(rss):
        try:
            request_headers = Utils.get_req_headers()
            parser = feedparser.parse(rss, request_headers=request_headers)

            pack_rss_res = []
            for entrie in parser.get('entries'):
                pack_rss_res.append({
                    "post_url": entrie.get("link"),
                    "title": entrie.get("title"),
                    "summary": entrie.get("summary"),
                    "updated": Utils.parser_rss_time(entrie.get("updated_parsed")),
                    "published": Utils.parser_rss_time(entrie.get("published_parsed"))
                })

            logger.info(f"rss_parser {rss} done!")
            return pack_rss_res

        except Exception as err:
            logger.exception(err)

        return None
