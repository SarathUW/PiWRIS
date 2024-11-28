from pywris.utils.fetch_wris import get_response
from pywris.country_data.state_codes import state_code
import pandas as pd

class State:
    
    def __init__(self, state_name):
        self.name = state_name
        self.id = self._fetch_state_id()
        self.districts = {}

    def _fetch_state_id(self):
        if self.name in state_code.keys():
            return state_code[self.name]
        else:
            return None

    def fetch_districts(self):
        '''
        fetches list of districts given state name
        parameters:

        '''
        url = 'https://arc.indiawris.gov.in/server/rest/services/Admin/Administrative_NWIC/MapServer/1/query?'
        if self.id is not None:
            payload = f'f=json&orderByFields=district&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=state%20in%20(%27{self.id}%27)'
        else:
            raise ValueError(f'State not found. List of available states: {state_code.keys()}')
        json_response = get_response(url, payload, method = 'GET')
        districts_data = pd.json_normalize(json_response['features'])
        
        self.districts = {}
        for index, district_row in districts_data.iterrows():
            key = district_row['attributes.district']
            
            district_id = district_row['attributes.district_code']
            district_code = district_row['attributes.district_code']
            district_area = district_row['attributes.st_area(shape)']
            district_length = district_row['attributes.st_length(shape)']
            district_intance = District(district_id, district_code, district_area, district_length)
            self.districts[key] = district_intance
            
        return list(self.districts.keys())


class District:
    def __init__(self, dist_id, code, area = None, length = None):
        self.id = dist_id
        self.code = code
        self.area = area
        self.length = length
        self.reservoirs = []

class Reservoir:
    def __init__(self, state):
        self.state = State(state)        
        self.district = None
        pass
    

        
    def fetch_reservoirs(self):
        pass

    def fetch_reservoir_data(self):
        pass


