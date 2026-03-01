import time
import requests
import smtplib
from datetime import datetime, timezone, timedelta
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
MY_LAT = 18.9810
MY_LONG =73.0309

print("EMAIL:", MY_EMAIL)
print("PASSWORD:", MY_PASSWORD)




#----------------------getting ISS current position from iss  API-----------#
def iss_overhead():
	iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
	iss_response.raise_for_status()

	dt= iss_response.json()

	current_position = dt["iss_position"]

	iss_lat = float(current_position["latitude"])
	iss_long = float(current_position["longitude"])

	print(f"ISS latitude:{iss_lat},\nISS longitude:{iss_long}")

	if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LONG - 5 <= iss_long <= MY_LONG + 5:
		return True

	return False
#----------------------getting sunrise and sunset hours from sunrise-sunset API-----------#
def is_night_time():
	parameters = {
		"lat" : MY_LAT,
		"lng" : MY_LONG,
		"formatted" : 0,
		"tzid" :"Asia/Kolkata"

	}
	response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)

	response.raise_for_status()
	data = response.json()

	sunrise = data["results"]["sunrise"].split("T")
	sunset = data["results"]["sunset"].split("T")

	sunrise_hour = sunrise[1][:2]
	sunset_hour = sunset[1][:2]
	time_now = datetime.now().hour

	if time_now > sunset_hour or time_now < sunrise_hour:
		return True

	print(f"Sunset hour : {sunrise_hour},\nSunset hour : {sunset_hour},\nCurrent Hour : {time_now}")


#----------if your position is within +5 and -5 degree of the ISS position  and it is dark(time>19 hrs) the send an email notification that lookup at the sky----#

while True:

	time.sleep(120)
	if iss_overhead() and is_night_time() :
		connection = smtplib.SMTP("smtp.gmail.com", 587)
		connection.starttls()
		connection.login(MY_EMAIL, MY_PASSWORD)
		connection.sendmail(
			from_addr=MY_EMAIL,
			to_addrs =MY_EMAIL,
			msg ="Subject:Look up ! \n\n Dear Girish,\nThe ISS is above you in the sky.\n\n Regards,\nGirish"
		)
