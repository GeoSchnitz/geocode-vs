import requests
import json
import xml.etree.ElementTree as ET
from numpy import array
from sys import argv

script, city_file = argv

# All functions are pretty much the same; therefore comments (mostly) on the first
def geocode_nominatim():
	#Load settings
	print "Nominatim geocoding ..."
	count_success = 0
	count_fail = 0
	api_data = json.load(open("API.json", "r"))
	return_result = {}
	with open(city_file, "r") as fp:
		for city in fp:
			try:
				api_data["Nominatim"]["payload"]["q"] = city # Set query to current city
				# send request with payload
				r = requests.get(api_data["Nominatim"]["service"]["url"], params=api_data["Nominatim"]["payload"]) 
				placesjson = r.json()
				ping = r.elapsed.microseconds / 1000 # get milliseconds
				result = placesjson[0] # get the first and (supposedly) best result
				return_result.update({city.strip("\n").replace(",",""): {"lat": result['lat'], "lon": result['lon'], "ping_ms": ping}})
				count_success += 1
			except KeyboardInterrupt:
				exit()
			except:
				count_fail += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": "NA", "lon": "NA", "ping_ms": ping}})
	print "%s out of %s cities were geocoded successfully (%d%%)." % (count_success, 
											count_success + count_fail,
											float(count_success) / float(count_success + count_fail) * 100)								
	return return_result

def geocode_google():
	print "Google geocoding ..."
	count_success = 0
	count_fail = 0
	api_data = json.load(open("API.json", "r"))
	return_result = {}
	with open(city_file, "r") as fp:
		for city in fp:
			try:
				api_data["Google"]["payload"]["address"] = city
				r = requests.get(api_data["Google"]["service"]["url"], params=api_data["Google"]["payload"])
				placesjson = r.json()
				ping = r.elapsed.microseconds / 1000
				result = placesjson["results"][0]["geometry"]["location"]
				return_result.update({city.strip("\n").replace(",",""): {"lat": result['lat'], "lon": result['lng'], "ping_ms": ping}})
				count_success += 1
			except KeyboardInterrupt:
				exit()
			except:
				count_fail += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": "NA", "lon": "NA", "ping_ms": ping}})
	print "%s out of %s cities were geocoded successfully (%d%%)." % (count_success, 
											count_success + count_fail,
											float(count_success) / float(count_success + count_fail) * 100)						
	return return_result

def geocode_here():
	print "HERE geocoding ..."
	count_success = 0
	count_fail = 0
	api_data = json.load(open("API.json", "r"))
	return_result = {}
	with open(city_file, "r") as fp:
		for city in fp:
			try:
				api_data["Here"]["payload"]["searchtext"] = city
				r = requests.get(api_data["Here"]["service"]["url"], params=api_data["Here"]["payload"])
				ping = r.elapsed.microseconds / 1000
				root = ET.fromstring(r.content)
				# [1] = first result; long version for readability; 
				# short version: root[0][1][1][3][2][0].text
				lat = root.findtext("./Response/View/Result[1]/Location/DisplayPosition/Latitude") 
				lon = root.findtext("./Response/View/Result[1]/Location/DisplayPosition/Longitude")
				ping = r.elapsed.microseconds / 1000
				if lat == None or lon == None:
					count_fail += 1
					return_result.update({city.strip("\n").replace(",",""): {"lat": "NA", "lon": "NA", "ping_ms": ping}})
				else:
					count_success += 1
					return_result.update({city.strip("\n").replace(",",""): {"lat": lat, "lon": lon, "ping_ms": ping}})
			except KeyboardInterrupt:
				exit()
	print "%s out of %s cities were geocoded successfully (%d%%)." % (count_success, 
											count_success + count_fail,
											float(count_success) / float(count_success + count_fail) * 100)						
	return return_result

def geocode_mapquest():
	print "MapQuest geocoding ..."
	count_success = 0
	count_fail = 0
	api_data = json.load(open("API.json", "r"))
	return_result = {}
	with open(city_file, "r") as fp:
		for city in fp:
			try:
				api_data["MapQuest"]["payload"]["location"] = city
				r = requests.get(api_data["MapQuest"]["service"]["url"], params=api_data["MapQuest"]["payload"])
				placesjson = r.json()
				ping = r.elapsed.microseconds / 1000
				result = placesjson['results'][0]['locations'][0]['latLng']
				count_success += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": result['lat'], "lon": result['lng'], "ping_ms": ping}})
			except KeyboardInterrupt:
				exit()
			except:
				count_fail += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": "NA", "lon": "NA", "ping_ms": ping}})
	print "%s out of %s cities were geocoded successfully (%d%%)." % (count_success, 
											count_success + count_fail,
											float(count_success) / float(count_success + count_fail) * 100)
	return return_result

