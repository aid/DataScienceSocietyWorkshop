import csv

print('Reading base data...')
with open('../01_Data/201510_05_09_trips.csv', 'r') as baseData:
	reader = csv.reader(baseData, delimiter=',')
	baseList = list(reader)
print(f'There are {len(baseList)} trips...')

print('Creating a list of the stations...')
stationList = []
for trip in baseList[1:]:
	originName = trip[4]
	destinationName = trip[8]
	if originName not in stationList:
		stationList.append(originName)
	if destinationName not in stationList:
		stationList.append(destinationName)
print(f'There are {len(stationList)} stations...')

print('Creating the output file...')
with open('../01_Data/201510_tripSummary.csv', 'w') as output:
	balanceLabels = []
	totalLabels = []
	for x in range(24):
		balanceLabels.append((f'Balance_{x}'))
		totalLabels.append((f'Total_{x}'))
	output.write('StationName' + ',' + ','.join(balanceLabels) + ',' + ','.join(totalLabels) + '\n')
	stationCount = 0
	for station in stationList:
		hourlyBalance = []
		totalHourlyTrips = []
		for hour in range(24):
			balance = 0
			totalTrips = 0
			for trip in baseList[1:]:
				tripHour = int(trip[1].split(' ')[1].split(':')[0])
				if tripHour == hour:
					if station == trip[4]:
						balance -= 1
					if station == trip[8]:
						balance += 1
					if station == trip[4] or station == trip[8]:
						totalTrips += 1
				else:
					continue
			hourlyBalance.append(str(balance))
			totalHourlyTrips.append(str(totalTrips))
		output.write(station + ',' + ','.join(hourlyBalance) + ',' + ','.join(totalHourlyTrips) + '\n')
		stationCount += 1
		print(f'Done with station {station} {stationCount}/{len(stationList)}')

