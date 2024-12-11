import pandas as pd
# from IPython.display import display, HTML

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
    
    def add_state(self, state_names):
        
        if isinstance(state_names, list):
            geo_components.check_valid_states(state_names)
            for state in state_names:
                self.states[state] = geo_components.State(state)
        else:
            self.states[state_names] = geo_components.State(state_names)
        
    def add_reservoir(self, reservoir_name, state_name):
        if reservoir_name not in self.reservoirs:
            self.reservoirs[reservoir_name] = geo_components.Reservoir(reservoir_name, state_name)
            
    def fetch_reservoir_data(self, end_date, start_date='1991-01-01', timestep='Daily'):
        if self.states.keys():
            self.reservoirs, self.reservoir_df = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_states=list(self.states.keys()))
        elif self.basins.keys():
            self.reservoirs, self.reservoir_df = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_basins=list(self.basins.keys()))
        else:
            raise ValueError("No states or basins defined in the HydroFrame.")
    
    def filter(self, on, by, range=None, values=None):
        return filter(self, on, by, range, values)
    
    def _repr_html_(self):
        """
        Generate an interactive HTML representation of PyWRIS HydroFrame Jupyter.
        """
        html = "======================================================"
        html += f"<h1 style = 'margin-bottom: 0; margin-top: 0;'>PyWRIS HydroFrame</h1>"
        html += "======================================================"
        
        # States Section
        if self.states:
            html += f"<h3 style='margin-bottom: 0;'>States: ({len(self.states)})</h3>"
            for state_name, state_obj in self.states.items():
                html += f"""
                <details>
                    <summary>{state_name}</summary>
                    {state_obj._repr_html_() if hasattr(state_obj, '_repr_html_') else '<p>No details available for this state.</p>'}
                </details>
                """
        else:
            pass
        
        # Reservoirs Section
        if self.reservoirs:
            html+="<br>-------------------------"
            html += f"<br><h3 style='margin-top: 0; margin-bottom: 0;'>Reservoirs: ({len(self.reservoirs)})</h3>"
            for res_name, res_obj in self.reservoirs.items():
                html += f"""
                <details>
                    <summary>{res_name}</summary>
                    {res_obj._repr_html_() if hasattr(res_obj, '_repr_html_') else '<p>No details available for this reservoir.</p>'}
                </details>
                
            """
        else:
            pass        
        
        # Basins Section
        if self.basins:
            html += f"<h3>Basins ({len(self.basins)}):</h3>"
            for basin_name, basin_obj in self.basins.items():
                html += f"""
                <details>
                    <summary><strong>Basin: {basin_name}</strong></summary>
                    {basin_obj._repr_html_() if hasattr(basin_obj, '_repr_html_') else '<p>No details available for this basin.</p>'}
                </details>
                """
        else:
            pass
        
        if not self.basins and not self.states:
            html += "<p>HydroFrame is currently empty as it has not been initialised with states.<br> Please pass a list of states to HydroFrame.add_state() to populate.</p>"


        return html

  


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
            filtered_df = hf.reservoir_df[hf.reservoir_df[by] >= range[0]] & hf.reservoir_df[hf.reservoir_df[by] <= range[1]]
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

