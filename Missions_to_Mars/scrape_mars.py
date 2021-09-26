from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def init_browser():
    #executable_path = {'executable_path': 'chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    return browser


def scrape():
    browser=init_browser()
    mars_dict={}

    # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    title = soup.find('div', class_='content_title').text
    paragraph = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images 
    nasa_url  =' https://spaceimages-mars.com/'
    browser.visit(nasa_url)

    html = browser.html
    soup = bs(html,"html.parser")
    image_url= soup.find('img', class_='headerimage fade-in')['src'] 

    featured_image_url = nasa_url + image_url

    # Mars Facts 
    facts_url = 'https://galaxyfacts-mars.com/'
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[1]
    facts_df.columns = ["Category", "Measurement"]
    facts_df.set_index("Category", inplace = True)
    fact_table = facts_df.to_html()
    fact_table.replace('\n','')
    
    # Mars Hemisphere
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    html=browser.html
    soup=bs(html,'html.parser')

    titles = soup.find_all("h3")
    for title in titles:
        browser.click_link_by_partial_text("Hemisphere")
        browser.back()

    results = soup.find_all("div", class_="description")
    mars_dict={}
    hemisphere_image_urls=[]
    for result in results:
        link = result.find('a')
        href = link['href']
        title = link.find('h3').text
        url2 = "https://marshemispheres.com/" + href
        hemisphere_image_urls.append({"title":title,"img_url":url2})

    mars_dict={
        "news_title":title,
        "news_p":paragraph,
        "featured_image_url":featured_image_url,
        "mars_table":fact_table,
        "hemisphere_images":hemisphere_image_urls
    }

    browser.quit()
    return mars_dict
    