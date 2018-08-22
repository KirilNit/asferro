import requests
from selenium import webdriver
from elasticsearch import Elasticsearch


url = "http://www.openweathermap.org/data/2.5/weather"
#London,uk
querystring = {"q":"London,uk","appid":"b6907d289e10d714a6e88b30761fae22"}

headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "c1e75b8f-0365-40ae-a6b1-9f472d04bbf7"
    }
es = Elasticsearch([{'host':'localhost', 'port':9200}])
response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)
api_humy = response.json()['main']['humidity']
#print('The London\'s humidity on Today is:', api_humy)
#send value in ES
weather=es.index(index ='weather1',doc_type='weather_city',id=1,body=response)
#weather_out=es.get(index='weather1',doc_type='weather_city',id =1)
#print(weather_out)

#=================Selenium's part

driver = webdriver.Chrome()

driver.get('https://openweathermap.org/city/2643743')
humidity = driver.find_element_by_xpath("//td[text()='Humidity']/following-sibling::td")
value_humidity = humidity.text
#send value in ES
sel_humidity = es.index(index ='weather1',doc_type='weather_city',id=2,body=value_humidity)
driver.quit()

#assertion 2 values

get_api_humidity = es.get(index ='weather1',doc_type='weather_city',id=1)

get_selenium_humidity = es.get(index ='weather1',doc_type='weather_city',id=2)

assert get_api_humidity['main']['humidity'] == get_selenium_humidity, 'Not ='

