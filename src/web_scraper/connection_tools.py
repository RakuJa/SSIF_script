import random
import time

import requests
from requests.exceptions import ProxyError
from lxml.html import fromstring

BOT_BLACKLISTED = ["To discuss automated access to Amazon data please contact",
                   "For automated access to price change or offer listing change events"]

TIMEOUT_FOR_GET = 5
WAIT_BETWEEN_PROXY_SCRAPING = 10
NUMBER_OF_PROXY_ROWS = 20


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:NUMBER_OF_PROXY_ROWS]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return list(proxies)


def check_status(page):
    """
    Method that will check and show information about the status of the passed request object.
    :param page: the requests returned object
    :return: True if the requests went well (code == 200)
    """
    print("check status")
    print(page)
    if page is None:
        return False
    if page.status_code == 200:
        # 200 = ok but that doesn't mean that i'm done
        if BOT_BLACKLISTED[1] in page.text:
            print("You got marked as a bot and returned a captcha!")
            return False
        else:
            print("Search found, extrapolating content.. \n")
            return True
    if page.status_code == 404:
        print("Error..  \n")
        return False
    if page.status_code > 500:
        if BOT_BLACKLISTED[0] in page.text:
            print("Page was blocked by Site. You got marked as a bot\n")
            return False
        else:
            print("Page must have been blocked by Site as the status code was %d" % page.status_code)
            return False


def iterate_request(url, session) -> requests.models.Response:
    """
    This method will iterate n times the request to the url given in input. with n == len(proxy_pool)
    If the requests goes well it will instantly return the value without iterating further
    :param url: The page to iterate the request on
    :param proxy_pool: a pool of ip to use as proxies
    :param session: requests.Session()
    :return: Page if the requests goes well or None if it iterates without success
    """
    # randomize the proxy order
    proxy_pool = get_proxies()
    random.shuffle(proxy_pool)
    i: int = 0
    for proxy in proxy_pool:
        # Get a proxy from the pool
        _proxies = {'http': 'http://' + proxy, "https": 'https://' + proxy}
        print("Ip used to connect proxy: {}".format(proxy))  # it will print proxy: ip
        print("Request #%d" % i)
        session.proxies.update(_proxies)
        response = None
        try:
            response = session.get(url, timeout=TIMEOUT_FOR_GET)  # get with 10 seconds timeout
        except ProxyError as e:
            print("Connection refused by target machine, maybe you tried too much in a short span of time..")
        if check_status(response):
            # search gone well!
            return response
        i += 1
        # This means that the request failed, it happens, maybe overload
    return None


def download_page(url) -> requests.models.Response:
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
            else:
                print("Cannot connect... scraping a new proxy list..")
                time.sleep(WAIT_BETWEEN_PROXY_SCRAPING)
        except Exception as e:
            print(e)
