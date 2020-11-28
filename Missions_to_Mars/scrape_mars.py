from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager




def scrape():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(14)
    abc= soup.find_all('li', class_= 'slide')[0]

    mars_title = ''
    for x in abc:
        test1= x.h3
        mars_title=test1.text
    mars_body = ''
    for x in abc:
        test1= x.find('div', class_='article_teaser_body')
        mars_body=test1.text
    browser.quit()
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url2)


    browser.links.find_by_partial_text('FULL IMAGE').first.click() 
    browser.links.find_by_partial_text('more info').first.click() 
        
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    source ="https://www.jpl.nasa.gov"
    figure = soup2.find_all('figure', class_='lede')
    for y in figure:
        href= y.a['href']
    
    featured_image_url= source + href
    browser.quit()
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    mars_fact_url = 'https://space-facts.com/mars/'
    browser.visit(mars_fact_url)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser') 
    
    
    table = soup3.find_all('table', id='tablepress-p-mars-no-2')

    df = pd.read_html(str(table))[0]
    df1 = df.set_index(0)
    df1.index.name = None
    df1.rename(columns = {1:'Mars'}, inplace = True) 
    html = df1.to_html()
    browser.quit()

    ##Mars Hemispheres
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    mars_Hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_Hemispheres_url)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')

    astro_source= 'https://astrogeology.usgs.gov'


    div_tags = soup4.find_all('div', class_= 'description')

    lista=[]

    for x in div_tags:
        
        h3= x.find('h3')
        
        lista.append(h3.text)

    hemishpere_full=[]
    
    for y in lista:
        browser.find_by_text(y).first.click()
        htmlx = browser.html
        soupx = BeautifulSoup(htmlx, 'html.parser')
        wide_image = soupx.find('div', id= 'wide-image')
        browser.find_by_text('Open').first.click()
        
        
        content=soupx.find('div', class_='content')
        h2 = content.find('h2')
        src_wind_image=  wide_image.find('img')['src']
    
        title = h2.text
        img_url = astro_source + src_wind_image
        hemishpere_full.append({"title" : title,
                                "img_url" : img_url })    
            
        browser.visit(mars_Hemispheres_url)
    browser.quit()
    main_dict={"mars_title" : mars_title,
                "mars_body" : mars_body,
                "featured_image_url": featured_image_url,
                "html": html,
                "hemishpere_full" : hemishpere_full}

    print(main_dict)
    return(main_dict)


    
