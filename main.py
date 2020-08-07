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
from urllib.request import urlopen, Request  # fetch file from url
import geopy  # geocoding (get coordinates of locations)
import matplotlib.pyplot as plt  # plotting
from geopy.geocoders import Nominatim  # specific geocoder
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from symbolDict import symbols  # map of symbol names to emoji
from statistics import mean


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
    locator = Nominatim(user_agent="github:sgango/metemail")
    loc = locator.geocode(locationstring)  # find place and get coordinates

    return email, password, recipient, loc, locationstring


def get_weather(loc):
    """Fetch weather data from Meteorologisk Institutt.
    """
    url = (f"https://api.met.no/weatherapi/locationforecast/"
        f"2.0/compact?lat={loc.latitude}&lon={loc.longitude}")

    with urlopen(Request(url,  # user agent to identify ourselves to met.no
            headers={'User-Agent': 'github:sgango/metemail'})) as fp:
        forecast = json.load(fp)  # convert JSON to Python dictionary

    return forecast


def meteogram(forecast, locationstring):
    """Read datetime and precip/temp values
    from dictionary, and plot meteogram.
    Gets weather for next 24 hours.
    """
    times = []
    precip = []
    temps = []
    for i in range(24):
        # iterate through dict, get values from first 24 timeseries
        times.append(forecast["properties"]["timeseries"][i]["time"])
        precip.append((forecast["properties"]["timeseries"][i]["data"]
            ["next_1_hours"]["details"]["precipitation_amount"]))
        temps.append((forecast["properties"]["timeseries"][i]["data"]
            ["instant"]["details"]["air_temperature"]))

    fig, ax1 = plt.subplots()
    ax1.bar(times, precip, color='blue')
    ax1.set_ylabel('Precipitation (mm)', color='blue')

    ax2 = ax1.twinx()  # new set of axes, shared x-axis
    ax2.plot(times, temps, color='red')
    ax2.set_ylabel('Temperature (Celsius)', color='red')

    ax1.set_xlabel('Time')
    for lbl in ax1.axes.xaxis.get_ticklabels()[::2]:
        lbl.set_visible(False)  # hide alternate labels for neatness
    hours = [i[11:13] for i in times]  # slice datetime strings
    ax1.set_xticklabels(hours)  # use hours only for x-labels

    fig.tight_layout()  # make sure everything fits nicely
    plt.title(f"Today's meteogram for {locationstring.title()}")
    plt.savefig('meteo.png', dpi=1000, bbox_inches='tight')


def send_email(loc, email, password, recipient, forecast):
    """Log into server and send an email with forecast.
    """
    symbs = []
    for i in range(6):
        symbs.append((forecast["properties"]["timeseries"]
            [i]["data"]["next_1_hours"]["summary"]["symbol_code"]))
    emoji = [symbols[symbol] for symbol in symbs]

    precipitation = (forecast["properties"]["timeseries"][0]["data"]
        ["next_6_hours"]["details"]["precipitation_amount"])
    if precipitation > 0:
        precip_msg = (
            f"Looks like it's going to rain! {precipitation} mm of "
            f"precipitation is forecast."
            )
    else:
        precip_msg = "Looks like it'll be dry! No rain is forecast."
    
    temps = []
    for i in range(6):
        temps.append((forecast["properties"]["timeseries"][i]["data"]
            ["instant"]["details"]["air_temperature"]))
    temp_mean = mean(temps)
    if temp_mean < 0:
        temp_phrase = "freezing ⛄"
    elif 0 < temp_mean <= 5:
        temp_phrase = "cold ❄"
    elif 5 < temp_mean <= 10:
        temp_phrase = "quite chilly"
    elif 10 < temp_mean <= 15:
        temp_phrase = "cool"
    elif 15 < temp_mean <= 25:
        temp_phrase = "warm"
    elif 25 < temp_mean <= 32:
        temp_phrase = "hot 🌞"
    elif temp_mean > 32:
        temp_phrase = "very hot 🥵"
    else:
        temp_phrase = ""
    temp_msg = f"Avg. temperature: {temp_mean:.2f} \u00b0C - {temp_phrase}."

    winds = []
    for i in range(6):
        winds.append((forecast["properties"]["timeseries"][i]["data"]
            ["instant"]["details"]["wind_speed"]))
    wind_mean = mean(winds)
    wind_mean *= 2.237  # convert ms^-1 to mph
    if 0 <= wind_mean <= 3:
        wind_phrase = "calm"
    elif 3 < wind_mean <= 12:
        wind_phrase = "a bit breezy 🍃"
    elif 12 < wind_mean <= 24:
        wind_phrase = "quite breezy 🍃"
    elif 24 < wind_mean <= 38:
        wind_phrase = "very strong winds 🌬"
    elif wind_mean > 38:
        wind_phrase = "extremely strong winds 🌬"
    else:
        wind_phrase = ""
    wind_msg = f"Avg. windspeed: {wind_mean:.2f} mph - {wind_phrase}."

    msg = MIMEMultipart()
    msg['Subject'] = "Weather report"
    msg['From'] = email
    msg['To'] = recipient

    text = MIMEText(
        f"Next six hours:\n{'  '.join(emoji)}\n\n"
        f"{precip_msg}\n"
        f"{temp_msg}\n"
        f"{wind_msg}\n\n"
        f"Check the attached meteogram for details.\n\n"
        f"Location: {loc.address}\n"
        f"Data from the Norwegian Meteorological Institute.\n"
        )
    msg.attach(text)

    img_data = open('meteo.png', 'rb').read()
    image = MIMEImage(img_data, name='meteo.png')
    msg.attach(image)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipient, msg.as_string())
        server.quit()


if __name__ == "__main__":
    email, password, recipient, loc, locationstring = env_setup()
    forecast = get_weather(loc)
    meteogram(forecast, locationstring)
    send_email(loc, email, password, recipient, forecast)
