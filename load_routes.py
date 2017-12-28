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

#bus_nums = [x + 1 for x in range(51)]
bus_nums = [1, 2, 3]
#tr_nums = [x + 1 for x in range(20)]
tr_nums = []

for num in bus_nums:
	driver.get(settings.bus_url.format(num))
	driver.execute_script(jquery)
	bus_data = driver.execute_script(script)
	if bus_data:
		for bus in bus_data:
			bus['href'] = settings.bus_url.format(num)
		data['bus'][str(num)] = bus_data

for num in tr_nums:
	driver.get(settings.tr_url.format(num))
	driver.execute_script(jquery)
	bus_data = driver.execute_script(script)

	for bus in bus_data:
		bus['href'] = settings.bus_url.format(num)

	data['tr'][str(num)] = bus_data

json_file = open(settings.routes_start_file, 'w', encoding = "utf-8")
json.dump(data, json_file, ensure_ascii = False)
driver.close()
