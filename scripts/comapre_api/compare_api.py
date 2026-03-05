import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from datetime import datetime, timedelta, timezone

    import requests
    return datetime, requests, timedelta, timezone


@app.cell
def _():
    current_api = "https://api-dev.quartz.solar/"
    new_api = "http://uk-development-uk-national-quartz-api.eu-west-1.elasticbeanstalk.com/"


    access_token = "todo"
    return access_token, current_api, new_api


@app.cell
def _(access_token, current_api, new_api, requests):
    def compare_one_call(call):
        print(call)

        current_url = current_api + call
        new_url = new_api + call
        r = requests.get(url=current_url,headers={"Authorization": "Bearer "+access_token})
        r_new = requests.get(url=new_url,headers={"Authorization": "Bearer "+access_token})

        print(f"Current API: {r.status_code}")
        print(f"New API: {r_new.status_code}")

        data = r.json()
        data_new = r_new.json()

        if isinstance(data, dict):
            print(f"Current API: Length Keys {len(data.keys())}")
            print(f"New API: Length Keys {len(data_new.keys())}")

            if len(data.keys()) != len(data_new.keys()):
                print("Error: Number of keys in the response is different between the two APIs")
            for key in data.keys():
                if isinstance(data[key], dict):
                    print(f"Current API: Length of {key} is {len(data[key])}")
                    print(f"New API: Length of {key} is {len(data_new[key])}")

            if "forecastValues" in data.keys():
                if len(data["forecastValues"]) == len(data_new["forecastValues"]):
                    print(f"Number of forecast values is the same between the two APIs: {len(data['forecastValues'])}")
                else:
                    print(f"Error: Number of forecast values is different between the two APIs: {len(data['forecastValues'])} != {len(data_new['forecastValues'])}")

        if isinstance(data, list):
            print(f"Current API: Length Keys {len(data)}")
            print(f"New API: Length Keys {len(data_new)}")
            if len(data) != len(data_new):
                print(f"Error: Number of forecast values is different between the two APIs: {len(data)} != {len(data_new)}")

    return (compare_one_call,)


@app.cell
def _(compare_one_call, datetime, timedelta, timezone):
    # miha.troha@comcom.si

    now = datetime.now(tz=timezone.utc) - timedelta(minutes=30)
    now_plus_2_days = now + timedelta(days=2)

    now = now.strftime("%Y-%m-%dT%H:00:00") + "%2B00:00"
    now_plus_2_days = now_plus_2_days.strftime("%Y-%m-%dT%H:00:00") + "%2B00:00"

    calls = [f"v0/solar/GB/national/forecast?start_datetime_utc={now}&end_datetime_utc={now_plus_2_days}&include_metadata=true&model_name=blend",f"v0/solar/GB/gsp/100/forecast?start_datetime_utc={now}&end_datetime_utc={now_plus_2_days}"]


    for call in calls:

        compare_one_call(call)
    return now, now_plus_2_days


@app.cell
def _(compare_one_call, now, now_plus_2_days):
    # emc_notifications@edfenergy.com

    models = ["blend","pvnet_intraday","pvnet_day_ahead","pvnet_intraday_ecmwf_only"]

    calls1 = [f"v0/solar/GB/national/forecast?start_datetime_utc={now}&end_datetime_utc={now_plus_2_days}&include_metadata=true&model_name=X&historic=false",f"v0/solar/GB/national/forecast?start_datetime_utc={now}&end_datetime_utc={now_plus_2_days}&model_name=X&historic=true&forecast_horizon_minutes=180"]


    for model in models:
        for call1 in calls1:
            call1 = call1.replace("model_name=X",f"model_name={model}")
            compare_one_call(call1)


    return


@app.cell
def _(compare_one_call):
    # rdf@.outlookemergy.co.uk

    calls2 = ["v0/solar/GB/national/forecast?only_forecast_values=true"]

    for call2 in calls2:

        compare_one_call(call2)
    return


if __name__ == "__main__":
    app.run()
