import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime,date
import pyowm
from pyowm import OWM
from matplotlib import rcParams
from pytz import timezone
from pyowm.utils import timestamps
from pyowm.commons.exceptions import NotFoundError


import pyowm
owm = pyowm.OWM('6dfd5610a3de02c4bc9727cdb60996fd') # generated API key | name: gforce

st.title("- Weather Forecast 🌦️")
st.write("## :white_check_mark: Created by Gaurav Pore 👨🏻‍💻 ")
st.header("Enter City name and select the Temperature Unit and Graph Type :")
place = st.text_input("NAME OF THE CITY :", "")
unit = st.selectbox("SELECT TEMPERATURE UNIT :", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("SELECT GRAPH TYPE :", ("Line Graph", "Bar Graph"))
b = st.button("SUBMIT")
st.set_option('deprecation.showPyplotGlobalUse', False)


def plot_line(days, min_t, max_t):
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 6, 4
    plt.plot(days, max_t, color='green', linestyle='dashdot', linewidth=1, marker='o', markerfacecolor='red',
             markersize=7)
    plt.plot(days, min_t, color='orange', linestyle='dashdot', linewidth=1, marker='o', markerfacecolor='blue',
             markersize=7)
    plt.ylim(min(min_t) - 4, max(max_t) + 4)
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.grid(True, color='brown')
    plt.legend(["Maximum Temperature", "Minimum Temperature"], loc=1)
    plt.xlabel('Dates(mm/dd)')
    plt.ylabel('Temperature')
    plt.title('5-Day Weather Forecast')

    for i in range(5):
        plt.text(days[i], min_t[i] - 1.5, min_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    for i in range(5):
        plt.text(days[i], max_t[i] + 0.5, max_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    # plt.show()
    # plt.savefig('figure_line.png')
    st.pyplot()
    plt.clf()




def plot_bars(days, min_t, max_t):
    # print(days)
    rcParams['figure.figsize'] = 6, 4
    days = dates.date2num(days)
    # print(days)
    min_temp_bar = plt.bar(days - 0.2, min_t, width=0.4, color='r')
    max_temp_bar = plt.bar(days + 0.2, max_t, width=0.4, color='b')
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.xlabel('Dates(mm/dd)')
    plt.ylabel('Temperature')
    plt.title('5-Day Weather Forecast')

    for bar_chart in [min_temp_bar, max_temp_bar]:
        for index, bar in enumerate(bar_chart):
            height = bar.get_height()
            xpos = bar.get_x() + bar.get_width() / 2.0
            ypos = height
            label_text = str(int(height))
            plt.text(xpos, ypos, label_text,
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     color='black')

    st.pyplot()
    plt.clf()

def find_min_max(place, unit, g_type):
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    temperature = weather.temperature(unit='celsius')['temp']
    if unit == 'Celsius':
        unit_c = 'celsius'
    else:
        unit_c = 'fahrenheit'

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_2:
            dates_2.append(date)
            min_t.append(None)
            max_t.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1] = temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1] = temperature
    # days = dates.date2num(days)
    # plt.xticks(days)
    # return days,min_t,max_t
    # print(f"| Minimum Temperature in {unit_c} for {place} is |",min_t)
    # print(f"| Maximum Temperature in {unit_c} for {place} is |",max_t)
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.title(f"Details for {place} currently:")
    if unit_c == 'celsius':
        st.write(f"## Temperature: {temperature} °C")
    else:
        st.write(f"## Temperature: {temperature} F")
    st.write(f"### Sky : {weather.detailed_status}")
    st.write(f"### Wind Speed : {weather.wind()['speed']} mph")
    st.write(f"### Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")

    st.title("Expected Temperature Changes/Alerts:")
    if forecaster.will_have_fog():
        st.write("### FOG ALERT 🌁")
    if forecaster.will_have_rain():
        st.write("### RAINY SCENES ☔")
    if forecaster.will_have_storm():
        st.write("### STORM ALERT ⛈")
    if forecaster.will_have_snow():
        st.write("### SNOW ALERT❄")
    if forecaster.will_have_tornado():
        st.write("### TORNADO ALERT 🌪️")
    if forecaster.will_have_hurricane():
        st.write("### HURRICANE ALERT 🌀")
    if forecaster.will_have_clouds():
        st.write("### CLOUDY SKIES ⛅")
    if forecaster.will_have_clear():
        st.write("### CLEAR WEATHER PREDICTED 🌞")

    if g_type == "Line Graph":
        plot_line(days, min_t, max_t)
    elif g_type == "Bar Graph":
        plot_bars(days, min_t, max_t)

    i = 0
    st.write(f"#    Date :  Max - Min  ({unit})")
    for obj in days:
        d = (obj.strftime("%d/%m"))
        st.write(f"### \v {d} :\t  ({max_t[i]} - {min_t[i]})")
        i += 1

def find_min_max_pin(pin, unit, g_type):
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    if str(pin) == '410222' or str(pin) == '410207':
          forecaster = mgr.forecast_at_coords(18.8931, 73.1701,'3h')
          forecast = forecaster.forecast
    obs = mgr.weather_at_zip_code(str(pin),'in')
    weather = obs.weather
    temperature = weather.temperature(unit='celsius')['temp']
    if unit == 'Celsius':
        unit_c = 'celsius'
    else:
        unit_c = 'fahrenheit'
    if str(pin) == '410222' or str(pin) == '410207':
         for weather in forecast:
             day = datetime.utcfromtimestamp(weather.reference_time())
             date = day.date()
             if date not in dates_2:
                 dates_2.append(date)
                 min_t.append(None)
                 max_t.append(None)
                 days.append(date)
             temperature = weather.temperature(unit_c)['temp']
             if not min_t[-1] or temperature < min_t[-1]:
                 min_t[-1] = temperature
             if not max_t[-1] or temperature > max_t[-1]:
                 max_t[-1] = temperature
    # days = dates.date2num(days)
    # plt.xticks(days)
    # return days,min_t,max_t
    # print(f"| Minimum Temperature in {unit_c} for {place} is |",min_t)
    # print(f"| Maximum Temperature in {unit_c} for {place} is |",max_t)
    obs = mgr.weather_at_zip_code(str(pin),'in')
    weather = obs.weather
    st.title(f"Details for {place} currently:")
    if unit_c == 'celsius':
        st.write(f"## Temperature: {temperature} °C")
    else:
        st.write(f"## Temperature: {temperature} F")
    st.write(f"### Sky : {weather.detailed_status}")
    st.write(f"### Wind Speed : {weather.wind()['speed']} mph")
    st.write(f"### Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")

    if str(pin) == '410222' or str(pin) == '410207':
         st.title("Expected Temperature Changes/Alerts:")
         if forecaster.will_have_fog():
             st.write("### FOG ALERT 🌁")
         if forecaster.will_have_rain():
             st.write("### RAINY SCENES ☔")
         if forecaster.will_have_storm():
             st.write("### STORM ALERT ⛈")
         if forecaster.will_have_snow():
             st.write("### SNOW ALERT❄")
         if forecaster.will_have_tornado():
             st.write("### TORNADO ALERT 🌪️")
         if forecaster.will_have_hurricane():
             st.write("### HURRICANE ALERT 🌀")
         if forecaster.will_have_clouds():
             st.write("### CLOUDY SKIES ⛅")
         if forecaster.will_have_clear():
             st.write("### CLEAR WEATHER PREDICTED 🌞")
    st.title("5-Day Weather Forecast: ")
    if str(pin) == '410222' or str(pin) == '410207':
        if g_type == "Line Graph":
                  plot_line(days, min_t, max_t)
        elif g_type == "Bar Graph":
                 plot_bars(days, min_t, max_t)
    if str(pin) == '410222' or str(pin) == '410207':
         i = 0
         st.write(f"#    Date :  Max - Min  ({unit})")
         for obj in days:
             d = (obj.strftime("%d/%m"))
             st.write(f"### \v {d} :\t  ({max_t[i]} - {min_t[i]})")
             i += 1


if b:

    if place != "":
        try :
            find_min_max(place, unit, g_type)
        except NotFoundError:
             st.write("#### Sorry, City not found! Please enter PIN CODE of your place!")

st.subheader('Note: Enter PIN CODE only* if City is not found ')
pincode = st.text_input("ENTER PIN CODE :")
d = st.button("SUBMIT PIN CODE")
if d:
    find_min_max_pin(str(pincode),unit,g_type)



















