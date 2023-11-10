import random
import requests

proxies_list = open("rotating_proxies_list.txt", "r").read().strip().split("\n")
# todo make a separate list of usable and unusable proxies depending on whether they work or not


def get_random_proxy():
    proxies = tuple(proxies_list)
    return random.choice(proxies)


def get(url, proxy):
    if not proxy:
        proxy = get_random_proxy()
    try:
        response = requests.get(url, proxies={'http': f"http://{proxy}"}, timeout=30)
        print(response.status_code, proxy)
        return response.status_code, proxy
    except Exception as e:
        print(e)
        return None


def check_proxies():
    res, proxy = get("https://www.google.com/", None)
    valid_statuses = [200, 301, 302, 307, 404]
    if res not in valid_statuses:
        check_proxies()
    else:
        return proxy


if __name__ == '__main__':
    proxy_len = len(proxies_list)
    for p in range(0, proxy_len):
        check_proxies()
