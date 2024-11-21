def get_data():
    '''
    Get the data from the reservoir
    parameters:
    '''

import requests

# get the url
url = "https://indiawris.gov.in/resdnlddata"

# user-defined parameters for post request
start_date = "2000-09-01"
end_data = "2024-10-11"
reservoir_name = "Idukki Reservoir"