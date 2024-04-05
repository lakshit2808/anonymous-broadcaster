import json
import requests

def ReadData():
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {} 
    return existing_data 

def SendMessage(chat_ids, message):
    for id in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}"
        print(requests.get(url).json())   

def WriteData(data, org=None):
    existing_data = ReadData()

    if org is not None:
        if data not in existing_data['organisations']:
            existing_data['organisations'].append(data)
        else:
            print(f"Organisation {data} already exists.")
    else:
        if data not in existing_data['users']:
            existing_data['users'].append(data)
        else:
            print(f"User {data} already exists.")

    # Writing the updated data back to the JSON file
    with open('data.json', 'w') as json_file:
        json.dump(existing_data, json_file)