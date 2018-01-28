
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import time
import pandas as pd
import os

def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome",**executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # Latest News
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'html.parser')


    latest_title=soup.find('div', class_='content_title').text.strip()
    
    latest_description= soup.find('div', class_="rollover_description_inner").text.strip()
   
    mars_data['latest_title'] = latest_title
    mars_data['latest_description'] = latest_description


### Mars Image
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit'

    browser.visit(url)
    time.sleep(3)  #allow time for page to load

    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(html, 'html.parser')

    #click full image button for feature picture on landing page(to second page)
    browser.find_by_css("div.carousel_container div.carousel_items a.button").first.click()

    time.sleep(3)  #allow time for page to load


    #read in second page to beautifulsoup
    html = browser.html
    soup = bs(html,'html.parser')

    #to third page
    get_full_img = browser.find_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').first.click()

    time.sleep(3)  #allow time for page to load

    #get large image
    large_image_url = browser.find_by_xpath('//*[@id="page"]/section[1]/div/article/figure/a/img')["src"]
    
    mars_data['featured_image'] = large_image_url


# ### Mars weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)
    time.sleep(3)  #allow time for page to load

    # Retrieve page 
    html = browser.html
    # Create BeautifulSoup object; parse with 'html'
    soup = bs(html, 'html.parser')
  
    #this is p tag looking for, but not for tweets with image
    current_weather=soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_data['weather'] = current_weather


# ### Mars facts

    url_table = 'https://space-facts.com/mars/'
    table =  pd.read_html(url_table)


    # create pandas DF
    mars_table = table[0]
    mars_table.columns = ["Parameter", "Values"]
    mars_table.set_index(["Parameter"])


    #convert pandas DF to HTML file
    mars_html_table = mars_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data['table'] = mars_html_table


    