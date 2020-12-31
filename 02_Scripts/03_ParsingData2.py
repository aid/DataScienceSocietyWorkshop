import csv
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict

########### Set up our data store...
@dataclass()
class StationData:
	hourlyBalance: List[int]
	totalHourlyTrips: List[int]

	def __init__(self):
		self.hourlyBalance = [0 for _ in range(0,24)]
		self.totalHourlyTrips= [0 for _ in range(0,24)]

# We use a default dict so we don't need to manually
# create all the stations that we come across
stations: Dict[str,StationData] = defaultdict(StationData)

########### Read and process the input data

print('Reading and processing trip data...')
with open('../01_Data/201510_05_09_trips.csv', 'r') as baseData:
	csv_reader = csv.reader(baseData, delimiter=',')
	header = next(csv_reader)
	for trip in csv_reader:
		# Extract the data we care about from the CSV row
		tripTime = trip[1]
		originName = trip[4]
		destinationName = trip[8]

		# Find the hour of this trip from the time...
		tripHour = int(tripTime.split(' ')[1].split(':')[0])

		# Update the origin and destination station data according to this trip...
		stations[originName].hourlyBalance[tripHour] -= 1
		stations[destinationName].hourlyBalance[tripHour] += 1
		stations[originName].totalHourlyTrips[tripHour] += 1
		stations[destinationName].totalHourlyTrips[tripHour] += 1

########### Output the results

print('Creating the output file...')
with open('../01_Data/201510_tripSummary2.csv', 'w') as output:
	csv_writer = csv.writer(output)
	header = ['StationName'] + [f'Balance_{x}' for x in range(0,24)] + [f'Total_{x}' for x in range(0,24)]
	csv_writer.writerow( header )
	
	# Print out the CSV Data; one line per station...
	for station_name, station_data in stations.items():
		row = [station_name] + station_data.hourlyBalance + station_data.totalHourlyTrips
		csv_writer.writerow(row)

