#!/usr/bin/env python

import datetime #for knowing when the data get saved
import requests #for getting the page
from bs4 import BeautifulSoup #for parsing the page

#settings
url='http://192.168.88.161'
username = 'pvserver'
password = 'pvwr'

{
    "time_datetime_object" : {
        "aktualni[W]" : 0,
        "denni_energie[kWh]" : 0,
        "energie_celkem[kWh]" : 0,
        "fv_generator_string1_napeti[V]" : 0,
        "fv_generator_string1_proud[A]" : 0,
        "fv_generator_string2_napeti[V]" : 0,
        "fv_generator_string2_proud[A]" : 0,
        "fv_generator_string3_napeti[V]" : 0,
        "fv_generator_string3_proud[A]" : 0,
        "vystupni_vykon_l1_napeti[V]" : 0,
        "vystupni_vykon_l1_vykon[W]" : 0,
        "vystupni_vykon_l2_napeti[V]" : 0,
        "vystupni_vykon_l2_vykon[W]" : 0,
        "vystupni_vykon_l3_napeti[V]" : 0,
        "vystupni_vykon_l3_vykon[W]" : 0
        }
}

def get_payload():
    #returns content of piko server, encoded to cp1252 for czech language
    #returns also time of the requests
    r = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
    if r.ok:
        r.encoding='cp1252'
        payload = r.content
        time = datetime.datetime.now()
        return time, payload

def unpack_payload(time, payload):
    result = {}
    #maybe convert
    #time = time.strftime('%Y-%m-%d %H:%M:%S')
    result[time] = {}

    soup = BeautifulSoup(payload, 'html.parser')
    #split the code row by row
    rows = soup.find_all('tr')

    #HARDCODED
    actual_and_total = [element for element in rows[6]]
    result[time]["aktualni[W]"] = actual_and_total[5].text.strip()
    result[time]["energie_celkem[kWH]"] = actual_and_total[11].text.strip()
    daily_energy = [element for element in rows[8]]
    result[time]["denni_energie[kWh]"] = daily_energy[11].text.strip() 
    
    return result

    #next table
    #result[time]["fv_generator_string1_napeti[V]"] = elements[11].text.strip()
    #result[time]["fv_generator_string1_proud[A]"] = elements[11].text.strip()
    #result[time]["fv_generator_string2_napeti[V]"] = elements[11].text.strip()
    #result[time]["fv_generator_string2_proud[A]"] = elements[11].text.strip()
    #result[time]["fv_generator_string3_napeti[V]"] = elements[11].text.strip()
    #result[time]["fv_generator_string3_proud[A]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l1_napeti[V]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l1_vykon[W]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l2_napeti[V]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l2_vykon[W]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l3_napeti[V]"] = elements[11].text.strip()
    #result[time]["vystupni_vykon_l3_vykon[W]"] = elements[11].text.strip()

def main():
    time, payload = get_payload()
    print(unpack_payload(time, payload))

if __name__ == '__main__':
    main()
