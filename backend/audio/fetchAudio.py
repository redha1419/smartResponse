import time
import base64
import requests
import json
import os
import sys


def fetch_audio_file(n, token):

    #for step 1
    audio_asset = "8f383e96-823d-48db-8053-85cafb290413"
    time_stamp = int(time.time()*1000) - 10000
    URL_1 = "https://hamilton.cityiq.io/api/v2/media/ondemand/assets/"+audio_asset+"/media?mediaType=AUDIO&timestamp=" + str(int(time_stamp))
    HEADERS = {'Authorization':'Bearer '+token, 'Predix-Zone-Id': 'HAMILTON-IE-AUDIO'}
    r_1 = requests.get(URL_1, headers = HEADERS) 
    data_1 = r_1.json() 

    time.sleep(2)

    #for step 2
    URL_2 = data_1['pollUrl']
    r_2 = requests.get(URL_2, headers=HEADERS)
    data_2 = r_2.json()


    time.sleep(2)

    #for step 3
    #print data_2['listOfEntries']['content'][0]
    URL_3 = str(data_2['listOfEntries']['content'][0]['url'])
    

    r_3 = requests.get(URL_3, headers=HEADERS)
    open('./temp/sample_'+str(n)+'.flac', 'wb').write(r_3.content)

def fetch_token():

    url = 'https://auth.aa.cityiq.io/oauth/token?grant_type=client_credentials'

    username = 'Hackathon.CITM.Hamilton'
    password = 'Wm,yb&G`KB\\2}d<s'

    response = requests.get(url, auth=(username, password))
    data = response.json()

    return data['access_token']




def main(name):
    #create an audio file directory
    path = './temp'

    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    #token = fetch_token
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI2NWVjZTliMDdlNjY0MGU3ODFiYjk4OGUwMmI3ZTdiOSIsInN1YiI6IkhhY2thdGhvbi5DSVRNLkhhbWlsdG9uIiwiYXV0aG9yaXRpZXMiOlsiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1QRURFU1RSSUFOLklFLVBFREVTVFJJQU4uTElNSVRFRC5ERVZFTE9QIiwidWFhLnJlc291cmNlIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1QQVJLSU5HLklFLVBBUktJTkcuTElNSVRFRC5ERVZFTE9QIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1CSUNZQ0xFLklFLUJJQ1lDTEUuTElNSVRFRC5ERVZFTE9QIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1UUkFGRklDLklFLVRSQUZGSUMuTElNSVRFRC5ERVZFTE9QIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1FTlZJUk9OTUVOVEFMLklFLUVOVklST05NRU5UQUwuTElNSVRFRC5ERVZFTE9QIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1JTUFHRS5JRS1JTUFHRS5MSU1JVEVELkRFVkVMT1AiLCJpZS1jdXJyZW50LkhBTUlMVE9OLUlFLVZJREVPLklFLVZJREVPLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtQVVESU8uSUUtQVVESU8uTElNSVRFRC5ERVZFTE9QIl0sInNjb3BlIjpbImllLWN1cnJlbnQuSEFNSUxUT04tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCIsInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtQklDWUNMRS5JRS1CSUNZQ0xFLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtSU1BR0UuSUUtSU1BR0UuTElNSVRFRC5ERVZFTE9QIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1WSURFTy5JRS1WSURFTy5MSU1JVEVELkRFVkVMT1AiLCJpZS1jdXJyZW50LkhBTUlMVE9OLUlFLUFVRElPLklFLUFVRElPLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJIYWNrYXRob24uQ0lUTS5IYW1pbHRvbiIsImNpZCI6IkhhY2thdGhvbi5DSVRNLkhhbWlsdG9uIiwiYXpwIjoiSGFja2F0aG9uLkNJVE0uSGFtaWx0b24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjliM2ZmYjhhIiwiaWF0IjoxNTc5OTg3NzcyLCJleHAiOjE1ODA1OTI1NzIsImlzcyI6Imh0dHBzOi8vYXV0aC5hYS5jaXR5aXEuaW8vb2F1dGgvdG9rZW4iLCJ6aWQiOiJ1YWEiLCJhdWQiOlsiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1JTUFHRS5JRS1JTUFHRS5MSU1JVEVEIiwiSGFja2F0aG9uLkNJVE0uSGFtaWx0b24iLCJpZS1jdXJyZW50LkhBTUlMVE9OLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1CSUNZQ0xFLklFLUJJQ1lDTEUuTElNSVRFRCIsInVhYSIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtQVVESU8uSUUtQVVESU8uTElNSVRFRCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQiLCJpZS1jdXJyZW50LkhBTUlMVE9OLUlFLVRSQUZGSUMuSUUtVFJBRkZJQy5MSU1JVEVEIiwiaWUtY3VycmVudC5IQU1JTFRPTi1JRS1FTlZJUk9OTUVOVEFMLklFLUVOVklST05NRU5UQUwuTElNSVRFRCIsImllLWN1cnJlbnQuSEFNSUxUT04tSUUtVklERU8uSUUtVklERU8uTElNSVRFRCJdfQ.kmAIw5Rf32eRiMsDB-cxphznHZe2cSIUlilmSYcXnZih6clLFYCsQb028FxiAKP76SwitENYypXnQVQXm_q_90hnYDQ80TGxqZ6bKAg9gD8DiqoEy2SeTN_55kDRApcWkezVl61fjj7U0_wXAOCX9gZj89065Yf8M5u1tJdhko8dtNWpwyBPyeozBE9uSZfWsxc04Ar-6jlWREfWOse_239_RDXQtAiLsp9PywZxL7ZCF0KoEYFMlQmKE5lU6sXBw9RQQtGJ1_5JtefKgB35kE-dhjfLozNY6LIQomlt_q5fbX4ML_ZwlGybC52p1zJeMoNT47q_GqeOYL-hPpHQgYi_oIGeyuQmAHVCgz3lmvLhFRS91bK42ChL3zlP7Emv81Q44xxYwalK0oZ7IkkZ4nmgToSKEsa0WOMjpjctc4tSn2JW628KAepaPc2VPl7bIrAjlqXH0Flf8Rtv8DtBY0VMzRgQEfe9JfCZM9yg3zif_85l-BtpZarQ_-7JDpARb7iKf7jpaIhjnIZy3bRf-kw2MeUpUIzlA9WHI4v1zXdx4jA5-EY-0kU4kn9YLd7f7um_eXfbDotU0D_vIxM_PmefESJGRdB268CkcxoACP2IMi4DWB8ZiDJ2lbajt_Q3tCIMYkHwidgT594GSc-PqWeE19PSFT8QLL4MhYqhBkg'
    fetch_audio_file(name, token)



main(sys.argv[1])