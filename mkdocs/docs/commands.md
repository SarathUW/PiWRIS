## Commands {wip}

* `check_valid_states(selected_states)` - Check if all listed states are valid
* `get_districts(selected_states)` - Get a dictionary of districts in given states.
* `get_reservoirs(end_date, start_date, timestep, selected_states, selected_districts, selected_basins, selected_reservoirs)` - Get a list of reservoirs and their time series data based on the given arguments
    - end_date: end date of the data to fetch (YYYY-MM-DD)
    - start_date (optional): start date of the data to fetch (YYYY-MM-DD). If left empty, will default to 1991-01-01
    - timestep (optional): the temporal resolution of the data. If left empty, will default to Daily.
    - selected_states: list of state names to filter reservoirs. If no selected_basins are specified, this is required.
    - selected_districts: list of district names to filter reservoirs. Use "all" to include reservoirs from all districts
    - selected_basins: list of basin names to filter reservoirs. If no selected_states are specified, this is required.
* `get_reservoir_data(reservoir)`
* `get_reservoir_data_valid_date_range()` - Get the avaliable date range for reservoir data
* `get_reservoir_info(reservoir_name_str)` - Get information for specific reservoirs
    - reservoir_name_str: reservoir names, separated by commas, formatted with single quotes
* `get_reservoir_names(states_list_str, districts_names_list_str)` - Get the names of reservoirs in specified states and districts
    - states_list_str: state names, separated by commas, formatted with single quotes
    - district_names_list_str: district names, separated by commas, formatted with single quotes
* `plot(self, args)` - Plot reservoir timeseries data
