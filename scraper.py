import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="news V_Title_Img" or @class="V_Title"]/text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p[not (@class)]/text()'


def parse_notice(link , today):
  try:
    response = requests.get(link)
    if response.status_code != 200:
      raise ValueError(f'Error: {response.status_code}')
    notice = response.content.decode('utf-8')
    parsed = html.fromstring(notice)
    print(parsed)
    try:
      title = parsed.xpath(XPATH_TITLE)[1]
      title = title.replace('\"','')
      print(title)
      summary = parsed.xpath(XPATH_SUMMARY)[0]
      body = parsed.xpath(XPATH_BODY)
    except IndexError:
      return
    with open(f'noticias/{today}/{title}.txt','w', encoding='utf-8') as f:
      f.write(title)
      f.write('\n\n')
      f.write(summary)
      f.write('\n\n')
      for p in body:
        f.write(p)
        f.write('\n')
  except ValueError as ve:
    print(ve)


def parse_home():
  try:
    response = requests.get(HOME_URL)
    if response.status_code != 200:
      raise ValueError(f'Error: {response.status_code}')
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    liksToNotices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
    today = datetime.date.today().strftime('%d-%m-%Y')
    if not os.path.isdir('noticias'):
      os.mkdir('noticias')
    if not os.path.isdir(today):
      os.mkdir(f'noticias/{today}')
    for link in liksToNotices:
      parse_notice(link , today)
  except ValueError as ve:
    print(ve)

def run():
  parse_home()

if __name__ == '__main__':
  run()