def geocode_opencage():
	print "OpenCage geocoding ..."
	count_success = 0
	count_fail = 0
	api_data = json.load(open("API.json", "r"))
	return_result = {}
	with open(city_file, "r") as fp:
		for city in fp:
			try:
				api_data["OpenCage"]["payload"]["q"] = city.replace(",","")
				r = requests.get(api_data["OpenCage"]["service"]["url"], params=api_data["OpenCage"]["payload"])
				placesjson = r.json()
				ping = r.elapsed.microseconds / 1000
				result = placesjson['results'][0]['geometry']
				count_success += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": result['lat'], "lon": result['lng'], "ping_ms": ping}})
			except KeyboardInterrupt:
				exit()
			except:
				count_fail += 1
				return_result.update({city.strip("\n").replace(",",""): {"lat": "NA", "lon": "NA", "ping_ms": ping}})
	print "%s out of %s cities were geocoded successfully (%d%%)." % (count_success, 
											count_success + count_fail,
											float(count_success) / float(count_success + count_fail) * 100)
	return return_result

def write_results():	
	with open("cities.csv", "w+") as f:
		# Writing header
		f.write("City, " 
				+ "Nominatim_Lat, Nominatim_Lon, Nominatim_ping_ms, " 
				+ "Google_Lat, Google_Lon, Google_ping_ms, " 
				+ "MapQuest_Lat, MapQuest_Lon, MapQuest_ping_ms, "
				+ "Here_Lat, Here_Lon, Here_ping_ms, "
				+ "OpenCage_Lat, OpenCage_Lon, OpenCage_ping_ms"
				+ "\n")
	# Write results
	for a, b in nom.iteritems():
		with open("cities.csv", "a+") as f:
			f.write(a + ", " + str(b["lat"]) + ", " 
							+ str(b["lon"]) + ", " 
							+ str(b["ping_ms"]) + ", "
							+ str(ggl[a]["lat"]) + ", "
							+ str(ggl[a]["lon"]) + ", " 
							+ str(ggl[a]["ping_ms"]) + ", "
							+ str(mq[a]["lat"]) + ", "
							+ str(mq[a]["lon"]) + ", " 
							+ str(mq[a]["ping_ms"]) + ", "
							+ str(here[a]["lat"]) + ", "
							+ str(here[a]["lon"]) + ", " 
							+ str(here[a]["ping_ms"]) + ", "
							+ str(oc[a]["lat"]) + ", "
							+ str(oc[a]["lon"]) + ", " 
							+ str(oc[a]["ping_ms"])
							+ "\n")	
	print "CSV output written to: cities.csv"

