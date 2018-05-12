
# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time


# Set up Chromedriver
executable_path = {"executable_path": "/Users/AJ/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# URLs to Scrape
img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
twitter_url = "https://twitter.com/marswxreport?lang=en" 
space_facts = "https://space-facts.com/mars/" 
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" 

# Defining scrape & dictionary
def scrape():
    mars = {}
    output = News()
    mars["newsm"] = output[0]
    mars["paragraphm"] = output[1]
    mars["imagem"] = Image()
    mars["weatherm"] = Weather()
    mars["factsm"] = Facts()
    mars["hemispherem"] = Hemi()
    return mars


# NASA Mars News Browser
def News():
    news = "https://mars.nasa.gov/news/" 
    browser.visit(news)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    # print(news_title)
    # print(news_p)
    return output


# JPL Mars Space Images - Find by id (CSS)
def Image():
    browser.visit(img)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    #print(featured_image_url)
    return featured_image_url


# Mars Weather from Twitter
def Weather():
    browser.visit(twitter_url)
    time.sleep(1)
    html_mars = browser.html
    soup_mars = BeautifulSoup(html_mars, "html.parser")

    tweet = soup_mars.find("ol", class_="stream-items")
    weather_m = tweet.find("p", class_="tweet-text").text
    #print(weather_m)
    return weather_m

# Mars Facts
def Facts():
    browser.visit(space_facts)
    facts_m = pd.read_html(space_facts)
    facts_m = pd.DataFrame(facts_m[0])
    facts_m.columns = ["Description", "Value"]
    facts_m = facts_m.set_index("Description")
    facts_m2 = facts_m.to_html(header = False, index = False)
    #print(facts_m2)
    return facts_m


# Mars Hemispheres
def Hemi():
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemi = []

    products = soup.find("div", class_ = "result-list" )
    hemis = products.find_all("div", class_="item")

    for hem in hemis:
        title = hem.find("h3").text
        title = title.replace("Enhanced", "")
        end = hem.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + end    
        browser.visit(img_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        img = downloads.find("a")["href"]
        mars_hemi.append({"title": title, "img_url": img})
    return mars_hemi



