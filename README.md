![image](https://user-images.githubusercontent.com/25332542/89449833-9035f700-d751-11ea-94ed-97cc0a18f693.png)

= "meteogram" + "email"  
*(meteomail, metmail, mailgram etc. were all taken)*

**A simple Python app which sends a daily meteogram and emoji summary.**  
Get a clear, concise forecast in your inbox every morning. 

## Example email

<img src="https://user-images.githubusercontent.com/25332542/89578548-35240300-d82a-11ea-9bbc-a3bad815c908.png" width="600">

### Example meteogram

<img src="https://user-images.githubusercontent.com/25332542/89579684-20486f00-d82c-11ea-975a-731bb0623f3f.png" width="600">

## Usage

In normal use, the environment variables `EMAIL`, `PASSWORD`, `RECIPIENT` and `LOCATION` should be set. The script can then run on a schedule, for example using GitHub Actions. For testing purposes, if the environment variables are not set, the script will prompt the user and read from standard input.  
See [the original instructions](https://github.com/ImperialCollegeLondon/whatever-the-weather/blob/main/README.md) for more details.

`LOCATION` should simply be a string referencing any location on Earth, such as `south kensington`. For common placenames, you may need to use a more precise string to select the intended location.

## Requirements

Tested using:

* python 3.8.3
* geopy 2.0.0
* matplotlib 3.2.2

but should work with any recent versions.

*Based on [example code from Mark Woodbridge](https://github.com/ImperialCollegeLondon/whatever-the-weather).*
