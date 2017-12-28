import json

import settings


def main():
	routes_data, stations_data = read_data()
	buses = import_buses(routes_data)
	stations = import_stations(stations_data, buses)
	routes = []

	buses_file = open(settings.bus_file, 'w', encoding = "utf-8")
	json.dump(buses, buses_file, ensure_ascii = False)
	stations_file = open(settings.station_file, 'w', encoding = "utf-8")
	json.dump(stations, stations_file, ensure_ascii = False)


def import_buses(routes):
	buses = []
	for bus_num in routes['bus']:
		for bus in routes['bus'][bus_num]:
			new_bus = {
				'id': len(buses),
				'city_id': 1,
				'type_id': 1,
				'number': bus_num,
				'name': bus['name'],
				'href': bus['href'],
				'route': bus['stations']
			}
			bus['id'] = new_bus['id']
			buses.append(new_bus)

	for bus_num in routes['tr']:
		for bus in routes['tr'][bus_num]:
			new_bus = {
				'id': len(buses),
				'city_id': 1,
				'type_id': 2,
				'number': bus_num,
				'name': bus['name'],
				'href': bus['href'],
				'route': bus['stations']
			}
			bus['id'] = new_bus['id']
			buses.append(new_bus)

	return buses


def import_stations(stations_data, buses):
	stations = {}
	for st_key in stations_data:
		stations[st_key] = {}
		for st_route in stations_data[st_key]:
			stations[st_key][st_route['direction']] = {}
			bus = get_bus_by_direction_and_href(buses, st_route['direction'], st_route['href'])
			if not bus:
				continue
			stations[st_key][st_route['direction']]['bus_number'] = bus['number']
			stations[st_key][st_route['direction']]['next'] = list(
				set(stations[st_key][st_route['direction']].get('next', [])) | set(get_next_stations(bus, st_key)))
			stations[st_key][st_route['direction']]['prev'] = list(
				set(stations[st_key][st_route['direction']].get('prev', [])) | set(get_prev_stations(bus, st_key)))

	stations_wr = {}

	return stations


def get_bus_by_direction_and_href(buses, direction, href):
	for bus in buses:
		if bus['name'] == direction:
			if not (bus['href'].find(href) == -1):
				return bus
			else:
				print('interesting direction - {0}'.format(direction))


def get_next_stations(bus, station_name):
	return bus['route'][bus['route'].index(station_name) + 1:][:settings.count_stations]


def get_prev_stations(bus, station_name):
	return bus['route'][:bus['route'].index(station_name)][:-settings.count_stations:-1]


def read_data():
	routes_file = open(settings.routes_start_file, 'r', encoding = "utf-8")
	routes = json.loads(routes_file.read())
	stations_file = open(settings.stations_start_file, 'r', encoding = "utf-8")
	stations = json.loads(stations_file.read())
	return routes, stations


main()
