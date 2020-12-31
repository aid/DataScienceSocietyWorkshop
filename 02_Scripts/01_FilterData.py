import csv

print('Reading base data...')
with open('../01_Data/201510-citibike-tripdata.csv', 'r') as baseData:
	reader = csv.reader(baseData, delimiter=',')
	baseList = list(reader)

print(f'There are {len(baseList)} trips...')

print('Creating the output file...')
with open('../01_Data/201510_05_09_trips.csv', 'w') as output:
	output.write(','.join(baseList[0]) + '\n')
	selectedTrips = 0
	for trip in baseList[1:]:
		tripDate = trip[1].split(' ')[0].split('/')[1]
		if 4 < int(tripDate) < 10:
			output.write(','.join(trip) + '\n')
			selectedTrips += 1
		else:
			pass
	print(f'{selectedTrips} trips were selected...')
