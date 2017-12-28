import json

from selenium import webdriver

import settings as settings

driver = webdriver.Chrome()
jquery_js = open('jquery.js', 'r')
jquery = jquery_js.read()

data = {}

driver.get(settings.all_stations_url)
driver.execute_script(jquery)
hrefs = driver.execute_script("""
	hrefs = [];
	$('.stops-all a').each(function(num, item){
		hrefs.push($(item).attr('href'))
	})
	return hrefs;
	""")
for href in hrefs:
	driver.get(settings.short_station_url.format(href))
	driver.execute_script(jquery)
	page_data = driver.execute_script("""
	var data = [];
	$('.proute').each(function(num, item){
		var bus = {
			"href":$(item).find('.href').attr('href'),
			"station":$(item).find('a').html(),
			"direction":$(item).find('.direction').html()
		}; 
		data.push(bus);
	});
	return data;
	""")

	if page_data:
		data[page_data[0]['station']] = page_data
	else:
		print(href)

json_file = open(settings.stations_file, 'w', encoding = "utf-8")
json.dump(data, json_file, ensure_ascii = False)
