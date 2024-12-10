
from copy import deepcopy

import pandas as pd
from IPython.display import display, HTML
import json

from pywris.utils.fetch_wris import get_response
from pywris.static_data.state_ids import state_id
from pywris.static_data.request_urls import requests_config

class State:
    def __init__(self, state_name):
        self.state_name = state_name
        self.state_id = self._fetch_state_id()
        self.districts = {}

    def _fetch_state_id(self):
        if self.state_name in state_id.keys():
            return state_id[self.state_name]
        else:
            return None
        
    def fetch_districts(self):
        self.districts = get_districts([self.state_name])

class District(State):
    def __init__(
        self, state_name, district_name=None, code=None, area=None, length=None
    ):
        super().__init__(state_name)
        self.district_name = str(district_name) if district_name is not None else district_name
        self.district_code = int(code) if code is not None else code
        self.district_area = float(area) if area is not None else area
        self.district_length = float(length) if length is not None else length
        self.reservoirs = []
    

class Basin:
    def __init__(self, basin_name, basin_code=None):
        self.basin_name = basin_name
        self.basin_code = basin_code

def get_districts(selected_states):
    """
    Fetches list of districts given state names.
    Parameters:
    """
    
    # Check if selected_states has valid input 
    if selected_states == 'all':
        selected_states = list(state_id.keys())
    elif isinstance(selected_states, list) and all(isinstance(state, str) for state in selected_states):
        check_valid_states(selected_states)
    else:
        raise ValueError("States must be a list of strings or 'all'.")
   
    # Prepare list of state objects
    states = [State(state_name) for state_name in selected_states]
    state_ids = [state.state_id for state in states]
    state_ids_list_str = "%27%2C%27".join(state_ids)
    
    # Fetch district data
    # Get url, payload and method
    url = requests_config["geounits"]["get_districts"]["url"]
    payload = deepcopy(requests_config["geounits"]["get_districts"]["payload"])
    payload = payload.format(state_ids_list_str)
    method = requests_config["geounits"]["get_districts"]["method"]
    # Send request and get response
    json_response = get_response(url, payload, method, "get_districts")
    # Parse response
    if json_response:
        districts_data = pd.json_normalize(json_response["features"])
    else:
        return None
    
    # Prepare dictionary of district objects to return with their names as keys
    districts = {}
    for index, district_row in districts_data.iterrows():
        key = district_row["attributes.district"]
        district_state_id = district_row["attributes.state"]
        district_state_name = state_id.inverse[district_state_id]
        district_code = district_row["attributes.district_code"]
        district_area = district_row["attributes.st_area(shape)"]
        district_length = district_row["attributes.st_length(shape)"]
        district_intance = District(
            district_state_name,
            key,
            district_code,
            district_area,
            district_length,
        )
        districts[key] = district_intance

    return districts

def check_valid_states(selected_states):
    """
    Checks if all selected states are valid.
    """
    valid_states = state_id.keys()
    if isinstance(selected_states, list):
        for state in selected_states:
            if state not in valid_states:
                raise ValueError(f"{state} is not a valid state. List of valid states: {valid_states}.")
    else:
        raise ValueError("States must be a list.")