from copy import deepcopy

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pywris.utils.fetch_wris import get_response
from pywris.static_data.state_ids import state_id
from pywris.static_data.request_urls import requests_config
from pywris.visualization.plot import plot_data
import pywris.geo_units.components as geo_components


class Reservoir:
    def __init__(self, reservoir_name, state, district=None):
        self.reservoir_name = reservoir_name
        self.dam_code = None
        self.latitude = None
        self.longitude = None
        self.state = geo_components.State(state)
        self.district = geo_components.District(state)
        self.block_name = None
        self.basin = None
        self.sub_basin_name = None
        self.agency = None
        self.frl = None
        self.live_cap_frl = None
        self.data = None
        
    def fetch_data(self):
        pass

    def plot(self, **args):
        """
        Plots timeseries of the reservoir data
        
        Parameters:
        - **args: Arguments that will be passed to the general plot function
        """
        plot_data(self, **args)


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
    Fetches a list of reservoir objects based on specified filters and returns detailed information including time series data.

    Parameters:
    ----------
    end_date : str
        The end date of the data to fetch, in the format 'YYYY-MM-DD'.
    start_date : str, optional
        The start date of the data to fetch, in the format 'YYYY-MM-DD' (default is '1991-01-01').
    timestep : str, optional
        The temporal resolution of the data (Acceptable values are 'Daily', 'Monthly' or 'Yearly'). Default is 'Daily'.
    selected_states : list of str or "all", optional
        List of state names to filter reservoirs. Use "all" to include reservoirs from all states. It is required when selected_basins is None.
    selected_districts : list of str or "all", optional
        List of district names to filter reservoirs. Use "all" to include reservoirs from all districts.
    selected_basins : list of str or None, optional
        List of basin names to filter reservoirs. It is required when selected_states is None.
    selected_reservoirs : list of str or "all", optional
        List of reservoir names to fetch. Use "all" to include all reservoirs within the filtered states and districts.

    Returns:
    -------
    dict
        A dictionary of reservoir objects keyed by reservoir names. Each reservoir object contains metadata (e.g., location, state, basin)
        and time series data (e.g., water level, live storage) for the specified date range and timestep.

    Raises:
    ------
    ValueError
        - If `selected_states` is not a list of strings or "all".
        - If `selected_districts` is not a list of strings or "all".
        - If `selected_reservoirs` is not a list of strings or "all".
        - If any of the provided states, districts, or reservoirs are invalid.

    Notes:
    ------
    - If "all" is used for `selected_states` or `selected_districts`, it fetches all corresponding entries.

    Example:
    --------
    Fetch reservoirs in a specific state and district:
    >>> reservoirs = get_reservoirs(
            end_date='2024-12-01',
            selected_states=['Kerala'],
            selected_districts=['Wayanad'],
            timestep='Daily'
        )

    Access metadata and time series for a specific reservoir:
    >>> res = reservoirs['Krishna Reservoir']
    >>> print(res.latitude, res.longitude)
    >>> print(res.data.head())
    """
    
    # Check if timestep is valid
    if timestep not in ["Daily", "Monthly", "Yearly"]:
        raise ValueError("Timestep must be 'Daily', 'Monthly' or 'Yearly'.")
    else:
        pass
    
    # Initialize flag to indicate whether all states are selected
    selection_all_states = False
    
    # Check if selected_states has valid input
    if selected_states == "all":
        selected_states = list(state_id.keys())
        selection_all_states = True
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
    
    # Fetch reservoir attributes (primarily latitute and longitude)
    reservoir_names_str = ",".join(["'" + reservoir + "'" for reservoir in selected_reservoirs])
    reservoir_info = get_reservoir_info(reservoir_names_str, selection_all_states)
    if reservoir_info:
        if 'features' in reservoir_info.keys():
            reservoir_info_df = pd.json_normalize(reservoir_info['features'])
        else:
            reservoir_info_df = None
    else:
        reservoir_info_df = None

    # Fetch reservoir valid dates and check if user provided valid dates
    reservoir_data_valid_date_range = get_reservoir_data_valid_date_range()
    check_valid_date_range(start_date, end_date, reservoir_data_valid_date_range)
    
    # Fetch reservoir time series data
    reservoir_data = get_reservoir_data(reservoir_names_str, timestep, start_date, end_date)
    if reservoir_data:
        reservoir_data_df = pd.json_normalize(reservoir_data)
    else:
        return None
    # return reservoir_data_df
    # Create dictionary of reservoir objects 
    reservoirs = {}
    for res_name in selected_reservoirs:
        if res_name in reservoir_info_df['attributes.station_name'].unique():
            sel_res_info_df = reservoir_info_df[reservoir_info_df['attributes.station_name']==res_name]
            sel_res_state = sel_res_info_df['attributes.state_name'].unique()[-1]
            sel_res = Reservoir(res_name, sel_res_state)
            sel_res.latitude = sel_res_info_df['attributes.lat'].unique()[-1]
            sel_res.longitude = sel_res_info_df['attributes.long'].unique()[-1]
            sel_res.agency = sel_res_info_df['attributes.agency_name'].unique()[-1]
            sel_res.dam_code = sel_res_info_df['attributes.dam_code'].unique()[-1]
            sel_res.frl = sel_res_info_df['attributes.frl'].unique()[-1]
            sel_res.live_cap_frl = sel_res_info_df['attributes.lsc_frl'].unique()[-1]
            sel_res.block_name = sel_res_info_df['attributes.block_name'].unique()[-1]
            basin_name = sel_res_info_df['attributes.basin_name'].unique()[-1]
            basin_code = sel_res_info_df['attributes.basin_code'].unique()[-1]
            sel_res.basin = geo_components.Basin(basin_name, basin_code)
            sel_res.sub_basin_name = sel_res_info_df['attributes.sub_basin_name'].unique()[-1]
            sel_res.sub_basin_name = sel_res_info_df['attributes.sub_basin_name'].unique()[-1] 
        else:
            sel_res = Reservoir(res_name, None)

        if res_name in reservoir_data_df['Reservoir Name'].unique():
            sel_res_data_df = reservoir_data_df[reservoir_data_df['Reservoir Name']==res_name]
            sel_res.data = sel_res_data_df[['Date','Level','Current Live Storage']]
            sel_res.data['Date'] = pd.to_datetime(sel_res.data['Date'])
            sel_res.district = district_dict[sel_res_data_df['Child'].unique()[-1]]
        else:
            pass
        
        reservoirs[res_name] = sel_res
        
        # Return the comined dataframe as well
        reservoir_data_df_drop_dl  = reservoir_data_df.drop_duplicates(subset=['Reservoir Name'],keep='last')
        reservoir_combined_df = reservoir_info_df.merge(reservoir_data_df_drop_dl, how='left', left_on='attributes.station_name', right_on='Reservoir Name')
        # Rename columns names to attribute names
        
    return reservoirs, reservoir_combined_df

def get_reservoir_names(states_list_str,district_names_list_str):
    """
    Fetches reservoir names based on the provided states and districts.

    Parameters:
    ----------
    states_list_str : str
        Comma-separated state names, formatted with single quotes (e.g., "'Karnataka','Maharashtra'").
    district_names_list_str : str
        Comma-separated district names, formatted with single quotes (e.g., "'Bangalore Rural','Pune'").

    Returns:
    -------
    list
        A nested list of reservoir names corresponding to the specified states and districts.
    """    
    url = requests_config["reservoir"]["get_reservoir_names"]["url"]
    # Create a copy of the payload to avoid modifying the original
    payload = deepcopy(requests_config["reservoir"]["get_reservoir_names"]["payload"])
    payload["stnVal"]["qry"] = payload["stnVal"]["qry"].format(
     states_list_str, district_names_list_str
    )
    method = requests_config["reservoir"]["get_reservoir_names"]["method"]
    reservoir_names = get_response(url, payload, method, "get_reservoir_names")
    return reservoir_names

def get_reservoir_data_valid_date_range():
    """
    Fetches the valid date range for reservoir data availability.

    Returns:
    -------
    list
        A list containing the start and end date strings of valid data availability.
    """
    url = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["url"]
    payload = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["payload"]
    method = requests_config["reservoir"]["get_reservoir_data_valid_date_range"]["method"]
    reservoir_data_valid_date_range = get_response(url, payload, method, "get_reservoir_data_valid_date_range")
    return reservoir_data_valid_date_range[0]

def get_reservoir_data(reservoir_names_str, timestep, start_date, end_date):
    """
    Fetches time-series data for specified reservoirs within a given date range.

    Parameters:
    ----------
    reservoir_names_str : str
        Comma-separated reservoir names, formatted with single quotes (e.g., "'Reservoir1','Reservoir2'").
    timestep : str
        The desired time interval for the data. Acceptable values are 'Daily', 'Monthly', or 'Yearly'.
    start_date : str
        The start date for the data range in 'YYYY-MM-DD' format.
    end_date : str
        The end date for the data range in 'YYYY-MM-DD' format.

    Returns:
    -------
    list of dict
        A list where each element is a dictionary containing time-series data for a reservoir.
    """
    url = requests_config["reservoir"]["get_reservoir_data"]["url"]
    payload = deepcopy(requests_config["reservoir"]["get_reservoir_data"]["payload"])
    payload["stnVal"]["Reservoir"] = payload["stnVal"]["Reservoir"].format(reservoir_names_str)
    payload["stnVal"]["Timestep"] = payload["stnVal"]["Timestep"].format(timestep)
    payload["stnVal"]["Startdate"] = payload["stnVal"]["Startdate"].format(start_date)
    payload["stnVal"]["Enddate"] = payload["stnVal"]["Enddate"].format(end_date)
    method = requests_config["reservoir"]["get_reservoir_data"]["method"]
    reservoir_data = get_response(url, payload, method, "get_reservoir_data")
    return reservoir_data

def check_valid_date_range(start_date, end_date, valid_date_range):
    """
    Validates the user-provided date range against the allowed date range.

    Parameters:
    ----------
    start_date : str or pd.Timestamp
        The start date for the data range in 'YYYY-MM-DD' format or as a Timestamp.
    end_date : str or pd.Timestamp
        The end date for the data range in 'YYYY-MM-DD' format or as a Timestamp.
    valid_date_range : list or tuple
        A list or tuple containing two elements: the valid start and end dates as strings or Timestamps.

    Raises:
    ------
    ValueError
        If the start or end date is outside the valid date range or if the start date is after the end date.

    Notes:
    ------
    - Converts all inputs to `pd.Timestamp` for comparison.
    """
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
    
def get_reservoir_info(reservoir_name_str, selection_all=False):
    """
    Fetches detailed information for the specified reservoirs.

    Parameters:
    ----------
    reservoir_name_str : str
        Comma-separated reservoir names, formatted with single quotes (e.g., "'Reservoir1','Reservoir2'").

    Returns:
    -------
    dict
        JSON response containing detailed information about the reservoirs.
    """
    url = requests_config["reservoir"]["get_reservoir_info"]["url"]
    payload = deepcopy(requests_config["reservoir"]["get_reservoir_info"]["payload"])
    payload = payload.format(reservoir_name_str)
    method = requests_config["reservoir"]["get_reservoir_info"]["method"]
    # Send request and get response
    json_response = get_response(url, payload, method, "get_reservoir_info")
    return json_response

