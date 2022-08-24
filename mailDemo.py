import os
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
import requests

#Gets info from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_USER') 
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


def getWeather():
 #Website to scrape information
    url = "https://weather.com/weather/today/l/ed83f6e97ad12bbd81cbca2c55a3d6cacbac193c9d2a79565531c166d24cfc2a"

    #Gets the info of the url
    results = requests.get(url)
    information = BeautifulSoup(results.text, "html.parser")
    
    #Scrapes website for value in parameters
    day = information.find(text = "Today's Forecast for Plainfield, NJ")
    temp = information.find(class_ = "styles--temperature--3MBn3")
    finishedTemp = temp.text
    finishedTemp = finishedTemp.strip("°")

    #Only gets the text of the element tags
    return day.text + " is "+ finishedTemp + " degrees. -Automated Program"

weatherToday = getWeather()

#Information of sender
msg = EmailMessage()
msg['Subject'] = 'Hello'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'Enter phone number here'

#Sends out sms message
msg.set_content(weatherToday)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
