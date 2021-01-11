import smtplib
import credentials
import datetime as dt
from pip._vendor import requests
import time

MY_LAT = "49.2827"
MY_LNG = "123.1207"

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}


def get_iss_station():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    lng = float(response.json()["iss_position"]["longitude"])
    lat = float(response.json()["iss_position"]["latitude"])
    return(lng, lat)


def get_sunrise_sunset():
    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sunrise = response.json()["results"]["sunrise"]
    sunset = response.json()["results"]["sunset"]
    sunrise = int(sunrise.split("T")[1].split(":")[0])
    sunset = int(sunset.split("T")[1].split(":")[0])
    return (sunrise, sunset)


def check_postions(iss_position):
    if iss_position[0] >= float(MY_LNG)-5.00 and iss_position[0] <= float(MY_LNG)+5.00 and iss_position[1] >= float(MY_LAT)-5.00 and iss_position[1] <= float(MY_LAT)+5.00:
        print("ISS is in the margin of the coordinated")
        return True
    else:
        print("ISS is too far")
        return False


def check_time(sunrise_sunset):
    now = dt.datetime.now()
    if sunrise_sunset[0] <= now.hour and sunrise_sunset[1] >= now.hour:
        print("It is right time")
        return True
    else:
        print("It is too bright")
        return False


def send_email(subject,  email_body):
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=credentials.sender_email,
                         password=credentials.password)
        connection.sendmail(
            from_addr=credentials.sender_email,
            to_addrs=credentials.recepient_email,
            msg=f"Subject:Happy Birthday!\n\n{email_body}"
        )


def main():
    subject = "ISS is above you"
    email_body = "ISS is above you, look out now!"
    while True:
        iss_coords = get_iss_station()
        sunrise_sunset_time = get_sunrise_sunset()
        if check_postions(iss_coords) and check_time(sunrise_sunset_time):
            print("ISS is above you! Look out now!")
            send_email(subject, email_body)
        else:
            print("You won't see ISS")
        time.sleep(60)


main()
# print(get_sunset())
