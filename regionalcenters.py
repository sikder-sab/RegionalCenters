import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import threading
import re
from datetime import datetime, timedelta
import requests
import http.client
import json
import os
import openpyxl
from openpyxl import Workbook
import argparse
import sys

def checkURLAndGetCode(webDriver):
	currentURL = webDriver.current_url
	print(currentURL)
	if "address=" in currentURL:
		print("Getting the health districts' name...")
		healthDistrict = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[7]/td[3]/table/tbody/tr[2]/td/div").text
		# regexQuery = "(code)=(\\w*)&"
		# regexSearch = re.search(regexQuery, currentURL)
		# code = regexSearch.group(2)
		healthDistrictText = healthDistrict.split(':')[1].lstrip()
		webDriver.close()
		return healthDistrictText
	elif "&scope" in currentURL:
		time.sleep(3)
		allowAuthorize = driver.find_element_by_name("commit")
		allowAuthorize.click()
		return checkURLAndGetCode(webDriver)
	else:
		return None

def healthDistrictScraper(driver, address):
	healthDistrictURL = "https://appcenter.gis.lacounty.gov/districtlocator/"
	driver.get(healthDistrictURL)

	#find html elements
	addressField = driver.find_element_by_id("txtAddress")
	searchButton = driver.find_element_by_id("ibtSearch")

	#start URL listener
	addressField.send_keys(address)
	searchButton.click()

	healthDistrict = checkURLAndGetCode(driver)
	if healthDistrict is None:
		healthDistrict = checkURLAndGetCode(driver)

	#return data
	return healthDistrict

def regionalDistrictScraper(address):
	query = address 
	url = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=37802734-7024-4ef5-8754-95f9853d92f4&limit=100&q=' + query
	fileobj = requests.get(url)
	response_dict = json.loads(fileobj.text)

	print("Getting the name of the regional center...")

	resultsArray = response_dict["result"]["records"]

	correctRegionalCenter = {}
	for regionalCenter in resultsArray:
		print("parsing...")
		LAserved = regionalCenter["Los Angeles Health District Served"]
		if LAserved == address:
			correctRegionalCenter = regionalCenter
			break

	return correctRegionalCenter

# -------------------------- start code --------------------------------------


user_input = raw_input("What is the address: ")
address = user_input

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options) 

healthDistrict = healthDistrictScraper(driver,address)

if healthDistrict == None:
	print("Error, please check your address")
else:
	realRegionalCenter = regionalDistrictScraper(healthDistrict)
	realRegionalCenterPretty = json.dumps(realRegionalCenter , indent=2)
	centerName = realRegionalCenter["Regional Center"]
	print(realRegionalCenterPretty)
	print(centerName)

driver.close()

