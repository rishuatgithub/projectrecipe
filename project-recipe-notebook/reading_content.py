#!/usr/bin/env python
# coding: utf-8

# # Project Recipe Notebook
# ### Scrapping Web pages for getting the recipe details
# - Author: Rishu Shrivastava (@rishuatgithub)
# - Last Updated: Sunday May 3, 2020
# #### License: Copyrighted. Rishu Kumar Shrivastava

import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',filename="reading_content_log.log",filemode='w',level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Starting of the Application: reading_content.py")

web_urls=['https://www.jamieoliver.com/recipes/']

def logwarnings(stepname,url):
    return logging.warning(f"Found an issue will parsing url: {url} for the step: {stepname}")

## define the webconnection class to get the content from the website
class WebConnection:
    
    def __init__(self,base_url,url):
        self.base_url = base_url
        if base_url in url: ## if the url contains the base url
            self.url = url
        else:
            self.url = base_url + url
            
        logging.info(f"Parsing web url: {self.url}")
    
    def getresponse(self):
        try:
            response = requests.get(self.url,timeout=10) ## waiting for max timeout = 10 sec for each request

        except requests.exceptions.timeout:
            logging.error(f"Request to server timed-out. Server: {self.url}")

        except requests.exceptions.RequestException:
            logging.error(f"Request to server received some exception. Server: {self.url}")

        return response
    
    def getcontent(self):
        response = self.getresponse()
        content = BeautifulSoup(response.content,features='lxml')
        return content

search_strings = {'l0':'tile-wrapper','l1':'recipe-block','l2':'recipe-block'}
search_title_strings = {'l0':'tile-title','l1':'recipe-title','l2':'recipe-title'}

