import dataset
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

date_min = datetime.min.replace(tzinfo=pytz.UTC)
date_max = datetime.max.replace(tzinfo=pytz.UTC)


def generate_plot(process_data):
    hours, temps, labels = extract_temperature_hour(process_data)
    for i, j, k in zip(hours, temps, labels):
        plt.plot(i, j, label=k)
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Temperature °C")
    plt.title("Temperature evolution")
    plt.savefig(f"out.png", dpi=300, verbose=False)
    # plt.show()


def parse_data(input_data: list):
    out_data = []
    _data = next(input_data)
    current_day = _data["date"].day
    current_data = [_data]
    for i in input_data:
        day = i["date"].day
        if day != current_day:
            out_data.append(current_data)
            current_data = []
        else:
            current_data.append(i)
        current_day = day
    if current_data:
        out_data.append(current_data)
    return out_data


def extract_data(db, _date_min=date_min, _date_max=date_max):
    table = db["weather"]
    out_data = table.find(date={"between": [_date_min, _date_max]})
    return out_data


def extract_temperature_hour(_data):
    out_temp = []
    out_hours = []
    out_labels = []
    for day in _data:
        current_temp = []
        current_hour = []
        for measure in day:
            current_temp.append(measure["temperature"])
            current_hour.append(measure["date"].hour + measure["date"].minute / 60)
        current_day = measure["date"]
        out_labels.append(f"{current_day.day}/{current_day.month}/{current_day.year}")
        out_temp.append(current_temp)
        out_hours.append(current_hour)
    return out_hours, out_temp, out_labels


if __name__ == "__main__":
    with dataset.connect("sqlite:///weather.db") as db:
        data = extract_data(db)
        data_parsed = parse_data(data)
        generate_plot(data_parsed)
