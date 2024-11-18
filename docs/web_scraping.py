# setup

## import necessary packages
import pandas as pd
import subprocess as sp
from selenium import webdriver
from selenium.webdriver.edge.service import Service
# from selenium.webdriver.common.keys import keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
#from selenium.common.exceptions import TimeoutException

# driver code

## create service object
#edgeService = Service(
#   "mnt/c/Users/ishaa/Downloads/edgedriver_win64/msedgedriver" 
#)

## create webdriver object
#edgeDriver = webdriver.Edge(service = edgeService)

# testing
#System.setProperty("webdriver.edge.driver", "C:\Users\ishaa\Downloads\edgedriver_win64\msedgedriver.exe")

# set browser
#driver = webdriver.Edge(executable_path = "C:\\Users\\ishaa\\Downloads\\edgedriver_win64\\msedgedriver.exe")

#driver = webdriver.Edge(service = Service(EdgeChromiumDriverManager().install(), service_args = ['--log-level=DEBUG'], log_output = sp.STDOUT))
#service = webdriver.EdgeService(EdgeChromiumDriverManager().install())
service = webdriver.EdgeService()

driver = webdriver.Edge(service=service)

# get data links from WRIS using devtools

## rainfall
### location
driver.get("http://www.python.org")
#timeout = 3
#try:
#    element_present = EC.presence_of_element_located((By.ID, 'main'))
#    WebDriverWait(driver, timeout).until(element_present)
#except TimeoutException:
#    print("Timed out waiting for page to load")
#finally:
#    print("Page loaded")
driver.quit()
#driver.get("https://wdo.indiawris.gov.in/api/comm/src/rainfall")

### table
#https://wdo.indiawris.gov.in/api/rf/rfTable

### chart
#https://wdo.indiawris.gov.in/api/rf/rfChart

## river authority
### location
#https://wdo.indiawris.gov.in/api/comm/src/River%20Authority

### table
#https://wdo.indiawris.gov.in/api/riverpoints/table

### gis
#https://wdo.indiawris.gov.in/api/riverpoints/gis

## groundwater
### location
#https://wdo.indiawris.gov.in/api/comm/src/groundwater

### table
#https://wdo.indiawris.gov.in/api/gw/gwTable

### chart
#https://wdo.indiawris.gov.in/api/gw/gwChart

## reservoir
### business
#https://indiawris.gov.in/getReservoirBusinessData

### date chart
#https://indiawris.gov.in/getReservoirDateChartData

### state chart
#https://indiawris.gov.in/getReservoirStateChartData