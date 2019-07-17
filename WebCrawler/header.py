from WebCrawler import settings
import os


COOKIE = ""
COOKIE_PATH = os.path.join(settings.STATIC_ROOT, 'cookie.txt')
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"


def get_cookie():
    global COOKIE
    if not COOKIE:
        with open(COOKIE_PATH, 'r') as f:
            COOKIE = f.read()
    return COOKIE


def set_cookie(cookie):
    if cookie and COOKIE != cookie:
        with open(COOKIE_PATH, 'w') as f:
            f.write(cookie)


def get_header():
    return {
        'User-Agent': USER_AGENT,
        'Cookie': get_cookie()
    }
