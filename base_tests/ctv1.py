import requests
from bs4 import BeautifulSoup
from hyperlink import URL

def print_link(title, url):
    url = URL.from_text(url)
    print(f'\x1b]8;;{url}\x1b\\{title}\x1b]8;;\x1b\\')

def scrape_news():
    base_url = "https://toronto.ctvnews.ca/more/local-news"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for index, story in enumerate(soup.find_all('h2', class_='teaserTitle')):
        title = story.text.strip()
        link = story.find('a')['href']
        if not link.startswith('http'):
            link = base_url + link
        print_link(title, link)
        if index != len(soup.find_all('h2', class_='teaserTitle')) - 1:
            print() 

scrape_news()
