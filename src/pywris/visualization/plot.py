from plotly.subplots import make_subplots
# from pywris.surface_water.storage.reservoir import Reservoir
import plotly.graph_objects as go
import pandas as pd


def plot_data(input_object, **args):
    """
    General plotting function that handles different object types and their specific plotting logic.

    Parameters:
    - input_object: The object to plot (either an instance of Reservoir, Groundwater, etc.)
    - **args: Additional arguments for customization (e.g., columns to plot, title, etc.)
    """
    from pywris.surface_water.storage.reservoir import Reservoir
    if isinstance(input_object, Reservoir):
        return plot_reservoir(input_object, **args)
    else:
        raise TypeError(f"Unsupported object type: {type(input_object)}. Only 'Reservoir' class is supported.")
    
def plot_reservoir(self, columns=None, title=None):
        """
        Create an interactive Plotly time series plot for reservoir data.

        Parameters:
        - columns (list): List of columns to plot (Currently ['Level', 'Current Live Storage']).
                          If None, it will plot all numeric columns except 'Date'.
        - title (str): Custom title for the plot, if provied.
        """
        if self.data is None or self.data.empty:
            raise ValueError(f"No data available for reservoir {self.reservoir_name} to plot.")
        
        if not pd.api.types.is_datetime64_any_dtype(self.data['Date']):
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        else:
            pass
        
        if columns is None:
            columns = [col for col in self.data.columns if col != 'Date' and pd.api.types.is_numeric_dtype(self.data[col])]
        else:
            missing_cols = [col for col in columns if col not in self.data.columns]
            if missing_cols:
                raise KeyError(f"The following columns are missing from data: {missing_cols}")
            else:
                pass

        fig = make_subplots(specs=[[{"secondary_y": True}]]) 
        for column in columns:
            fig.add_trace(
                go.Scatter(
                    x=self.data['Date'],
                    y=self.data[column],
                    mode='lines+markers',
                    name=column
                ),
                secondary_y=False
            )
        fig.update_layout(
            title=title or f"Time Series Data for Reservoir: {self.reservoir_name}",
            xaxis_title="Date",
            yaxis_title="Values",
            template="plotly_white",
            legend=dict(title="Legend"),
            hovermode="x unified",
        )
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
        fig.show()
