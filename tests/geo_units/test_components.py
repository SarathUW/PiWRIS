import pytest
from pywris.geo_units.components import State, District, check_valid_states, get_districts
from unittest.mock import patch, MagicMock
from bidict import bidict

## Mock attributes and requests responses are used to test the functions in the components.py file.
###################################### Mocks and Patches ##########################################################

@pytest.fixture
def mock_state_id():
    """Fixture to mock state_id as a bidict."""
    return bidict({"Kerala": "KL"})

@pytest.fixture
def mock_districts():
    """Fixture to mock districts."""
    return {
        "Ernakulam": MagicMock(_repr_html_=lambda: "<p>Details for Ernakulam</p>"),
        "Kollam": MagicMock(_repr_html_=lambda: "<p>Details for Kollam</p>"),
    }

@pytest.fixture
def mock_get_districts(mock_districts):
    """Fixture to mock the get_districts function."""
    with patch("pywris.geo_units.components.get_districts", return_value=mock_districts):
        yield

@pytest.fixture
def mock_state(mock_state_id, mock_get_districts):
    """Fixture to create a mocked State instance."""
    with patch("pywris.static_data.state_ids.state_id", mock_state_id):
        yield State("Kerala")

@pytest.fixture
def mock_requests_config():
    """Fixture to mock requests_config."""
    return {
        "geounits": {
            "get_districts": {
                "url": "http://mock-url.com",
                "payload": 'f=json&orderByFields=district&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=state%20in%20(%27{}%27)',
                "method": "GET"
            }
        }
    }

@pytest.fixture
def mock_response():
    """Fixture to mock the response from get_response."""
    return {
        "features": [
            {
                "attributes": {
                    "district": "Ernakulam",
                    "state": "KL",
                    "district_code": 101,
                    "st_area(shape)": 500.0,
                    "st_length(shape)": 50.0
                }
            },
            {
                "attributes": {
                    "district": "Kollam",
                    "state": "KL",
                    "district_code": 102,
                    "st_area(shape)": 600.0,
                    "st_length(shape)": 60.0
                }
            }
        ]
    }

@pytest.fixture
def patches(mock_state_id, mock_requests_config, mock_response):
    """Fixture to apply necessary patches."""
    patches = [
        patch("pywris.geo_units.components.state_id", mock_state_id),
        patch("pywris.geo_units.components.requests_config", mock_requests_config),
        patch("pywris.geo_units.components.get_response", return_value=mock_response)
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()
################################################################################################################

############################################# Unit Tests #######################################################
def test_get_districts_smoke(patches):
    """Smoke test for get_districts function."""
    selected_states = ["Kerala"]
    result = get_districts(selected_states)

    # Smoke test checks - if function returns a dictionary and has two districts
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "Ernakulam" in result
    assert "Kollam" in result

    # Check attributes of one district
    district_a = result["Ernakulam"]
    assert district_a.district_name == "Ernakulam"
    assert district_a.district_code == 101
    assert district_a.district_area == 500.0


#smoke test for state class
def test_state_smoke():
    state = State('Kerala')
    assert state.state_name == 'Kerala'

def test__fetch_state_id():
    try:        
        State._fetch_state_id(State('Kerala'))
    except Exception as e:
        pytest.fail(f"Fetching state id failed: {e}")

#Edge case test for get_districts function - when wrong state name is passed
def test_get_districts_wrong_state(patches):
    """Edge case test for get_districts function."""
    selected_states = ["Karnataka"]
    with pytest.raises(ValueError):
        get_districts(selected_states)


#Smoke Test for _repr_html_ method of State class
def test_repr_html_with_districts(mock_state, mock_districts):
    """Test the HTML representation with districts fetched."""
    # Fetch districts
    mock_state.fetch_districts()

    # Generate HTML
    html_output = mock_state._repr_html_()

    # Check if the HTML includes the state ID and district details
    assert "State ID: KL" in html_output
    assert "Districts (2)" in html_output
    assert "Ernakulam" in html_output
    assert "Kollam" in html_output
    assert "<p>Details for Ernakulam</p>" in html_output
    assert "<p>Details for Kollam</p>" in html_output


#Smoke test for Distrcit class and _repr_html_
def test_district_initialization():
    """Test the initialization of the District class."""
    district = District(
        state_name="Kerala",
        district_name="Ernakulam",
        code=101,
        area=500.0,
        length=50.0
    )
    # Verify attributes
    assert district.state_name == "Kerala"
    assert district.district_name == "Ernakulam"
    assert district.district_code == 101
    assert district.district_area == 500.0
    assert district.district_length == 50.0

def test_district_initialization_defaults():
    """Test the initialization of District with default values."""
    district = District(state_name="Kerala")
    # Verify attributes
    assert district.state_name == "Kerala"
    assert district.district_name is None
    assert district.district_code is None
    assert district.district_area is None
    assert district.district_length is None

def test_district_repr_html():
    """Test the HTML representation of the District class."""
    district = District(
        state_name="Kerala",
        district_name="Ernakulam",
        code=101,
        area=500.0,
        length=50.0
    )
    # Generate HTML
    html_output = district._repr_html_()

    # Verify HTML content
    assert "District Code: 101" in html_output
    assert "Area: 500.0 km²" in html_output