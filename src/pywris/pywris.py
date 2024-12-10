import pandas as pd
from IPython.display import display, HTML

import pywris.geo_units.components as geo_components
import pywris.surface_water.storage.reservoir as py_reservoir

class HydroFrame:
    def __init__(self, states=None, basins=None, reservoirs=None):
        self.states = {}
        self.basins = {}
        self.reservoirs = {}
        self.reservoir_df = None
        
        ## Validate input 
        if states is not None:
            geo_components.check_valid_states(states)
            for state in states:
                self.add_state(state)
        else:
            pass
        
        if reservoirs is not None:
            for res in reservoirs:
                self.add_reservoir(res, 'None')
    
    def add_state(self, state_name):        
        self.states[state_name] = geo_components.State(state_name)
        
    def add_reservoir(self, reservoir_name, state_name):
        if reservoir_name not in self.reservoirs:
            self.reservoirs[reservoir_name] = geo_components.Reservoir(reservoir_name, state_name)
            
    def fetch_reservoirs(self, end_date, start_date='1991-01-01', timestep='Daily'):
        if self.states.keys():
            self.reservoirs, self.reservoir_df = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_states=list(self.states.keys()))
        elif self.basins.keys():
            self.reservoirs, self.reservoir_df = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_basins=list(self.basins.keys()))
        else:
            raise ValueError("No states or basins defined in the HydroFrame.")
    
    def filter(self, on, by, range=None, values=None):
        return filter(self, on, by, range, values)
    
    def _generate_display_data(self):
        """ Prepare the data to be displayed in a neat format """
        display_data = {
            "States": list(self.states.keys()),
            "Reservoirs": list(self.reservoirs.keys()),
        }
        return display_data

    def _expand_reservoir(self, reservoir_name):
        """ Expands to show attributes of a reservoir """
        reservoir = self.reservoirs.get(reservoir_name)
        if reservoir:
            return {
                "Reservoir Name": reservoir.reservoir_name,
                "State": reservoir.state.state_name,
                "District": reservoir.district.district_name if reservoir.district else None,
                "Latitude": reservoir.latitude,
                "Longitude": reservoir.longitude,
                "Block Name": reservoir.block_name,
                "Basin": reservoir.basin,
                "Sub Basin Name": reservoir.sub_basin_name,
                "Agency": reservoir.agency,
                "FRL": reservoir.frl,
                "Live Cap FRL": reservoir.live_cap_frl,
            }
        return {}

    def _repr_html_(self):
        """ Display the HydroFrame in a neat, interactive way """
        display_data = self._generate_display_data()
        
        html_str = "<h3>HydroFrame Overview</h3>"
        
        # Add state list
        html_str += "<b>States:</b><br>"
        for state in display_data["States"]:
            html_str += f"<button onclick='expandItem(\"state_{state}\")'>{state}</button><br>"
            html_str += f"<div id='state_{state}' style='display:none'>{state}</div>"
        
        # Add reservoirs
        html_str += "<br><b>Reservoirs:</b><br>"
        for reservoir in display_data["Reservoirs"]:
            html_str += f"<button onclick='expandItem(\"reservoir_{reservoir}\")'>{reservoir}</button><br>"
            html_str += f"<div id='reservoir_{reservoir}' style='display:none'>{self._expand_reservoir(reservoir)}</div>"
        
        # Inject JS for expanding and collapsing
        html_str += """
        <script>
        function expandItem(id) {
            var item = document.getElementById(id);
            if (item.style.display === 'none') {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        }
        </script>
        """
        
        return html_str

def filter(hf, on, by, range=None, values=None):
    # Validate input
    if values is not None and range is not None:
        raise ValueError("Values and range cannot be used together.")
    elif values is None and range is None:
        raise ValueError("Either values or range must be provided.")
    else:
        pass

    if on == 'reservoir':
        if values is not None:
            filtered_df = hf.reservoir_df[hf.reservoir_df[by] in values]
        else:
            filtered_df = hf.reservoir_df[hf.reservoir_df[by] >= range[0]] & hf.reservoir_df[hf.reservoir_df[by] <= range[1]
    else:
        raise ValueError("Invalid filter on.")
        
    filtered_hf = HydroFrame()
    filtered_hf.reservoir_df = filtered_df
    filtered_hf.states =  {key: hf.states[key] for key in filtered_df['state'].unique() if key in hf.states}
    filtered_hf.basins =  {key: hf.basins[key] for key in filtered_df['basin'].unique() if key in hf.basins}
    filtered_hf.reservoirs = {key: hf.reservoirs[key] for key in filtered_df['reservoir_name'].unique() if key in hf.reservoirs}

    
    return filtered_hf

## Things to DO:
## 1. Add representation to individual classes of State, Reservoir and District.
## 2. Adjust indentation and padding in HydroFrame representation
## 3. Renaming of columns in reservoir_df
## 4. Pytests

