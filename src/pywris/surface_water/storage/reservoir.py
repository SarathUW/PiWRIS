from copy import deepcopy

import pandas as pd

from pywris.utils.fetch_wris import get_response
from pywris.static_data.state_ids import state_id
from pywris.static_data.request_urls import requests_config
import pywris.geo_units.components as geo_components


class Reservoir:
    def __init__(self, reservoir_name, state, district=None):
        self.reservoir_name = reservoir_name
        self.state = geo_components.State(state)
        self.district = geo_components.District(state)
        self.frl = None
        self.live_cap_frl = None
        self.agency = None
        self.data = None

    def fetch_data(self):
        pass
    
    def plot():
        pass


def get_reservoirs(
    end_date,
    start_date='1991-01-01',
    timestep='Daily',
    selected_states=None,
    selected_districts="all",
    selected_basins=None,
    selected_reservoirs="all",
):
    """
    Fetches list of reservoirs given district name.
    Parameters:
    """

    # Check if selected_states has valid input
    if selected_states == "all":
        selected_states = list(state_id.keys())
    elif isinstance(selected_states, list) and all(
        isinstance(state, str) for state in selected_states
    ):
        geo_components.check_valid_states(selected_states)
    else:
        raise ValueError("States must be a list of strings or 'all'.")

    # Prepare list of state ids
    states_list_str = ",".join(["'" + state + "'" for state in selected_states])

    # Check if selected_districts has valid input
    district_dict = geo_components.get_districts(selected_states)
    if selected_districts == "all":
        selected_districts = list(district_dict.keys())
    elif isinstance(selected_districts, list) and all(
        isinstance(state, str) for state in selected_districts
    ):
        for district in selected_districts:
            if district not in district_dict.keys():
                raise ValueError(f"{district} is not a valid district.")
            else:
                pass
    else:
        raise ValueError("Districts must be a list of strings or 'all'.")

    # Prepare list of ditrict names
    district_names_list_str = ",".join(
        ["'" + district + "'" for district in selected_districts]
    )

    # Fetch reservoir names data
    reservoir_list = get_reservoir_names(states_list_str, district_names_list_str)
    reservoir_list = [item for sublist in reservoir_list for item in sublist]

    # Check if selected_reservoirs has valid input
    if selected_reservoirs == "all":
        selected_reservoirs = reservoir_list
    elif isinstance(selected_reservoirs, list) and all(
        isinstance(state, str) for state in selected_reservoirs
    ):
        for reservoir in selected_reservoirs:
            if reservoir not in reservoir_list:
                raise ValueError(f"{reservoir} is not a valid reservoir.")
            else:
                pass
    else:
        raise ValueError("Reservoirs must be a list of strings or 'all'.")

    # Fetch reservoir valid dates and check if user provided valid dates
    reservoir_data_valid_date_range = get_reservoir_data_valid_date_range()
    check_valid_date_range(start_date, end_date, reservoir_data_valid_date_range)
    
    # Fetch reservoir time series data
    reservoir_names_str = ",".join(["'" + reservoir + "'" for reservoir in selected_reservoirs])
    reservoir_data = get_reservoir_data(reservoir_names_str, timestep, start_date, end_date)
    reservoir_df = pd.json_normalize(reservoir_data)
    # Create dictionary of reservoir objects 
    reservoirs = {}
    for res_name in selected_reservoirs:
        sel_res_df = reservoir_df[reservoir_df['Reservoir Name']==res_name]
        sel_res_state = sel_res_df['Parent']
        
        sel_res = Reservoir(res_name, sel_res_state)
        sel_res.district = district_dict[sel_res_df['Child']]
        sel_res.frl = sel_res_df['FRL'].unique()[-1]
        sel_res.live_cap_frl = sel_res_df['Live Cap FRL'].unique()[-1]
        sel_res.agency = sel_res_df['Agency Name'].unique()[-1]
        sel_res.data = sel_res_df[['Date','Level','Current Live Storage']]
        sel_res.data['Date'] = pd.to_datetime(sel_res.data['Date'])
        
        reservoirs[res_name] = sel_res
    
    return reservoirs

def get_reservoir_names(states_list_str,district_names_list_str):    
    url = requests_config["reservoir"]["get_reservoir_names"]["url"]
    # Create a copy of the payload to avoid modifying the original
    payload = deepcopy(requests_config["reservoir"]["get_reservoir_names"]["payload"])
    payload["stnVal"]["qry"] = payload["stnVal"]["qry"].format(
     states_list_str, district_names_list_str
    )
    method = requests_config["reservoir"]["get_reservoir_names"]["method"]
    reservoir_names = get_response(url, payload, method)
    return reservoir_names

def get_reservoir_data_valid_date_range():
    url = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["url"]
    payload = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["payload"]
    method = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["method"]
    reservoir_data_valid_date_range = get_response(url, payload, method)
    return reservoir_data_valid_date_range[0]

def get_reservoir_data(reservoir_names_str, timestep, start_date, end_date):
    url = requests_config["reservoir"]["get_reservoir_data"]["url"]
    payload = deepcopy(requests_config["reservoir"]["get_reservoir_data"]["payload"])
    payload["stnVal"]["Reservoir"] = payload["stnVal"]["Reservoir"].format(reservoir_names_str)
    payload["stnVal"]["Timestep"] = payload["stnVal"]["Timestep"].format(timestep)
    payload["stnVal"]["Startdate"] = payload["stnVal"]["Startdate"].format(start_date)
    payload["stnVal"]["Enddate"] = payload["stnVal"]["Enddate"].format(end_date)
    method = requests_config["reservoir"]["get_reservoir_data"]["method"]
    reservoir_data = get_response(url, payload, method)
    return reservoir_data

def check_valid_date_range(start_date, end_date, valid_date_range):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    valid_start_date = pd.to_datetime(valid_date_range[0])
    valid_end_date = pd.to_datetime(valid_date_range[1])
    if start_date < valid_start_date or end_date > valid_end_date:
        raise ValueError(
            f"Invalid date range. Valid date range is {valid_start_date} to {valid_end_date}."
        )
    if start_date > end_date:
        raise ValueError("Invalid date range. Start date must be before end date.")