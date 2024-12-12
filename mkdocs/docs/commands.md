## Commands

This page lists all avilable functions. For example usage, please see the [Tutorials](tutorials.md) page.

### Checking Validity

* `check_valid_states(selected_states)` - Check if all listed states are valid
* `check_valid_date_range(start_date, end_date, valid_date_range)` - Check if given date range is valid
    - start_date: start date of the data to fetch, formatted as YYYY-MM-DD or as a timestamp
    - end_date: end date of the data to fetch, formatted as YYYY-MM-DD or as a timestamp
    - valid_date_range: a list or tuple containing two elements (valid start and end dates) as strings or timestamps

### Fetching information

* `get_districts(selected_states)` - Get a dictionary of districts in given states
* `get_reservoirs(end_date, start_date, timestep, selected_states, selected_districts, selected_basins, selected_reservoirs)` - Get a list of reservoirs and their time series data based on the given arguments
    - end_date: end date of the data to fetch (YYYY-MM-DD)
    - start_date (optional): start date of the data to fetch (YYYY-MM-DD). If left empty, will default to 1991-01-01
    - timestep (optional): the temporal resolution of the data. If left empty, will default to Daily
    - selected_states: list of state names to filter reservoirs. If no selected_basins are specified, this is required
    - selected_districts: list of district names to filter reservoirs. Use "all" to include reservoirs from all districts
    - selected_basins: list of basin names to filter reservoirs. If no selected_states are specified, this is required
* `get_reservoir_data_valid_date_range()` - Get the avaliable date range for reservoir data
* `get_reservoir_info(reservoir_name_str)` - Get information for specific reservoirs
    - reservoir_name_str: reservoir names, separated by commas, formatted with single quotes
* `get_reservoir_names(states_list_str, districts_names_list_str)` - Get the names of reservoirs in specified states and districts
    - states_list_str: state names, separated by commas, formatted with single quotes
    - districts_names_list_str: district names, separated by commas, formatted with single quotes

### Plotting

* `plot_data(input_object, **args)` - General plotting function
    - input_object: the object to plot (an instance of Reservoir, Groundwater, etc.)
* `plot_reservoir(self, columns, title)` - Create interactive timeseries plot for reservoir data
    - columns: list of columns to plot. If none, it will default to all numeric columns except "Date"
    - title: custom title for the plot

### Hydroframe
* `hydroframe.reservoirs` - get dictionary of reservoirs currently in hydroframe
    * `['reservoir_name'].plot()` - generate time series plot for selected reservoir in hydroframe
* `hydroframe.reservoir_gdf` - get static reservoir data in GeoDataFrame
    * `.explore()` - generate interactive map with reservoir data
* `hydroframe.reservoir_rawData` - get complete reservoir data