def calc_stats():
	nom_outlier = 0
	ggl_outlier = 0
	mq_outlier = 0
	here_outlier = 0
	oc_outlier = 0
	
	outlier = []

	nom_ping = 0
	ggl_ping = 0
	mq_ping = 0
	here_ping = 0
	oc_ping = 0

	nom_fail = 0
	nom_success = 0
	ggl_fail = 0
	ggl_success = 0
	mq_fail = 0
	mq_success = 0
	here_fail = 0
	here_success = 0
	oc_fail = 0
	oc_success = 0

	iter_count = 1
	fail_count = 0

	for a, b in nom.iteritems():
		# Get response time for queries
		nom_ping += b["ping_ms"]
		ggl_ping += ggl[a]["ping_ms"]
		mq_ping += mq[a]["ping_ms"]
		here_ping += here[a]["ping_ms"]
		oc_ping += oc[a]["ping_ms"]
		iter_count += 1
		
		# Get success rate of geocoding per provider (w/o passing the value from the 
		# function above...
		if b["lat"] == "NA":
			nom_fail += 1
		else: 
			nom_success += 1
			
		if ggl[a]["lat"] == "NA":
			ggl_fail += 1
		else: 
			ggl_success += 1
			
		if mq[a]["lat"] == "NA":
			mq_fail += 1
		else: 
			mq_success += 1
			
		if here[a]["lat"] == "NA":
			here_fail += 1
		else: 
			here_success += 1
			
		if oc[a]["lat"] == "NA":
			oc_fail += 1
		else: 
			oc_success += 1
		# Try to calculate outliers
		try:
			coords_x = array((float(b["lat"]), float(ggl[a]["lat"]), float(mq[a]["lat"]),
								float(here[a]["lat"]), float(oc[a]["lat"])))
			coords_y = array((float(b["lon"]), float(ggl[a]["lon"]), float(mq[a]["lon"]), 
								float(here[a]["lon"]), float(oc[a]["lon"])))			
				
			# Calculate outliers, which is done by comparing a coordinate with the standard 
			# deviation of the 5 providers. If the difference is higher than the std then 
			# the point should be counted as outlier. Although this doesn't neccessarily mean
			# anything it may create hints to investige further. It could be a sign for a very
			# high or very poor quality of geocoding or some other issues (e.g. using the
			# first result of the response set). 
			if (abs(coords_x.mean() - float(b["lat"])) > coords_x.std() 
				and abs(coords_y.mean() - float(b["lat"])) > coords_y.std()):
				nom_outlier += 1
				outlier.append(str(a) + " (Nominatim)")
			elif (abs(coords_x.mean() - float(ggl[a]["lat"])) > coords_x.std() 
				and abs(coords_y.mean() - float(ggl[a]["lat"])) > coords_y.std()):
				ggl_outlier += 1
				outlier.append(str(a) + " (Google)")
			elif (abs(coords_x.mean() - float(mq[a]["lat"])) > coords_x.std() 
				and abs(coords_y.mean() - float(mq[a]["lat"])) > coords_y.std()):
				mq_outlier += 1
				outlier.append(str(a) + " (MapQuest)")
			elif (abs(coords_x.mean() - float(here[a]["lat"])) > coords_x.std() 
				and abs(coords_y.mean() - float(here[a]["lat"])) > coords_y.std()):
				here_outlier += 1
				outlier.append(str(a) + " (HERE)")
			elif (abs(coords_x.mean() - float(oc[a]["lat"])) > coords_x.std() 
				and abs(coords_y.mean() - float(oc[a]["lat"])) > coords_y.std()):
				oc_outlier += 1				
				outlier.append(str(a) + " (OpenCage)")
		except ValueError:
			# Coordinates of one or more providers are missing ("NA"), therefore do not 
			# calculate. This should make sure that at least some statistical common sense
			# is obeyed. But definitely open for discussion, whether it is a good idea.
			fail_count += 1
	print """
-----------------------------------------------------------------------
|           | success rate / no. of outliers / ping (ms) 
|-----------|----------------------------------------------------------
| Nominatim | %s%% / %s / %s
| Google    | %s%% / %s / %s
| MapQuest  | %s%% / %s / %s
| HERE      | %s%% / %s / %s
| OpenCage  | %s%% / %s / %s
|----------------------------------------------------------------------
| Processed %s datapoints, %s were used for outlier calculation (%s%%).
-----------------------------------------------------------------------
	""" % (format(float(nom_success) / float(nom_fail + nom_success) * 100, '.2f'), nom_outlier, 
				nom_ping / iter_count, 
			format(float(ggl_success) / float(ggl_fail + ggl_success) * 100, '.2f'), 
				ggl_outlier, ggl_ping / iter_count, 
			format(float(mq_success) / float(mq_fail + mq_success) * 100, '.2f'), 
				mq_outlier, mq_ping / iter_count, 
			format(float(here_success) / float(here_fail + here_success) * 100, '.2f'), 
				here_outlier, here_ping / iter_count, 
			format(float(oc_success) / float(oc_fail + oc_success) * 100, '.2f'),
				oc_outlier, oc_ping / iter_count, 
			iter_count, iter_count - fail_count, float(iter_count - fail_count) / float(iter_count) * 100)
	# Write outliers to file for further investigation
	with open("outliers.txt", "w+") as o:
		for item in outlier:
			o.write(item + "\n")
	print "Outliers written to: outliers.txt"
	
if __name__ == "__main__":
	nom = geocode_nominatim()
	ggl = geocode_google()
	mq = geocode_mapquest()
	here = geocode_here()
	oc = geocode_opencage()
	calc_stats()
	write_results()
