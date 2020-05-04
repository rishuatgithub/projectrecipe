#!/usr/bin/env python
# coding: utf-8

# # Project Recipe Notebook - Parallel Processing
# ### Scrapping Web pages for getting the recipe details
# - Author: Rishu Shrivastava (@rishuatgithub)
# - Last Updated: Sunday May 4, 2020
# #### License: Copyrighted. Rishu Kumar Shrivastava

import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import logging
import multiprocessing
from multiprocessing import Pool
from multiprocessing import cpu_count
import json
import os

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',filename="reading_content_log.log",filemode='w',level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

web_urls=['https://www.jamieoliver.com/recipes/']
search_strings = {'l0':'tile-wrapper','l1':'recipe-block','l2':'recipe-block'}
search_title_strings = {'l0':'tile-title','l1':'recipe-title','l2':'recipe-title'}
web_parsed_content = {}
web_parsed_content['levels'] = {}
url = web_urls[0]
base_url = urljoin(web_urls[0],'/') ## https://jamieoliver.com/
total_cpu_count = multiprocessing.cpu_count()

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


### parsing the website no 1. - Jamie Oliver
# Level 0
def parsingJOWebL0():
    logging.info("Parsing of Level 0 is started")
    cont = WebConnection(base_url,url).getcontent()
    web_parsed_content['title'] = cont.title.text
    web_parsed_content['parent_url'] = url

    l0_block = cont.find_all("div",{'class':search_strings['l0']})
    l0_ahref = [f.find_all("a")[0].get("href") for f in l0_block]
    l0_title = [f.find("div",{'class':search_title_strings['l0']}).text for f in l0_block]
    
    web_parsed_content['levels']['level0'] = {'parent_url':url, 'level':{'title':l0_title,'url':l0_ahref}}
    logging.info("Parsing of Level 0 is complete")
    print(web_parsed_content['levels']['level0']['level']['url'])
    return web_parsed_content

# Level 1
def parsingJOWebL1(webcontentL0):
    l1_arr = []
    
    logging.info("Parsing of Level 1 is started")
    for l0 in webcontentL0['levels']['level0']['level']['url']:
        cont_l1 = WebConnection(base_url,l0).getcontent()
        l1_block = cont_l1.find_all("div",{'class':search_strings['l1']})
        l1_ahref = [f.find_all("a")[0].get("href") for f in l1_block]
        l1_title = [f.find("div",{'class':search_title_strings['l1']}).text for f in l1_block]
        l1_arr.append({'parent_url':l0, 'level':{'title':l1_title,'url':l1_ahref}})
        
    web_parsed_content['levels']['level1'] = l1_arr
    logging.info("Parsing of Level 1 is complete")

    return web_parsed_content

# Level 2
def parsingJOWebL2(webcontentL1):
    l2_arr = []

    logging.info("Parsing of Level 2 is started")
    l1_url_list = [ pcl1['level']['url'] for pcl1 in webcontentL1['levels']['level1']]
    
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

    return web_parsed_content

# Level 3 (Final Level)
def parsingJOWebL3(webcontentL2):
    l3_arr = []

    logging.info("Parsing of Level 3 is started")
    l2_url_list = [ pcl2['level']['url'] for pcl2 in webcontentL2['levels']['level2']]
    
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

    return web_parsed_content  ## returning the full final content


def savetofile(data_dict,level):
    fname = 'jamieoliverdata_'+level+'.json'
    logging.info(f"Writing the dictionary to the file: {fname} started.")

    with open(fname,"w") as file:
        file.write(json.dumps(data_dict))
    
    logging.info(f"Writing the dictionary to the file: {fname} is complete.")

def readfromfile(level):
    fname = 'jamieoliverdata_'+level+'.json'
    logging.info(f"Reading from the file: {fname} started.")

    with open(fname,'r') as file: 
        data = json.load(file)

    logging.info(f"Reading from the file: {fname} completed.")
    return data 

def checkiffileexists(level): 
    fname = 'jamieoliverdata_'+level+'.json'
    isexits = os.path.isfile(fname)
    logging.info(f"checking if the file : {fname} exists. Result: {isexits}")
    return isexits


def mainjob(): 

    if checkiffileexists('l0'): 
        data_dictL0 = readfromfile('l0') ## read from file instead of scrapping again
    else:
        data_dictL0 = {'data': parsingJOWebL0() }
        savetofile(data_dictL0, 'l0')
    
    if checkiffileexists('l1'):
        data_dictL1 = readfromfile('l1')
    else: 
        data_dictL1 = {'data': parsingJOWebL1(data_dictL0['data']) }
        savetofile(data_dictL1, 'l1')

    if checkiffileexists('l2'):
        data_dictL2 = readfromfile('l2')
    else: 
        data_dictL2 = {'data': parsingJOWebL2(data_dictL1['data']) }
        savetofile(data_dictL2, 'l2')

    if not checkiffileexists('l3'):
        data_dictL3 = {'data': parsingJOWebL3(data_dictL2['data']) }
        savetofile(data_dictL3, 'l3')

    #with Pool(total_cpu_count) as p: 
    #    data_dictL1 = {'data': p.map(parsingJOWebL1,data_dictL0['data']) }
    #    savetofile(data_dictL1, 'l1')


if __name__ == '__main__': 
    logging.info("Starting of the Application: reading_content.py")
    mainjob()
    logging.info("====== Scrapping Data from Website Completed. =========")


