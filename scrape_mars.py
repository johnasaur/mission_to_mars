
# Import Dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import tweepy

# Set up Chromedriver
def init_browser():
    exec_path = {"executable_path": "/Users/AJ/Downloads/chromedriver"}
    return Browser("chrome", **exec_path, headless=True)


# URLs to Scrape
news = "https://mars.nasa.gov/news/" 
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
twitter_url = "https://twitter.com/marswxreport?lang=en" 
space_facts = "https://space-facts.com/mars/" 
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" 


# NASA Mars News - Find News by CSS | http://splinter.readthedocs.io/en/latest/finding.html
browser = init_browser()
browser.visit(news)
news_title = browser.find_by_css(".content_title").first.text
news_p = browser.find_by_css(".article_teaser_body").first.text
print(news_title, "\n" + news_p)


# JPL Mars Space Images - Find by id (CSS)
browser = init_browser()
browser.visit(image_url)
browser.find_by_id("full_image").click()
featured_image_url = browser.find_by_css(".fancybox-image").first["src"]
print(featured_image_url)


# Mars Weather from Twitter
browser.visit(twitter_url)
mars_weather_html = browser.html
mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

tweets = mars_weather_soup.find('ol', class_='stream-items')
mars_weather = tweets.find('p', class_="tweet-text").text
print(mars_weather)


# Mars Facts
df_mars = pd.read_html(space_facts, attrs = {"id": "tablepress-mars"})[0]
df_mars = df_mars.set_index(0).rename(columns={1:"value"})
mars_facts = df_mars.to_html()
print(mars_facts)


# Mars Hemisperes
browser = init_browser()
browser.visit(hemi_url)

one = browser.find_by_tag("h3")[0].text
two = browser.find_by_tag("h3")[1].text
three = browser.find_by_tag("h3")[2].text
four = browser.find_by_tag("h3")[3].text

browser.find_by_css(".thumb")[0].click()
img1 = browser.find_by_text("Sample")["href"]
browser.back()

browser.find_by_css(".thumb")[1].click()
img2 = browser.find_by_text("Sample")["href"]
browser.back()

browser.find_by_css(".thumb")[2].click()
img3 = browser.find_by_text("Sample")["href"]
browser.back()

browser.find_by_css(".thumb")[3].click()
img4 = browser.find_by_text("Sample")["href"]

hemisphere_image_url = [
    {"title": one, "img_url": img1},
    {"title": two, "img_url": img2},
    {"title": three, "img_url": img3},
    {"title": four, "img_url": img4}
]

print(hemisphere_image_url)

