# setup

## import necessary packages
import pandas as pd
from selenium import webdriver

# set browser
driver = webdriver.Edge()

# get data links from WRIS using devtools

## rainfall
### location
# driver.get("https://wdo.indiawris.gov.in/api/comm/src/rainfall")

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