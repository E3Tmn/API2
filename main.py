import requests
import os
from urllib.parse import urlparse


def is_bitlink(token, url):
    bitlink = urlparse(url).netloc + urlparse(url).path
    bit_links_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
      "Authorization": token
    }
    response = requests.get(bit_links_url, headers=headers)
    return response.ok


def count_clicks(token, bitlink):
    temp = urlparse(bitlink)
    bitlink = temp.netloc + temp.path
    bit_links_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
      "Authorization": token
    }
    response = requests.get(bit_links_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def shorten_link(token, url):
    bit_links_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
      "Authorization": token
    }
    payload = {
      "long_url": url
    }
    response = requests.post(bit_links_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def main(token):
    user_link = input("Введите ссылку: ")
    is_bit = is_bitlink(token, user_link)
    bitlink = ''
    clicks_count = ''
    if is_bit:
        try:
            clicks_count = count_clicks(token, user_link)
        except requests.exceptions.HTTPError:
            print("Что-то пошло не так")
            return
        print("Количество переходов по ссылке: ", clicks_count)
    else:
        try:
            bitlink = shorten_link(token, user_link)
        except requests.exceptions.HTTPError:
            print("Что-то не так")
            return
        print('Битлинк ', bitlink)


if __name__ == '__main__':
    secret_token = os.environ['TOKEN_BITLY']
    main(secret_token)
