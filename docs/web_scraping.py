# import necessary packages
import pandas as pd
from selenium import webdriver

# set browser
driver = webdriver.Edge()

# get rainfall data
driver.get("https://wdo.indiawris.gov.in/api/comm/src/rainfall")