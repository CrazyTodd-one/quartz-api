current_api = "https://api-dev.quartz.solar/"
new_api = "http://uk-development-uk-national-quartz-api.eu-west-1.elasticbeanstalk.com/"



calls = ["v0/solar/GB/national/forecast?start_datetime_utc=2026-02-23T11:00:00%2B00:00&end_datetime_utc=2026-02-25T11:00:00%2B00:00&include_metadata=true&model_name=blend"]

access_token = "todo"

import requests

for call in calls:

    print(call)

    current_url = current_api + call
    new_url = new_api + call
    r = requests.get(url=current_url,headers={"Authorization": "Bearer "+access_token})
    r_new = requests.get(url=new_url,headers={"Authorization": "Bearer "+access_token})

    data = r.json()
    data_new = r_new.json()

    print(f"Current API: {r.status_code}")
    print(f"New API: {r_new.status_code}")

    print(f"Current API: Length Keys {len(data.keys())}")
    print(f"New API: Length Keys {len(data_new.keys())}")

    assert len(data.keys()) == len(data_new.keys()), "Number of keys in the response is different between the two APIs"
    for key in data.keys():
        if isinstance(data[key], dict):
            print(f"Current API: Length of {key} is {len(data[key])}")
            print(f"New API: Length of {key} is {len(data_new[key])}")

    if len(data["forecastValues"]) == len(data_new["forecastValues"]):
        print(f"Number of forecast values is the same between the two APIs: {len(data['forecastValues'])}")
    else:
        print(f"Number of forecast values is different between the two APIs: {len(data['forecastValues'])} != {len(data_new['forecastValues'])}")
