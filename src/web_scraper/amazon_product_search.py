import os
import sys
import time

from bs4 import BeautifulSoup
import requests
import random

from requests.exceptions import ProxyError
import requests_random_user_agent
# This library will randomize user agent, don't delete
from src.web_scraper import get_list_of_proxy_scraper

import certifi

BASE_URL_LIST = ['https://www.amazon.it/s?k=']
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
BOT_BLACKLISTED = ["To discuss automated access to Amazon data please contact",
                   "For automated access to price change or offer listing change events"]

TIMEOUT_FOR_GET = 5
WAIT_BETWEEN_PROXY_SCRAPING = 10


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
            print("Page was blocked by Amazon. You got marked as a bot\n")
            return False
        else:
            print("Page must have been blocked by Amazon as the status code was %d" % page.status_code)
            return False


def iterate_request(url, proxy_pool, session) -> requests.models.Response:
    """
    This method will iterate n times the request to the url given in input. with n == len(proxy_pool)
    If the requests goes well it will instantly return the value without iterating further
    :param url: The page to iterate the request on
    :param proxy_pool: a pool of ip to use as proxies
    :param session: requests.Session()
    :return: Page if the requests goes well or None if it iterates without success
    """
    # randomize the proxy order
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
        proxies = get_list_of_proxy_scraper.get_proxies()
        try:
            response_page = iterate_request(url, proxies, session)
            if response_page is not None:
                return response_page
            else:
                print("Cannot connect... scraping a new proxy list..")
                time.sleep(WAIT_BETWEEN_PROXY_SCRAPING)
        except Exception as e:
            print(e)


def scrape_html(page) -> dict:
    """
    This method will get name, price and currency tag from html
    :param page: the html page to scrape, already downloaded
    :return: return dictionary with item name as a key and price and currency in a vector as value
    """
    soup = BeautifulSoup(page.content, 'html.parser')  # This will contain the html page

    # gets item name list
    item_found = soup.findAll("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
    # gets item price list
    price_found = soup.findAll("span", {"class": "a-price-whole"})
    # gets item currency list
    currency_found = soup.findAll("span", {"class": "a-price-symbol"})
    item_dictionary = {}
    for (curr_name, curr_price, curr_currency) in zip(item_found, price_found, currency_found):
        # gets name, price and currency strings
        name = curr_name.get_text()
        price = curr_price.get_text()
        currency = curr_currency.get_text()
        # put the value in a dictionary, name is a key, [price, currency] a value as a vector
        item_dictionary[name] = [price, currency]
    return item_dictionary


def print_dictionary(dictionary) -> None:
    """
    Prints a dictionary row by row as follows, key : value
    :param dictionary: dictionary to print out
    :return: None
    """
    for item in dictionary:
        tmp_vector = dictionary[item]
        currency = tmp_vector.pop()
        price = tmp_vector.pop()
        print(item + " : " + price + " " + currency)


def start():
    while True:
        name = input("Enter product to search for : ")
        product_list = name.split()
        result_string = product_list[0]
        product_list.remove(product_list[0])
        for substring in product_list:
            result_string += str(str("+") + str(substring))

        full_url = BASE_URL_LIST[0] + result_string

        page = download_page(full_url)
        item_dictionary = scrape_html(page)
        print_dictionary(item_dictionary)

        user_input = input("Search for another product? Y/N : ")
        if user_input.upper() == "N":
            sys.exit()
