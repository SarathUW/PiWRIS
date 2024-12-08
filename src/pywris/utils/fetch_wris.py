import requests
import json

def get_response(url,payload, method, request_desciption=None):

    if method == 'GET':
        url_complete = url + payload
        response = requests.get(url_complete, verify=False)

    else:    
        response = requests.post(url, json=payload, verify=False)
    
    # Checking if the request was successful
    if response.status_code == 200:
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            if request_desciption is not None:
                print(f'Empty Response from the server for request: {request_desciption}.')
            else:
                print('Empty Response from the server.')
            return None
    else:
        print("Error:", response.status_code)
        raise Exception("Error:", response.status_code)