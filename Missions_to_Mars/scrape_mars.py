from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}

    ### NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text