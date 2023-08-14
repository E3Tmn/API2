import requests
import os
from urllib.parse import urlparse


def is_bitlink(token, url):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    bit_links_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
      "Authorization": token
    }
    response = requests.get(bit_links_url, headers=headers)
    return response.ok


def count_clicks(token, url):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
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


def main():
    secret_token = os.environ['BITLY_TOKEN']
    user_link = input("Введите ссылку: ")
    try:
        if is_bitlink(secret_token, user_link):
            print("Количество переходов по ссылке: ", count_clicks(secret_token, user_link))
        else:
            print('Битлинк ', shorten_link(secret_token, user_link))
    except requests.exceptions.HTTPError as err:
        print(err)   


if __name__ == '__main__':
    main()
