import requests
from bs4 import BeautifulSoup
from hyperlink import URL

def print_link(title, url):
    url = URL.from_text(url)
    print(f'\x1b]8;;{url}\x1b\\{title}\x1b]8;;\x1b\\')

def scrape_bbc_news():
    base_url = "https://www.ctvnews.ca"
    response = requests.get(base_url + "/canada")
    soup = BeautifulSoup(response.text, 'html.parser')

    printed_titles = set()

    for story in soup.find_all('a', class_='c-list__item__link'):
        title = story.text.strip()
        link = story.get('href')
        if link.startswith('https:'):
            full_link = link
        else:
            full_link = base_url + link
        
        if title not in printed_titles:
            print_link(title, full_link)
            printed_titles.add(title)

def scrape_news(source):
    if source == "CP24":
        base_url = "https://www.cp24.com"
        response = requests.get(base_url + "/news")
        soup = BeautifulSoup(response.text, 'html.parser')
    elif source == "CTV News":
        scrape_bbc_news()
        return
    else:
        print("Invalid news source.")
        return

    printed_titles = set()

    for index, story in enumerate(soup.find_all('h2', class_='teaserTitle')):
        title = story.text.strip()
        if title not in printed_titles:
            link = story.find('a')['href']
            if not link.startswith('http'):
                link = base_url + link
            print_link(title, link)
            printed_titles.add(title)
        if index != len(soup.find_all('h2', class_='teaserTitle')) - 1:
            print()  # Add a new line between each link

def scrape_all_news():
    print("Choose a news source:")
    print("1. CP24")
    print("2. CTV News")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        scrape_news("CP24")
    elif choice == '2':
        scrape_news("CTV News")
    else:
        print("Invalid choice. Please enter 1 or 2.")

scrape_all_news()
