import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import schedule
import time

#open file
filename = "covid.csv"
f = open(filename, "w")
headers = "state, count, deaths, date, update time"
f.write(headers)
f.close()

def data_mining(): 
	# fetch info
	my_url = 'https://www.washingtonpost.com/graphics/local/dc-maryland-virginia-coronavirus-cases/'
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#open file
	filename = "covid.csv"
	f = open(filename, "a+")
	f.write("\n")

	# HTML parsing
	page_soup = soup(page_html, "html.parser")

	# grabs each state container
	containers = page_soup.findAll("div", {"class": "covid-state-content-wrapper"})
	update = page_soup.findAll("span", {"itemprop" : "dateModified"})[0].text.strip()
	update_date = update.split(' ')[1] + " " + update.split(' ')[2]
	update_time = update.split(' at ')[1]

	for container in containers: 
		state_name = container.findAll("p", {"class" : "covid-state-name"})[0].text.strip()
		state_count = container.findAll("p", {"class" : "covid-state-count"})[0].text.strip()
		state_death = container.findAll("p", {"class" : "covid-state-death-count"})[0].text.strip()[:-7]
		print("state: " + state_name)
		print("cases: " + state_count)
		print("deaths: " + state_death)
		print("date: " + update_date)
		print("update time: " + update_time)
		f.write(state_name + "," + state_count + "," + state_death + "," + update_date + "," + update_time + "\n")

	f.close()

schedule.every().day.at("23:59").do(data_mining)
# schedule.every().second.do(data_mining)

while True:
    schedule.run_pending()
    time.sleep(1)






	