## parse the website no 1.
def parsingJOWeb():
    
    url = web_urls[0]
    base_url = urljoin(web_urls[0],'/') ## https://jamieoliver.com/
    
    web_parsed_content = {}
    web_parsed_content['levels'] = {}
    
    l1_arr = []
    l2_arr = []
    l3_arr = []
    
    cont = WebConnection(base_url,url).getcontent()
    web_parsed_content['title'] = cont.title.text
    web_parsed_content['parent_url'] = url
    
    ## level 0
    logging.info("Parsing of Level 0 is started")
    l0_block = cont.find_all("div",{'class':search_strings['l0']})
    l0_ahref = [f.find_all("a")[0].get("href") for f in l0_block]
    l0_title = [f.find("div",{'class':search_title_strings['l0']}).text for f in l0_block]
    
    web_parsed_content['levels']['level0'] = {'parent_url':url, 'level':{'title':l0_title,'url':l0_ahref}}
    logging.info("Parsing of Level 0 is complete")

    ## level 1
    logging.info("Parsing of Level 1 is started")
    for l0 in l0_ahref:
        cont_l1 = WebConnection(base_url,l0).getcontent()
        l1_block = cont_l1.find_all("div",{'class':search_strings['l1']})
        l1_ahref = [f.find_all("a")[0].get("href") for f in l1_block]
        l1_title = [f.find("div",{'class':search_title_strings['l1']}).text for f in l1_block]
        l1_arr.append({'parent_url':l0, 'level':{'title':l1_title,'url':l1_ahref}})
        
    web_parsed_content['levels']['level1'] = l1_arr
    logging.info("Parsing of Level 1 is complete")
    
    ## level 2
    logging.info("Parsing of Level 2 is started")
    l1_url_list = [ pcl1['level']['url'] for pcl1 in web_parsed_content['levels']['level1']]
    
    for l1_list in l1_url_list:
        for l1 in l1_list:
            cont_l2 = WebConnection(base_url,l1).getcontent()
            l2_block = cont_l2.find_all("div",{'class':search_strings['l2']})
            l2_ahref = [f.find_all("a")[0].get("href") for f in l2_block]
            l2_title = [f.find("div",{'class':search_title_strings['l2']}).text for f in l2_block]
            #l2_meta = [f.find("div",{'class':'recipe-meta'}).text for f in l1_block]
            l2_arr.append({'parent_url':l1, 'level':{'title':l2_title,'url':l2_ahref}})
    
    web_parsed_content['levels']['level2'] = l2_arr
    logging.info("Parsing of Level 2 is complete")
    
    ## level 3 - final level
    logging.info("Parsing of Level 3 is started")
    l2_url_list = [ pcl2['level']['url'] for pcl2 in web_parsed_content['levels']['level2']]
    
    for l2_list in l2_url_list:
        for l2 in l2_list:
            conn = WebConnection(base_url,l2).getcontent()
            
            if conn.find('div',{'class':'single-recipe-details'}) != None:
                recipe_name = conn.find('div',{'class':'single-recipe-details'}).find('h1').text
            else:
                logwarnings('recipe_name',l2)
                recipe_name = ''
                
            if conn.find('div',{'class':'single-recipe-details'}) != None and conn.find('div',{'class':'single-recipe-details'}).find('p') != None:
                recipe_subtitle = conn.find('div',{'class':'single-recipe-details'}).find('p').text
            else:
                logwarnings('recipe_subtitle',l2)
                recipe_subtitle = ''
            
            if conn.find('div',{'class':'recipe-intro'}) != None:
                recipe_intro = conn.find('div',{'class':'recipe-intro'}).text.strip()
            else:
                logwarnings('recipe_intro',l2)
                recipe_intro = ''
            
            if conn.find('ul',{'class':'special-diets-list'}) != None and conn.find('ul',{'class':'special-diets-list'}).find_all('span',{'class':'full-name'}) != None:
                title_tags = [ title_tags.text.strip() for title_tags in conn.find('ul',{'class':'special-diets-list'}).find_all('span',{'class':'full-name'})]
            else:
                logwarnings('title_tags',l2)
                title_tags = []
            
            if conn.find('div',{'class':'nutrition-expanded'}) != None and  conn.find('div',{'class':'nutrition-expanded'}).find_all('div',{'class':'inner'}) != None:
                nutrition = [ (nut.find('span',{'class':'title'}).text.strip(), nut.find('span',{'class':'top'}).text.strip(), nut.find('span',{'class':'bottom'}).text.strip()) for nut in conn.find('div',{'class':'nutrition-expanded'}).find_all('div',{'class':'inner'})]
            else:
                logwarnings('nutrition',l2)
                nutrition = []
            
            if conn.find('div',{'class':'recipe-detail serves'}) != None:
                servings = conn.find('div',{'class':'recipe-detail serves'}).text.strip()
            else:
                logwarnings('servings',l2)
                servings = ''
               
            if conn.find('div',{'class':'recipe-detail time'}) != None:
                timing = conn.find('div',{'class':'recipe-detail time'}).text.strip().replace('Cooks In','')
            else:
                logwarnings('timing',l2)
                timing = ''
            
            if conn.find('div',{'class':['difficulty']}) != None:
                difficulty = conn.find('div',{'class':['difficulty']}).text.strip().replace('Difficulty','')
            else:
                logwarnings('difficulty',l2)
                difficulty = ''
            
            if conn.find('div',{'class':'tags-list'}) != None and conn.find('div',{'class':'tags-list'}).find_all('a') != None:
                tags_list = [ taglist.text for taglist in conn.find('div',{'class':'tags-list'}).find_all('a')]
            else:
                logwarnings('tags_list',l2)
                tags_list = []
            
            if conn.find("ul",{'class':'ingred-list'}) != None and conn.find("ul",{'class':'ingred-list'}).find_all('li') != None:
                ingrednt = [''.join(t.text.strip().split(' '*11)) for t in conn.find("ul",{'class':'ingred-list'}).find_all('li')]
            else:
                logwarnings('ingredients',l2)
                ingrednt = []
            
            #method = [ (index, meth.text.strip()) for index,meth in enumerate(conn.find('ol',{'class':'recipeSteps'}).find_all('li'))]
            if conn.find('div',{'class':['instructions-wrapper']}) != None and conn.find('div',{'class':['instructions-wrapper']}).find_next().find_next().find_next() != None:
                method = conn.find('div',{'class':['instructions-wrapper']}).find_next().find_next().find_next().text.strip().split('\r\n')
            else:
                logwarnings('method',l2)
                method = []
                
            recipedict = {'recipe_name':recipe_name,'recipie_subtitle':recipe_subtitle,'recipe_intro':recipe_intro,
                          'title_tags':title_tags,'tags_list':tags_list, 'servings':servings, 'timing':timing,
                          'difficulty':difficulty, 'nutrition':nutrition, 'ingredients':ingrednt, 'method':method
                         }
            
            l3_arr.append({'parent_url':l2, 'recipe_details':recipedict})

    web_parsed_content['levels']['level3'] = l3_arr
    logging.info("Parsing of Level 3 is complete")

    return web_parsed_content


data_dict = {'data': parsingJOWeb() }  # wrap everything into a dict

#### Save to a file locally
## save to a file 

import json
fname = 'jamieoliverdata.json'

logging.info(f"Writing the dictionary to the file: {fname} started.")

with open(fname,"w") as file:
    file.write(json.dumps(data_dict))

logging.info(f"Writing the dictionary to the file: {fname} is complete.")


logging.info("====== Scrapping Data from Website Completed. =========")


