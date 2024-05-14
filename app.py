from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from hyperlink import URL

app = Flask(__name__)

def print_link(title, url):
    url = URL.from_text(url)
    return f'\x1b]8;;{url}\x1b\\{title}\x1b]8;;\x1b\\'

def scrape_news(source):
    if source == "CP24":
        base_url = "https://www.cp24.com"
        response = requests.get(base_url + "/news")
        soup = BeautifulSoup(response.text, 'html.parser')
    elif source == "CTV News":
        base_url = "https://www.ctvnews.ca"
        response = requests.get(base_url + "/canada")
        soup = BeautifulSoup(response.text, 'html.parser')

    news_list = []

    if source == "CTV News":
        for story in soup.find_all('a', class_='c-list__item__link'):
            title = story.text.strip()
            link = story.get('href')
            if not link.startswith('https:'):
                link = base_url + link
            news_list.append((title, link))
    else:
        for story in soup.find_all('h2', class_='teaserTitle'):
            title = story.text.strip()
            link = story.find('a')['href']
            if not link.startswith('http'):
                link = base_url + link
            news_list.append((title, link))

    return news_list



@app.route('/', methods=['GET', 'POST'])
def index():
    selected_source = None
    if request.method == 'POST':
        selected_source = request.form['source']
        news = scrape_news(selected_source)
        return render_template('index.html', news=news, selected_source=selected_source)
    else:
        return render_template('index.html', news=[], selected_source=selected_source)



if __name__ == '__main__':
    app.run(debug=True)
