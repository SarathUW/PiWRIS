import pytest
from unittest.mock import patch, MagicMock
from pywris.geo_units.components import State, District
from pywris.surface_water.storage.reservoir import Reservoir
from pywris.surface_water.storage.reservoir import get_reservoirs, get_reservoir_data_valid_date_range
import pandas as pd

pytestmark = pytest.mark.filterwarnings("ignore::Warning")
################# MOCKS and PATCHES ############################

@pytest.fixture
def mock_state_id():
    """Fixture to mock state_id."""
    return {"Kerala": "KL"}

@pytest.fixture
def mock_districts():
    return {"Idukki": MagicMock(), "Wayanad": MagicMock()}

@pytest.fixture
def mock_reservoir_names():
    return [["Idukki Reservoir"], ["Wayanad Reservoir"]]

@pytest.fixture
def mock_reservoir_data():
    """Fixture to mock reservoir live data as a pandas DataFrame."""
    return pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "Storage (MCM)": [10.5, 11.0, 12.0, 12.5],
        "Inflows (cumecs)": [100, 110, 120, 130],
        "Outflows (cumecs)": [90, 95, 100, 105],
    })

@pytest.fixture
def mock_reservoir_info():
    return {
        "features": [
            {
                
                "attributes.station_name": "Idukki Reservoir",
                "attributes.state_name": "Kerala",
                'attributes.state_code': 'KL',
                'attributes.district_name': 'Idukki',
                "attributes.lat": 9.85,
                "attributes.long": 76.96,
                "attributes.agency_name": "Agency A",
                "attributes.dam_code": "IDK001",
                "attributes.frl": 2398,
                "attributes.lsc_frl": 1450,
                "attributes.block_name": "Block A",
                "attributes.basin_name": "Periyar Basin",
                "attributes.basin_code": "PB01",
                "attributes.sub_basin_name": "Sub-Basin A",
                
            }
        ]
    }

@pytest.fixture
def mock_reservoir_data():
    return [
        {"Reservoir Name": "Idukki Reservoir", "Date": "2024-01-01", "Child": "Idukki", "Level": 100, "Current Live Storage": 50},
        {"Reservoir Name": "Idamalayaar Reservoir","Child": "Idukki", "Date": "2024-01-02", "Level": 101, "Current Live Storage": 52},
    ]

#Applying patch
@pytest.fixture
def patches(mock_state_id, mock_districts, mock_reservoir_names, mock_reservoir_info, mock_reservoir_data):
    patches = [
        patch("pywris.static_data.state_ids.state_id", mock_state_id),
        patch("pywris.surface_water.storage.reservoir.geo_components.get_districts", return_value=mock_districts),
        patch("pywris.surface_water.storage.reservoir.get_reservoir_names", return_value=mock_reservoir_names),
        patch("pywris.surface_water.storage.reservoir.get_reservoir_info", return_value=mock_reservoir_info),
        patch("pywris.surface_water.storage.reservoir.get_reservoir_data", return_value=mock_reservoir_data),
        patch("pywris.surface_water.storage.reservoir.get_reservoir_data_valid_date_range", return_value=("1990-01-01", "2024-12-31")),
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()



################# UNIT TESTS ############################
#Smoke Test for reservoir class
def test_reservoir_initialization():
    """Test the initialization of the Reservoir class."""
    reservoir = Reservoir(
        reservoir_name="Idukki",
        state="Kerala",
        district="Idukki"
    )

    # Verify attributes
    assert reservoir.reservoir_name == "Idukki"
    assert reservoir.state.state_name == "Kerala"
    assert reservoir.district.state_name == "Kerala"

#Smoke Test for _repr_html_ method with no data
def test_reservoir_repr_html_no_data():
    """Test the HTML representation of the Reservoir class without data."""
    reservoir = Reservoir(
        reservoir_name="Idukki",
        state="Kerala",
        district="Idukki"
    )

    # Generate HTML
    html_output = reservoir._repr_html_()

    # Verify HTML content
    assert "Static Data" in html_output
    assert "State: Kerala" in html_output
    assert "Latitude: N/A" in html_output
    assert "Longitude: N/A" in html_output
    assert "FRL: N/A m" in html_output
    assert "Live Capacity (FRL): N/A MCM" in html_output

# Smoke and One-shot test for get_reservoirs() method
def test_get_reservoirs_valid(patches):
    """Test get_reservoirs with valid input."""
    reservoirs, reservoir_gdf, reservoir_data_df = get_reservoirs(
        end_date="2024-12-01",
        selected_states=["Kerala"],
        selected_districts=["Idukki"],
        selected_reservoirs=["Idukki Reservoir"]
    )

    # Verify reservoirs dictionary
    assert isinstance(reservoirs, dict)
    assert "Idukki Reservoir" in reservoirs
    res = reservoirs["Idukki Reservoir"]
    assert res.state.state_name == "Kerala"
    assert res.latitude == 9.85
    assert res.longitude == 76.96

    # Verify GeoDataFrame output
    assert "geometry" in reservoir_gdf.columns
    assert reservoir_gdf.crs.to_string() == "EPSG:4326"

    # Verify reservoir data DataFrame
    assert "Date" in reservoir_data_df.columns
    assert "Level" in reservoir_data_df.columns
    assert len(reservoir_data_df) == 2

#Edge case test for get_reservoirs() method
#1. If selected_states is not a list
#2. If selected_districts is not a list
#3. If selected_reservoirs is not a list

def test_get_reservoirs_invalid_input(patches):
    """Test get_reservoirs with invalid input."""
    with pytest.raises(ValueError):
        get_reservoirs(
            end_date="2024-12-01",
            selected_states="Kerala",
            selected_districts=["Idukki"],
            selected_reservoirs=["Idukki Reservoir"]
        )

    with pytest.raises(ValueError):
        get_reservoirs(
            end_date="2024-12-01",
            selected_states=["Kerala"],
            selected_districts="Idukki",
            selected_reservoirs=["Idukki Reservoir"]
        )

    with pytest.raises(ValueError):
        get_reservoirs(
            end_date="2024-12-01",
            selected_states=["Kerala"],
            selected_districts=["Idukki"],
            selected_reservoirs="Idukki Reservoir"
        )