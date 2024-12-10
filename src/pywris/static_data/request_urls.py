requests_config = {
    'reservoir': {
        'get_reservoir_names':{
            'url': 'https://indiawris.gov.in/getReservoirBusinessData',
            'payload': {"stnVal":{"qry":"select distinct(reservoir_name) from public.reservoir_data where state_name in ({}) and district_name in ({}) order by reservoir_name asc"}},
            'method': 'POST'
        },
        'get_reservoir_data_valid_date_range':{
            'url': 'https://indiawris.gov.in/getReservoirBusinessData',
            'payload': {"stnVal":{"qry":"select min(to_char(date, \'yyyy-mm-dd\')), max(to_char(date, \'yyyy-mm-dd\')) from public.reservoir_data"}},
            'method': 'POST'
        },
        'get_reservoir_data':{
            'url': 'https://indiawris.gov.in/resdnlddata',
            'payload': {"stnVal":{"Reporttype":"Level & Storage Timeseries","View":"Admin","Agencyname":"All",
                              "Reservoir":"\"{}\"","Timestep":"{}","Parent":"","Child":"","Startdate":"{}","Enddate":"{}"}},
            'method': 'POST'
        },
        'get_reservoir_info':{
            'url':'https://arc.indiawris.gov.in/server/rest/services/NWIC/Reservoir_Points/MapServer/0/query?',
            'payload':'f=json&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=station_type=%27Reservoir%27%20AND%20station_name%20IN%20({})',
            'payload_all_reservoirs':'f=json&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=station_type=%27Reservoir%27',
            'method': 'GET'
        }
    },
    'geounits': {
        'get_districts':{
            'url': 'https://arc.indiawris.gov.in/server/rest/services/Admin/Administrative_NWIC/MapServer/1/query?',
            'payload': 'f=json&orderByFields=district&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=state%20in%20(%27{}%27)',
            'method': 'GET'
        }
    },

}
