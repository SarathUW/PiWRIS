# import modules and functions
import pytest
from unittest.mock import patch, MagicMock
from pywris import HydroFrame
import pywris.surface_water.storage.reservoir as py_reservoir


########################################## Mocks and Patches ##########################################################
@pytest.fixture
def mock_geo_components():
    """Mock the geo_components module."""
    return {
        "check_valid_states": MagicMock(),
        "State": MagicMock(),
        "Reservoir": MagicMock(),
    }

@pytest.fixture
def mock_get_reservoirs():
    with patch('pywris.surface_water.storage.reservoir.get_reservoirs') as mock_function:
        # Set up the mock return values
        mock_function.return_value = (
            ['Reservoir1', 'Reservoir2', 'Reservoir3'],  # reservoirs
            MagicMock(),  # reservoirs_gdf (mocked GeoDataFrame)
            MagicMock()   # reservoirs_rawData (mocked raw data)
        )
        yield mock_function

@pytest.fixture
def patches(mock_geo_components):
    patches = [
        patch("pywris.geo_units.components", mock_geo_components),
        # patch("pywris.surface_water.storage.reservoir.get_reservoirs", mock_py_reservoir),
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()

############################################ UNIT TESTS ################################################################
#Smoke test for HydroFrame initialization - empty
def test_hydroframe_initialization_empty():
    """Test HydroFrame initialization."""
    hf = HydroFrame()

    assert hf.states == {}
    assert hf.reservoirs == {}
    assert hf.reservoirs_gdf == None
    assert hf.reservoirs_rawData == None

#Smoke test for HydroFrame initialization - with states
def test_hydroframe_initialization(patches):
    """Test HydroFrame initialization."""
    hf = HydroFrame(states=["Kerala", "Tamil Nadu"])

    assert "Kerala" in hf.states
    assert "Tamil Nadu" in hf.states

#Smoke test for add_state method
def test_add_state(patches):
    """Test add_state method."""
    hf = HydroFrame()
    hf.add_state(["Kerala", "Tamil Nadu"])

    # Verify states are added correctly
    assert len(hf.states) == 2
    assert "Kerala" in hf.states
    assert "Tamil Nadu" in hf.states

#Smoke test for fetch_reservoir_data method
def test_fetch_reservoir_data_no_states_or_basins(patches):
    """Test fetch_reservoir_data raises error when no states or basins are defined."""
    hf = HydroFrame()

    with pytest.raises(ValueError, match="No states or basins defined in the HydroFrame."):
        hf.fetch_reservoir_data(end_date="2024-12-01", start_date="2024-01-01")

#One-shot test for fetch_reservoir_data method
def test_fetch_reservoir_data(mock_get_reservoirs):
    # Create an instance of the HydroFrame class
    hydroframe = HydroFrame()
    
    # Configure attributes for the test
    hydroframe.selection_allState = True
    hydroframe.states = {}
    hydroframe.basins = {}

    # Call the method
    hydroframe.fetch_reservoir_data(end_date='2024-12-01')

    # Assert the mock was called with correct parameters
    mock_get_reservoirs.assert_called_once_with(
        '2024-12-01', '1991-01-01', 'Daily', selected_states='all'
    )

    # Check that the attributes were set as expected
    assert len(hydroframe.reservoirs) == 3
    assert hydroframe.reservoirs == ['Reservoir1', 'Reservoir2', 'Reservoir3']
    assert hydroframe.reservoirs_gdf is not None
    assert hydroframe.reservoirs_rawData is not None
