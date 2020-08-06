![image](https://user-images.githubusercontent.com/25332542/89449833-9035f700-d751-11ea-94ed-97cc0a18f693.png)

= "meteogram" + "email"  
*(meteomail, metmail and mailgram were all taken)*

**A simple Python app which sends a daily meteogram and emoji summary.**  
Get a clear, concise forecast in your inbox every morning. 

## Example email

<img src="https://user-images.githubusercontent.com/25332542/89591944-58a77780-d843-11ea-96d8-1f76ec613447.png" width="400">

The body of the email features an emoji summary of the upcoming weather conditions, helping you know what's ahead at a glance.

### Example meteogram

<img src="https://user-images.githubusercontent.com/25332542/89579684-20486f00-d82c-11ea-975a-731bb0623f3f.png" width="500">

The meteogram, attached to every email, shows an easy-to-read graphical representation of the temperature and precipitation over the next 24 hours, giving a clear and detailed overview of what to expect. 

## Usage

In normal use, the environment variables `EMAIL`, `PASSWORD`, `RECIPIENT` and `LOCATION` should be set. The script can then run on a schedule, for example using GitHub Actions. For testing purposes, if the environment variables are not set, the script will prompt the user and read from standard input.  
See [the original instructions](https://github.com/ImperialCollegeLondon/whatever-the-weather/blob/main/README.md) for more details.

`LOCATION` should simply be a string referencing any location on Earth, such as `south kensington`. For some placenames, you may need to use a more precise string to select the intended location (e.g. `new york, tyne and wear, UK`).

## Requirements

Tested using:

* python 3.8.3
* geopy 2.0.0
* matplotlib 3.2.2

but should work with any recent versions.

*Based on [example code from Mark Woodbridge](https://github.com/ImperialCollegeLondon/whatever-the-weather).*
