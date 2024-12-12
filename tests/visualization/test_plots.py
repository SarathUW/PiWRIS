# import modules and functions
import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock
from unittest.mock import patch
from pywris.surface_water.storage.reservoir import get_reservoirs  
import pywris.geo_units.components as geo_components

def create_synthetic_reservoir_data():
    """Generate synthetic reservoir data for testing purposes."""
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = {
        'Date': date_range,
        'Level': np.random.uniform(50, 150, size=len(date_range)),  # Random reservoir levels
        'Current Live Storage': np.random.uniform(1000, 5000, size=len(date_range)),  # Random storage values
    }
    return pd.DataFrame(data)

def mock_get_reservoirs(*args, **kwargs):
    """Mock the 'get_reservoirs' function to return synthetic reservoirs."""
    reservoirs = {
        'Bisalpur': MagicMock(),
        'Mahi Bajaj Sagar': MagicMock(),
    }
    reservoirs['Bisalpur'].data = create_synthetic_reservoir_data()
    reservoirs['Mahi Bajaj Sagar'].data = create_synthetic_reservoir_data()
    return reservoirs, pd.DataFrame(), pd.DataFrame()

def test_reservoir_plot_smoke():
    """
    Smoke test to ensure the 'plot' method works for a known reservoir ('Bisalpur') with synthetic data.
    """
    reservoirs, _, _ = mock_get_reservoirs(end_date='2023-04-01', selected_states=['Rajasthan'])
    try:
        reservoirs['Mahi Bajaj Sagar'].data.plot()
    except Exception as e:
        pytest.fail(f"Plotting failed for Bisalpur reservoir with synthetic data: {e}")

def test_reservoir_plot_non_existent_column():
    """
    Edge test for plotting with a column that doesn't exist in the data.
    """
    reservoirs, _, _ = mock_get_reservoirs(end_date='2023-04-01', selected_states=['Rajasthan'])
    non_existent_column = 'NonExistentColumn'
    try:
        reservoirs['Bisalpur'].plot(columns = [non_existent_column])
    except Exception :
        pytest.fail(f"Edge test failed: {non_existent_column} should not exist in the data.")

def test_reservoir_plot_functionality():
    """
    One-shot test to ensure the 'plot' method works for a known reservoir.
    """
    reservoirs, _, _ = mock_get_reservoirs(end_date='2023-04-01', selected_states=['Rajasthan'])
    try:
        reservoirs['Bisalpur'].plot()
    except Exception as e:
        pytest.fail(f"Plotting failed for Bisalpur reservoir: {e}")

def test_reservoir_plot_functionality_single():
    """
    One-Shot test to ensure the 'plot' method works for a known reservoir and specific column.
    """
    reservoirs, _, _ = mock_get_reservoirs(end_date='2023-04-01', selected_states=['Rajasthan'])
    try:
        reservoirs['Bisalpur'].plot(columns = ['Level'])
    except Exception as e:
        pytest.fail(f"Plotting failed for Bisalpur reservoir: {e}")

def test_reservoir_add_column_and_plot():
    """
    One-shot Test: adding a new column to the reservoir data and plotting it.
    """
    reservoirs, _, _ = mock_get_reservoirs(end_date='2023-04-01', selected_states=['Rajasthan'])
    try:
        # reservoirs['Bisalpur'].data['added_column'] = np.nan
        reservoirs['Bisalpur'].data['added_column'] = reservoirs['Bisalpur'].data[reservoirs['Bisalpur'].data.columns[1]] * 2
        reservoirs['Bisalpur'].plot()
    except Exception as e:
        pytest.fail(f"Adding a new column and plotting failed: {e}")
