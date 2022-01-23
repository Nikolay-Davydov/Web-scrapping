import requests
import bs4 


HEADERS = {'Cookie': '_ym_d=1632417883; _ym_uid=1632417883101874388; _ga=GA1.2.242725729.1632417883; __gads=ID=8e39d4d48a409f1d:T=1632418144:S=ALNI_MbwaT6C0GUuDNjxAlihba3_CEP4bQ; fl=ru; hl=ru; feature_streaming_comments=true',
 'Sec-Fetch-Dest': 'document',
 'Sec-Fetch-Mode': 'navigate',
 'Sec-Fetch-Site': 'same-origin',
 'Sec-Fetch-User': '?1',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
 }
KEYWORDS = ['даже', 'корпорации']

def get_data(url):
  response = requests.get(url, headers=HEADERS)
  response.raise_for_status()
  text = response.text
  soup = bs4.BeautifulSoup(text, features='html.parser')
  return soup

all_article_soup = get_data('https://habr.com/ru/all/')
articles = all_article_soup.find_all('article')
 
for article in articles:
  find_flag = False
  article_title = article.find('h2').text
  href = article.find('a', class_ ='tm-article-snippet__title-link')['href']
  article_url = 'https://habr.com' + href
  
  hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
  artuicle_hubs =set([hub.find('span').text for hub in hubs])
  article_preview = article.find('div', class_='article-formatted-body').text

  for word in KEYWORDS:
    if (word in article_title) or (word in artuicle_hubs) or (word in article_preview):
      public_date_all = article.find('time')
      public_date = public_date_all.attrs['title']
      find_flag = True
      print(public_date, article_title, article_url)
      break
  if not find_flag:
    soup_article = get_data(article_url)   
    text_article_all = soup_article.find('div', class_ ='article-formatted-body').text
    for word_key in KEYWORDS:
      if word_key in text_article_all:
        public_date_all = article.find('time')
        public_date = public_date_all.attrs['title']
        print(public_date, article_title, article_url)
        break     
