import json
import datetime

import pandas as pd

from package.database import ConnectionMySQL
from package.api import API
import random
import numpy as np

# get public holiday data from ileo database
def getPubHoliday():
    request = "SELECT type, date " \
              "FROM time_hr_publicholidays " \
              "WHERE fk_country = 21 " \
              "AND date < '2021-09-23 00:00:00'"

    connectionileo = ConnectionMySQL("ileo")
    response = connectionileo.query(request, None).fetchall()
    connectionileo.close()

    return response

#get scolar holiday from hardcoding
def getScoHoliday():
    scoholiday = []
    # winter 2019
    for d in range(1, 5):
        scoholiday.append(datetime.date(2019, 1, d))
    # carnaval 2019
    for d in range(4, 9):
        scoholiday.append(datetime.date(2019, 3, d))
    # paques 2019
    for d in range(8, 20):
        scoholiday.append(datetime.date(2019, 4, d))
    # summer 2019
    for m in 7, 8:
        for d in range(1, 32):
            scoholiday.append(datetime.date(2019, m, d))
    # autumn 2019
    for d in range(28, 31):
        scoholiday.append(datetime.date(2019, 10, d))
    scoholiday.append(datetime.date(2019, 11, 1))
    # winter 2019
    for d in range(23, 32):
        scoholiday.append(datetime.date(2019, 12, d))
    # winter 2020
    for d in range(1, 4):
        scoholiday.append(datetime.date(2020, 1, d))
    # carnaval 2020
    for d in range(24, 29):
        scoholiday.append(datetime.date(2020, 2, d))
    # paques 2020
    for d in range(6, 18):
        scoholiday.append(datetime.date(2020, 4, d))
    # summer 2020
    for m in 7, 8:
        for d in range(1, 32):
            scoholiday.append(datetime.date(2020, m, d))
    # autumn 2020
    for d in range(2, 7):
        scoholiday.append(datetime.date(2020, 11, d))
    # winter 2020
    for d in range(21, 32):
        scoholiday.append(datetime.date(2020, 12, d))
    # winter 2021
    scoholiday.append(datetime.date(2021, 1, 1))
    # carnaval 2021
    for d in range(15, 20):
        scoholiday.append(datetime.date(2021, 2, d))
    # paques 2021
    for d in range(5, 17):
        scoholiday.append(datetime.date(2021, 4, d))
    # summer 2021
    for m in 7, 8:
        for d in range(1, 32):
            scoholiday.append(datetime.date(2021, m, d))
    # autumn 2021
    for d in range(1, 6):
        scoholiday.append(datetime.date(2021, 11, d))
    # winter 2021
    for d in range(27, 32):
        scoholiday.append(datetime.date(2021, 12, d))

    return scoholiday

#load weather data from json ==> not used for now
def main():
    with open('weather.json') as wth:
        wthData = json.load(wth)

        wthByHour = [[elem['main']['temp'],
                      elem['main']['pressure'],
                      elem['main']['humidity'],
                      elem['wind']['speed'],
                      elem['clouds']['all']] for elem in wthData['list']]
        print(wthByHour)

#format time data
def get_time_data(start, end):
    # day_id, leave
    # (0->6), (0->2)
    timeline = end - start
    day_list = []
    pubholiday = getPubHoliday()
    scolholiday = getScoHoliday()

    for i, e in enumerate(pubholiday):
        timelaps = e[1] - start
        pubholiday[i] = timelaps.days
    for i, e in enumerate(scolholiday):
        timelaps = e - start
        scolholiday[i] = timelaps.days
    for day in range(timeline.days):
        weekday = (start.weekday() + day) % 7

        typeofday = 0
        if day in scolholiday:
            typeofday = 1
        if day in pubholiday:
            typeofday = 2

        day_list.append([typeofday, weekday])

    return day_list

#generate fakedata to train
def get_fake_hourly_data(liste):
    liste2 = []

    for data in liste:
        temp_mean = random.randrange(-40, 300, 1) / 10
        tempday = np.arange(temp_mean - 3.5, temp_mean + 3.5, 7 / 12)
        for i, temp in enumerate(tempday):
            liste2.append([data[0], data[1], i, temp, get_client_number(data[0], data[1], i, temp)])

        for i, temp in enumerate(tempday[::-1]):
            liste2.append([data[0], data[1], i + 12, temp, get_client_number(data[0], data[1], i + 12, temp)])

    return liste2


def get_client_number(typeofday, day, hour, temp):
    # simulation du nombre de client

    # score indiquant la présence ou non de client (très peu 0 à beaucoup 8)
    score = 0
    # on ajoute le congé
    score += typeofday
    # score augmenté lundi mercredi et vdd
    if day in range(0, 5, 2):
        score += 1

    # on augmente le score aux heures de tables
    if hour in [11, 12, 13, 14, 18, 19, 20, 21, 22]:
        score += 3

    if temp > 7 and temp < 28:
        score += 1

    if temp > 14 and temp < 22:
        score += 1

    return score*15 + random.randrange(0, 20)

#save the data generated in fakedata.csv
if __name__ == '__main__':
    start_2019 = datetime.date(2019, 1, 1)
    now = datetime.date.today()

    df = pd.DataFrame(get_fake_hourly_data(get_time_data(start_2019, now)))
    df.to_csv("fakedata.csv")
