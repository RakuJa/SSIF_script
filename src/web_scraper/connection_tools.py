import logging
import random
import time
from http import HTTPStatus

import requests
from defusedxml.lxml import fromstring
from requests import Response, Session
from requests.exceptions import ProxyError

BOT_BLACKLISTED: list[str] = [
    "To discuss automated access to Amazon data please contact",
    "For automated access to price change or offer listing change events",
]

TIMEOUT_FOR_GET: int = 5
WAIT_BETWEEN_PROXY_SCRAPING: int = 10
NUMBER_OF_PROXY_ROWS: int = 20

logger = logging.getLogger(__name__)


def get_proxies() -> list[str]:
    url = "https://free-proxy-list.net/"
    response = requests.get(url, timeout=60)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath("//tbody/tr")[:NUMBER_OF_PROXY_ROWS]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy: str = ":".join(
                [i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]],
            )
            proxies.add(proxy)
    return list(proxies)


def check_status(page: Response) -> bool:
    """
    Method that will check and show information about
    the status of the passed request object.
    :param page: the requests returned object
    :return: True if the requests went well (code == 200)
    """
    logger.debug("checking status..")
    logger.debug(page)
    error: str = ""
    if page is None:
        return False
    if page.status_code == HTTPStatus.OK:
        # 200 = ok but that doesn't mean that the page is valid
        if BOT_BLACKLISTED[1] not in page.text:
            logger.info("Search found, extrapolating content.. \n")
            return True
        error = "You got marked as a bot and returned a captcha!"
    if page.status_code == HTTPStatus.NOT_FOUND:
        error = "Page not found"
    if page.status_code > HTTPStatus.INTERNAL_SERVER_ERROR:
        if BOT_BLACKLISTED[0] in page.text:
            error = "Page was blocked by Site. You got marked as a bot\n"
        else:
            error = (
                f"Page must have been blocked by"
                f" Site as the status code was {page.status_code}"
            )
    logger.warning(error)
    return False


def iterate_request(url: str, session: Session) -> requests.models.Response | None:
    """
    This method will iterate n times the request to the url given in input.
     with n == len(proxy_pool)
    If the requests goes well it will
     instantly return the value without iterating further
    :param url: The page to iterate the request on
    :param proxy_pool: a pool of ip to use as proxies
    :param session: requests.Session()
    :return: Page if the requests goes well or None if it iterates without success
    """
    # randomize the proxy order
    proxy_pool = get_proxies()
    random.shuffle(proxy_pool)
    i: int = 0
    for proxy in enumerate(proxy_pool):
        # Get a proxy from the pool
        _proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy,
        }
        print(f"Ip used to connect proxy: {proxy}")  # it will print proxy: ip
        print("Request #%d" % i)
        session.proxies.update(_proxies)
        response = None
        try:
            response = session.get(
                url,
                timeout=TIMEOUT_FOR_GET,
            )  # get with 10 seconds timeout
        except ProxyError as e:
            print(
                f"Connection refused by target machine with error {e}, "
                "maybe you tried too much in a short span of time..",
            )
        if check_status(response):
            # search gone well!
            return response
        # This means that the request failed, it happens, maybe overload
    return None


def download_page(url: str) -> requests.models.Response:
    """
    Method that will try on downloading a page until it succeeded
    :param url: url to page to download
    :return: downloaded page as a request.get return obj
    """
    session = requests.Session()
    while True:
        try:
            response_page = iterate_request(url, session)
            if response_page is not None:
                return response_page
            print("Cannot connect... scraping a new proxy list...")
            time.sleep(WAIT_BETWEEN_PROXY_SCRAPING)
        except Exception as e:
            print(e)
