import pandas as pd
# from IPython.display import display, HTML

import pywris.geo_units.components as geo_components
import pywris.surface_water.storage.reservoir as py_reservoir

class HydroFrame:

    def __init__(self, states=None, basins=None):
        self.states = {}
        self.basins = {}
        self.reservoirs = {}
        self.reservoir_gdf = None
        self.reservoir_rawData = None
        
        ## Validate input 
        if states is not None:
            geo_components.check_valid_states(states)
            for state in states:
                self.add_state(state)
        else:
            pass
        
        # if reservoirs is not None:
        #     for res in reservoirs:
        #         self.add_reservoir(res, 'None')
    
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
            self.reservoirs, self.reservoir_gdf, self.reservoir_rawData = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_states=list(self.states.keys()))
        elif self.basins.keys():
            self.reservoirs, self.reservoir_gdf, self.reservoir_rawData = py_reservoir.get_reservoirs(end_date, start_date, timestep, selected_basins=list(self.basins.keys()))
        else:
            raise ValueError("No states or basins defined in the HydroFrame.")
    
    def filter(self, on, by, range=None, values=None):
        return filter(self, on, by, range, values)
    
    def test_connection(self):
        """
        Test connection to the IndiaWRIS website using a sample request.

        """
    
    def _repr_html_(self):
        """
        Generate an interactive HTML representation of PyWRIS HydroFrame Jupyter.
        """
        html = "----------------------------------------------------------------------------------------------------------------"
        html += f"<h1 style='margin-bottom: 0; margin-top: 0;'>PyWRIS HydroFrame</h1>"
        html += "----------------------------------------------------------------------------------------------------------------"

    
        if self.reservoirs:
            html+=f"<br>Downloaded Data: <strong>Reservoirs</strong>"
            html+=f"<br>Reservoir count: {len(self.reservoirs)}<br>"
        # html = """
        #     <div style="
        #         background-color: black; 
        #         padding: 6px; 
        #         border: 1px solid grey; 
        #         max-width: 275px;  
        #         text-align: left;">
        #         <h1 style="margin: 0;">PyWRIS HydroFrame</h1>
        #     </div>
        #     """
        
        # States Section
        if self.states:
            html += f"<h3 style='margin-bottom: 0;'>States: ({len(self.states)})</h3>"
            for state_name, state_obj in self.states.items():
                html += f"""
                <details>
                    <summary><strong>{state_name}</strong></summary>
                    {state_obj._repr_html_() if hasattr(state_obj, '_repr_html_') else '<p>No details available for this state.</p>'}
                    <div style="margin-left: 20px;">
                    
                """
                

                # Reservoirs Section within State
                state_reservoirs = [
                    res_obj for res_name, res_obj in self.reservoirs.items()
                    if res_obj.state.state_name == state_name
                ]
                if state_reservoirs:
                    html += f"""
                    <details>
                        <summary>Reservoirs ({len(state_reservoirs)}):</summary>
                        <div style="margin-left: 20px;">
                    """
                    for res_obj in state_reservoirs:
                        html += f"""
                        <details>
                            <summary>{res_obj.reservoir_name}</summary>
                            {res_obj._repr_html_() if hasattr(res_obj, '_repr_html_') else '<p>No details available for this reservoir.</p>'}
                        </details>
                        """
                    html += "</div></details>"
                else:
                    pass

                html += "</div></details>"

         
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

        if self.reservoirs:
            html += "<br><br>Quick help:<br>Reservoir data:"
            html += "<br>- HydroFrame.reservoirs:<i> Dictionary of Reservoir objects</i>"
            html += "<br>- HydroFrame.reservoir_gdf:<i> GeoDataFrame of static reservoir data</i>"
            html += "<br>- HydroFrame.reservoir_rawData:<i> DataFrame of complete reservoir data</i>"
            html += """ <div style="margin-bottom: 0">- Preset Plots: <br> </div>
                <ul style='margin-top: 0; margin-left:1; list-style-type: none'>
                    <li>- HydroFrame.reservoir_gdf.explore():<i> Interactive map with reservoir data</i> </li>
                    <li>- HydroFrame.reservoirs['Reservoir Name'].plot():<i> Time Series plots of individual reservoir data</i></li>
                </ul>
                """
        html += """
        <a href='https://sarathuw.github.io/PyWRIS/' style='color: inherit; text-decoration: none;'>
        <i>Click</i> for PyWRIS documentation
        </a>
        """
        html += "<br>----------------------------------------------------------------------------------------------------------------"
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
                filtered_df = hf.reservoir_gdf[hf.reservoir_gdf[by] in values]
            else:
                filtered_df = hf.reservoir_gdf[hf.reservoir_gdf[by] >= range[0]] & hf.reservoir_gdf[hf.reservoir_gdf[by] <= range[1]]
        else:
            raise ValueError("Invalid filter on.")
            
        filtered_hf = HydroFrame()
        filtered_hf.reservoir_gdf = filtered_df
        filtered_hf.states =  {key: hf.states[key] for key in filtered_df['state'].unique() if key in hf.states}
        filtered_hf.basins =  {key: hf.basins[key] for key in filtered_df['basin'].unique() if key in hf.basins}
        filtered_hf.reservoirs = {key: hf.reservoirs[key] for key in filtered_df['reservoir_name'].unique() if key in hf.reservoirs}

        
        return filtered_hf

## Things to DO:
## 1. Add representation to individual classes of State, Reservoir and District.
## 2. Adjust indentation and padding in HydroFrame representation
## 3. Renaming of columns in reservoir_gdf
## 4. Pytests

