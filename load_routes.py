import json

from selenium import webdriver
import settings as settings

driver = webdriver.Chrome()

script = """
var a = [];
$('.stops').each(function(num, item){
	var route = {};
	route.name = $(item).find('h2').html();
	stations = [];
	$(item).find('a').each(function(num, station){
		stations.push($(station).html());
	})
	route.stations = stations;
	a.push(route)
})
return a;
"""

jquery_js = open('jquery.js', 'r')
jquery = jquery_js.read()

data = {
	'bus': {},
	'tr': {}
}

for num in range(51):  # 51
	driver.get(settings.bus_url.format(num + 1))
	driver.execute_script(jquery)

	bus_data = driver.execute_script(script)
	if bus_data:
		data['bus'][str(num + 1)] = bus_data

for num in range(20):  # 20
	driver.get(settings.tr_url.format(num + 1))
	driver.execute_script(jquery)
	data['tr'][str(num + 1)] = driver.execute_script(script)

json_file = open(settings.routes_file, 'w', encoding = "utf-8")
json.dump(data, json_file, ensure_ascii = False)
