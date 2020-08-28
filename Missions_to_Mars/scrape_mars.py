#Dependency
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver

#initialyzing the browser
def init_browser():
    #load the crome driver
    executable_path ={'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#scraping   
def scrape():
    Browser = init_browser()    
    #Scraping data from the existing NASA Mars News website 
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text,"html.parser")

    #find latest News Title and Paragraph by beautiful soup
    news_title = soup.find("div", class_= "content_title").find("a").text.strip()
    news_p = soup.find("div", class_= "rollover_description_inner").text.strip()

    #visit the URL for the JPL Featured Space Image by splinter
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)   
    #HTML object and parser
    html_image = browser.html
    soup = bs(html_image, "html.parser")

    #retreieve sub-url for the background image
    featured_image_sub_url = soup.find("div", class_="carousel_items")("article")[0]["style"].replace('background-image: url(','').replace(');','')[1:-1]

    #main existing url
    main_url = "https://www.jpl.nasa.gov"

    #creating full url 
    featured_image_url = main_url + featured_image_sub_url
    featured_image_url
    #visit the Mars Facts web url
    Mars_Facts_url="https://space-facts.com/mars"
    browser.visit(Mars_Facts_url)
    #reading in the tables on the Mars_Facts_url
    tables = pd.read_html(Mars_Facts_url)

    #find the second table contains from "Mars Facts"
    Mars_Facts_raw = tables[1]
    #rename the columns head
    Mars_Facts_raw.columns=["Facts", "Value","Earth"]
    #drop the earth column
    Mars_Facts=Mars_Facts_raw.drop(columns=["Earth"])
    #set Facts column as index
    Mars_Facts.set_index("Facts", inplace=True)
    #convert pandas data to html
    Mars_Facts_htmldata=Mars_Facts.to_html()

    #visit the Mars Hemispheres web url
    Mars_Hem="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Mars_Hem)
    #HTML object and parser
    html_Hem = browser.html
    soup = bs(html_Hem, "html.parser")
    #find the all item 
    Mars_Hem_item=soup.find_all("div", class_="item")
    #declare a list of Hamisphere url list
    Hem_image_url=[]
    # bring the main url 
    Hem_main_url = "https://astrogeology.usgs.gov"
    #use for loop to containg the image link
    for item in Mars_Hem_item:
        #to get the title
        title=item.find("h3").text
        #to get the partial image url
        partial_image_url=item.find("a", class_="itemLink product-item")["href"]
        #visit the both url
        browser.visit(Hem_main_url + partial_image_url)
        #HTML object and parser
        partial_image_html=browser.html
        soup=bs(partial_image_html, "html.parser")
        # to get the  full image url 
        full_image_url = Hem_main_url + soup.find("img", class_="wide-image")["src"]
        #put the data in the list
        Hem_image_url.append({"title":title, "img_url" : full_image_url })

    Mars_Hemispheres_data= {
        "Mars_News_Title": news_title,
        "Mars_News_Paragraph": news_p,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": Mars_Facts_htmldata,
        "Mars_Hemisphere_Images": Hem_image_url
    }
    browser.quit()
    
    return Mars_Hemispheres_data