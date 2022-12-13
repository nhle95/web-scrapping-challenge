from email import header
from operator import index
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit redplanetscience
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #visit spaceimages
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)

    # Scrape page into Soup
    html2 = browser.html
    soup2 = BeautifulSoup(html2,'html.parser')

    #visist galaxyfacts
    url3 = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url3)
            
    #NASA MARS NEWS

    # collect the latest title
    latest_title = soup.find_all("div",class_="content_title")[0].text
    #collect the latest news paragraph 
    latest_para = soup.find_all("div",class_="article_teaser_body")[0].text


    #JPL Mars Space Images - Featured Image

    # collect the latest image
    image =soup2.find("img", class_="headerimage")
    featured_image_url = "https://spaceimages-mars.com/" + image['src']

    #Mars Facts
    
    # collect the table
    df = tables[0]
    #rename columns header
    df.columns =['Description', 'Mars', 'Earth']
    #drop the first row
    df = df.iloc[1: , :]
        
    # save as HTML
    table = df.to_html(index=False,header=False, classes = "table table-sm table-striped" )
    
    
    #Mars Hemispheres

    # visit Mars Hemispheres 
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)
    marshemispheres_html = browser.html
    soup = BeautifulSoup(marshemispheres_html, 'html.parser')
    divs =soup.find_all("div", class_="item")
    hemisphere_image_urls = []
    
    titles = []
    img_urls = []
    for div in range(len(divs)):
        titles.append(divs[div].h3.text)
        img_urls.append("https://marshemispheres.com/" + divs[div].img["src"])

    hemisphere_image_urls = []
    for title, img_url in zip(titles,img_urls):
        hemisphere_image_url = {'title':title,'img_url':img_url}
        hemisphere_image_urls.append(hemisphere_image_url)
    
    

   # Store data in a dictionary
    mars_data = {
        "mars_img": featured_image_url,
        "news_title": latest_title,
        "news_p": latest_para,
        "table":table, 
        "hemisphere_images_urls": hemisphere_image_urls

    }   

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data