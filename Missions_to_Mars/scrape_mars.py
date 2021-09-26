from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}

    # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Mars Space Images 
    nasa_url  =' https://spaceimages-mars.com/'
    browser.visit(nasa_url)

    html = browser.html
    soup = bs(html,"html.parser")
    image_url= soup.find('img', class_='headerimage fade-in')['src'] 

    featured_image_url = nasa_url + image_url

    # Mars Facts 
    url = 'https://galaxyfacts-mars.com/'
    facts_table = pd.read_html(url)
    facts_df = facts_table[1]
    facts_df.columns = ["Category", "Measurement"]
    facts_df = facts_df.set_index("Category")
    