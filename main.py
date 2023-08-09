import requests
import os


def is_bitlink(url):
  my_secret = os.environ['TOKEN']
  bitlink = ''
  clicks_count = ''
   
  if url.find('bit.ly') == -1:
    try:
      bitlink = shorten_link(my_secret, url)
    except requests.exceptions.HTTPError:
      print("Что-то не так")
      return
    print('Битлинк', bitlink)
  else:
    try:
      clicks_count = count_clicks(my_secret, url)
    except requests.exceptions.HTTPError:
      print("Что-то пошло не так")
      return
      
def count_clicks(token, bitlink):
  bitlink = bitlink[8:]
  bit_links_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
  headers = {
    "Authorization": token
  }
  response = requests.get(bit_links_url,headers=headers)
  response.raise_for_status()
  print(response.json()['total_clicks'])
  
def shorten_link(token, url):
  bit_links_url = 'https://api-ssl.bitly.com/v4/bitlinks'
  headers = {
    "Authorization": token
  }
  payload = {
  "long_url":url
  }
  
  response = requests.post(bit_links_url,json=payload,headers=headers)
  response.raise_for_status()
  return response.json()['link']
  
def main():
  user_link = input("Ссылку дай: ")
  is_bitlink(user_link)
  
if __name__ == '__main__':
  main()