import csv
from typing import Dict, List
from dataclasses import dataclass, field
from collections import defaultdict

INPUT_FILENAME  = '../01_Data/201510_05_09_trips.csv'
OUTPUT_FILENAME = '../01_Data/201510_tripSummary2.csv'

########### Set up our data store...
@dataclass()
class StationData:
	"""
	StationData holds:
		hourlyBalance    - A list of 24 integers (one per hour of the day) - initialised to zero
		totalHourlyTrips - A list of 24 integers (one per hour of the day) - initialised to zero
    """
	hourlyBalance: List[int] = field(default_factory=lambda: [0 for _ in range(0,24)])
	totalHourlyTrips: List[int] = field(default_factory=lambda: [0 for _ in range(0,24)])

# We use a default dict so we don't need to manually
# create all the stations that we come across
stations: Dict[str, StationData] = defaultdict(StationData)

########### Read and process the input data

print(f'Reading and processing input data from: {INPUT_FILENAME}')
with open(INPUT_FILENAME, 'r') as baseData:
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
		# The original script treated a trip that starts and ends at the same
		# station as single count against the station counter. To match this
		# we update the destination station counter only if it is different
		# to the origin station.
		if originName != destinationName:
			stations[destinationName].totalHourlyTrips[tripHour] += 1

########### Output the results

print(f'Outputing parsed data to: {OUTPUT_FILENAME}')
with open(OUTPUT_FILENAME, 'w') as output:
	csv_writer = csv.writer(output)
	header = ['StationName'] + [f'Balance_{x}' for x in range(0,24)] + [f'Total_{x}' for x in range(0,24)]
	csv_writer.writerow( header )
	
	# Print out the CSV Data; one line per station...
	for station_name, station_data in stations.items():
		row = [station_name] + [str(i) for i in station_data.hourlyBalance] + [str(i) for i in station_data.totalHourlyTrips]
		csv_writer.writerow(row)

