#!/usr/bin/python
import requests, json, time, re
from httplib2 import Http
from json import dumps
##EXPORT CONTACT LIST FROM GOOGLE IN CSV FORMAT, THEN CONVERT TO JSON USING THE FOLLOWING SITE: https://www.csvjson.com/csv2json
##SAVE THE FILE AND EDIT THE VARIABLE "_EMAILSJSON" WITH THE ABOSOLUTE PATH TO THE FILE
##EDIT THE VARIABLE _DOMAIN WITH YOUR DOMAIN NAME
_EMAILSJSON = '<INSERT FILE PATH HERE>'
_DOMAIN = ".*<INSERT DOMAIN NAME HERE>"

emails = open(_EMAILSJSON)
emails = json.loads(emails.read())

for x in emails:
 email = x['E-mail 1 - Value']
 url = "https://haveibeenpwned.com/api/v2/breachedaccount/%s" % (email)
 if re.search(r'%s' % (_DOMAIN), url):
  headers = {
      'Accept': "application/vnd.haveibeenpwned.v2+json",
      'Cache-Control': "no-cache",
      'Postman-Token': "efefb833-bc90-47e0-bc66-68938b7f95ac"
      }
  response = requests.request("GET", url, headers=headers)
  time.sleep(2)
##FOR TESTING PURPOSES TO SEE IF YOUR REQUEST IS GOING THROUGH. ANYTHING OTHER THAN 200 OR 404 YOU HAVE BEEN BLOCKED BY THE SITE.
##TO PREVENT THIS DO NOT REMOVE THE time.sleep(2) ABOVE. REQUESTS FASTER THAN 1.5 SECONDS TO THE API RESULTS IN BEING BLOCKED.
#  print response.status_code
#  print response.text
  if response.status_code == 200:
   emails2 = json.loads(response.text)
   for x in emails2:
    emails2 = "Email: " + email + "\n" + "Title: " + x["Title"] + "\n" + "Description: " + x["Description"] + "\n"
    emails2 = re.sub('<a \S*\s\S*\s\S*>', '', emails2)
    emails2 = re.sub('<\/\S*>', '', emails2)
    emails2 = re.sub('(?<!\S)<\S*>(?=\S)', '', emails2)
#    print emails2
##THE VARIABLE 'emails2' CONTAINS THE INFORMATION GATHERED.
##IF USING GOOGLE CHAT TO ALERT UNCOMMENT THE BELOW AND EDIT THE "url" VARIABLE TO YOUR WEBHOOK URL
#    headers2 = {'Content-Type': 'application/json'}
#    url = "<INSERT GOOGLE WEBHOOK URL HERE>"
#    msg = { 'text': "\n      *Compromised Email Account*" + "\n" + '%s' % (emails2) }
#    response = Http().request(
#     uri=url,
#     method='POST',
#     headers=headers2,
#     body=dumps(msg)
#    )
