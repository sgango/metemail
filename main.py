"""
Author: Srayan Gangopadhyay
2020-07-23
Adapted from MIT-licensed code by Mark Woodbridge
"""

import getpass  # for secure password retrieval
import json  # handling JSON file from met.no
import os  # access environment variables
import smtplib  # send emails
import ssl  # network stuff (for emails)
import urllib.request  # fetch file from url
import geopy  # geocoding (get coordinates of locations)
import matplotlib.pyplot as plt  # plotting
from geopy.geocoders import Nominatim


def env_setup():
    """Get parameters from environment variables if present,
    otherwise get them from stdin.
    """
    # EMAIL PARAMETERS
    email = (os.environ["EMAIL"] if "EMAIL" in os.environ 
        else input("Log in to send an email.\nEmail: "))

    password = (os.environ["PASSWORD"] if "PASSWORD" in os.environ 
        else getpass.getpass(prompt='Password: '))

    recipient = (os.environ["RECIPIENT"] if "RECIPIENT" in os.environ 
        else input("Recipient email: "))

    # LOCATION SETTING
    locationstring = (os.environ["LOCATION"] if "LOCATION" in os.environ 
        else input("Location: "))
    locator = Nominatim(user_agent="github:sgango/whatever-the-weather")
    loc = locator.geocode(locationstring)  # find place and get coordinates    
    
    return email, password, recipient, loc, locationstring


def get_weather(loc):
    """Fetch weather data from Meteorologisk Institutt.
    """
    url = (f"https://api.met.no/weatherapi/locationforecast/"
        f"2.0/compact?lat={loc.latitude}&lon={loc.longitude}")

    with urllib.request.urlopen(url) as fp:
        forecast = json.load(fp)  # convert JSON to Python dictionary
        precipitation = (forecast["properties"]["timeseries"][0]["data"]
            ["next_6_hours"]["details"]["precipitation_amount"])

    return precipitation, forecast


def meteogram(forecast, locationstring):
    """Read datetime and precip/temp values
    from dictionary, and plot meteogram.
    Gets weather for next 24 hours.
    """
    times = []
    precip = []
    temps = []
    for i in range(24):
        # iterate through dict, get vals from first 24 timeseries
        times.append(forecast["properties"]["timeseries"][i]["time"])
        precip.append((forecast["properties"]["timeseries"][i]["data"]
            ["next_1_hours"]["details"]["precipitation_amount"]))
        temps.append((forecast["properties"]["timeseries"][i]["data"]
            ["instant"]["details"]["air_temperature"]))
    
    fig, ax1 = plt.subplots()
    ax1.plot(times, temps, color='red')    
    ax1.set_ylabel('Temperature (Celsius)', color='red')

    ax2 = ax1.twinx()  # new set of axes, shared x-axis
    ax2.bar(times, precip, color='blue')
    ax2.set_ylabel('Precipitation (mm)', color='blue')

    ax1.set_xlabel('Time')
    for lbl in ax1.axes.xaxis.get_ticklabels()[::2]:
        lbl.set_visible(False)  # hide alternate labels for neatness
    hours = [i[11:13] for i in times]  # slice datetime strings
    ax1.set_xticklabels(hours)  # use hours only for x-labels
    fig.tight_layout()  # make sure everything fits nicely
    plt.title(f"Today's meteogram for {locationstring}")
    plt.show()  # FOR DEVELOPMENT ONLY


def send_email(precipitation, loc, email, password, recipient):
    """Log into server and send an email with precipitation forecast.
    """
    msg = (f"Subject: Don\'t forget your umbrella!\n"
        f"\n{precipitation}mm of precipitation is forecast in {loc.address}"
        f" in the next six hours.")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
        server.login(email, password)
        # TODO: save meteogram and attach to email
        server.sendmail(email, recipient, msg)


if __name__ == "__main__":
    email, password, recipient, loc, locationstring = env_setup()
    precipitation, forecast = get_weather(loc)
    if precipitation > 0:
        send_email(precipitation, loc, email, password, recipient)
    meteogram(forecast, locationstring)  # FOR DEVELOPMENT ONLY
