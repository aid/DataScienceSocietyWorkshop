## Data Visualization with Processing
Workshop for the Columbia Data Science Society by Juan Francisco Saldarriaga (jfs2118@columbia.edu)

### 1. Download Processing and Base Data
* [Processing.org](https://processing.org/)
* There are great tutorials for Processing [here](https://processing.org/tutorials/) and [here](https://www.youtube.com/user/shiffman/playlists?sort=dd&shelf_id=2&view=50).
* [Citibike trip data](https://www.citibikenyc.com/system-data): trip data by month.
* [Citibike station data](https://feeds.citibikenyc.com/stations/stations.json): station data, updated every two minutes (json format).

### 2. Filtering the data
We will only be using data for weekday trips in one week in October 2015. So the first thing we need to do is create a subset of the data with just these trips: 10/05/15 - 10/09/15.
```python
import csv

print 'Reading base data...'
with open('../01_Data/201510-citibike-tripdata.csv', 'rb') as baseData:
    reader = csv.reader(baseData, delimiter=',')
    baseList = list(reader)

print 'There are ' + str(len(baseList)) + ' trips...'

print 'Creating the output file...'
output = open('../01_Data/201510_05_09_trips.csv', 'wb')
output.write(','.join(baseList[0]) + '\n')
selectedTrips = 0
for trip in baseList[1:]:
    tripDate = trip[1].split(' ')[0].split('/')[1]
    if 4 < int(tripDate) < 10:
        output.write(','.join(trip) + '\n')
        selectedTrips += 1
    else:
        pass
print str(selectedTrips) + ' trips were seelcted...'
output.close()
```

### 3. Summarizing the data
Once we've filtered the data we need to summarize into the right format, showing for every station, how many trips per hour happened and what was the balance for every hour. There is probably a much better way of creating this dataset with Pandas but here's my basic Python script:
```python
import csv

print 'Reading base data...'
with open('../01_Data/201510_05_09_trips.csv', 'rb') as baseData:
    reader = csv.reader(baseData, delimiter=',')
    baseList = list(reader)
print 'There are ' + str(len(baseList)) + ' trips...'

print 'Creating a list of the stations...'
stationList = []
for trip in baseList[1:]:
    originName = trip[4]
    destinationName = trip[8]
    if originName not in stationList:
        stationList.append(originName)
    if destinationName not in stationList:
        stationList.append(destinationName)
print 'There are ' + str(len(stationList)) + ' stations...'

print 'Creating the output file...'
output = open('../01_Data/201510_tripSummary.csv', 'wb')
balanceLabels = []
totalLabels = []
for x in range(24):
    balanceLabels.append(('Balance_'+str(x)))
    totalLabels.append(('Total_'+str(x)))
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
    print 'Done with station ' + station + ' ' + str(stationCount) + '/' + str(len(stationList))

output.close()
```

### 4. Intro to Processing
```Processing
void setup(){
  size(500,500);
  background(0);
}

void draw(){
  background(0);
  ellipse(mouseX, mouseY, 20, 20);
}
```

### 5. Creating a grid
```Processing
int circleWidth = 20;
int numberOfColumns = 22;
int numberOfRows = 22;
int topMargin = 15;
int rightMargin = 15;
int circleSpacing = 2;
float hueColor = 0;
float saturationColor = 0;

void setup(){
  size(500,500);
  background(0);
  colorMode(HSB, 360, 100, 100);
  pixelDensity(2);
  noLoop();
  noStroke();
  for (int i=0; i < numberOfRows; i++){
    for (int j=0; j < numberOfColumns; j++){
      hueColor = map(i, 0, numberOfRows, 0, 360);
      saturationColor = map(j, 0, numberOfColumns, 50, 100);
      fill(hueColor, saturationColor, 100);
      ellipse(i*(circleWidth+circleSpacing) + rightMargin, j*(circleWidth+circleSpacing) + topMargin, circleWidth, circleWidth);
    }
  }
}
```

### 6. Loading the data into Processing
```Processing
// Global Objects
Table stationTable;

void setup(){
  loadData();
}

void loadData(){
  stationTable = loadTable("201510_tripSummary.csv", "header");
  println(stationTable.getRowCount());
  String stationName;
  int totalImbalance;
  for (int i=0; i<stationTable.getRowCount(); i++){
    totalImbalance = 0;
    stationName = stationTable.getString(i, "StationName");
    for (int j=0; j<24; j++){
      totalImbalance = totalImbalance + stationTable.getInt(i, (1+j));
    }
    println(stationName + " - Total Imbalance = " + str(totalImbalance));
  }
}
```
### 7. Creating a 'Heatmap' of station imbalance
Final code:
```Processing
// Import libraries
import processing.pdf.*;

// Global Objects
Table stationTable;
PFont font;

void setup(){
  size(670,1415);
  noLoop();
  loadData();
  createGraph();
}

void createGraph(){
  beginRecord(PDF, "ImbalanceMatrix.pdf");
  colorMode(HSB, 360, 100, 100);
  font = createFont("NeutraTextLight.otf", 2, true);
  textFont(font);
  background(0, 0, 20);
  String stationName;
  textAlign(RIGHT);
  noStroke();
  for (int i=0; i<stationTable.getRowCount(); i++){
    stationName = stationTable.getString(i, "StationName");
    fill(0, 0, 100);
    text(stationName, 45, 25+i*3);
    for (int j=0; j<24; j++){
      float hourValue = stationTable.getInt(i, (j+1));
      float alphaValue;
      if (hourValue >= 0){
        alphaValue = map(hourValue, 0, 50, 5, 100);
        fill(180, 100, 100, alphaValue);
      }
      else{
        alphaValue = map(hourValue, 0, -50, 5, 100);
        fill(24, 100, 100, alphaValue);
      }
      rect(50 + j*25, 23.5 + i*3, 24.5, 2.5);
    }
  }
  endRecord();
}

void loadData(){
  stationTable = loadTable("201510_tripSummary.csv", "header");
  println("Data loaded... " + str(stationTable.getRowCount()) + " stations read...");
}
```

### 8. Creating station 'Dials'
```Processing
import processing.pdf.*;

Table hourTable;
Table balanceTable;
int middleCircle = 20;
float divisionFactor = .6668;
int numberOfDials = 15;
int sidePadding = 90;
int spaceBetweenDials = 105;
int verticalSpaceBetween = 100;
float increments = 3;
int position = 0;
float factor = 500;
int totalRadius = 40;

PFont smallFont;
PFont font;

void setup() {
  size(1675, 2384);
  noLoop();
  smooth();
  font = createFont("NeutraTextLight.otf", 6, true);
  smallFont = createFont("NeutraTextLight.otf", 3, true);
  createGraph();
  println("All done...");
}

void createGraph() {
  beginRecord(PDF, "Test_03.pdf");
  colorMode(HSB, 360, 100, 100);
  textAlign(CENTER, CENTER);
  background(0, 0, 20);

  //Read the files
  hourTable = loadTable("Activity_Matrix.csv", "header");
  println("Done loading the activity table, there are " + hourTable.getRowCount() + " rows in the table...");
  balanceTable = loadTable("Oct_Balance_Hour.csv", "header");
  println("Done loading the balance table...");

  //Get data out of the table
  for (int i=0; i<hourTable.getRowCount (); i++) {
    String stationName = hourTable.getString(i, 0);
    float maxTrips = 0;
    float totalTrips = 0;
    float trips = 0;
    float percentage = 0;
    int balance = 0;
    int colorValue;
    for (int j=0; j<25; j++) {
      trips = hourTable.getInt(i, j);
      maxTrips = max(trips, maxTrips);
      totalTrips = totalTrips + trips;
    }

    //Build the framework for the dials
    position = i;
    fill(0, 0, 20);
    noStroke();
    ellipse(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), 72, 72);
    for (int j = 0; j<4; j++) {
      noFill();
      strokeWeight(.25);
      stroke(0, 0, 60);
      //ellipse(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), middleCircle+(increments*4*j)+increments*2, middleCircle+(increments*4*j)+increments*2);
    }
    for (int j = 0; j<5; j++) {
      noFill();
      strokeWeight(.25);
      stroke(0, 0, 30);
      ellipse(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), middleCircle+(increments*4*j), middleCircle+(increments*4*j));
    }
    for (int j = 1; j<5; j++) {
      fill(0, 0, 20);
      noStroke();
      rectMode(CENTER);
      rect((sidePadding+30+(position%numberOfDials)*spaceBetweenDials)+0.25, (verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween)-middleCircle/2-(increments*2*j))+1, 5, 3);
      fill(0, 0, 40);
      textFont(smallFont);
      text(round(j*increments*2*factor/1000)+"%", sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween)-middleCircle/2-(increments*2*j)-1);
    }

    //Build the bars in the dials
    //    for (int j=1; j<25; j++) {
    //      trips = hourTable.getInt(i, j);
    //      strokeWeight(0.5);
    //      strokeCap(SQUARE);
    //      stroke(255, 100, 255);
    //      pushMatrix();
    //      translate(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween));
    //      rotate(radians(360.0/24*j));
    //      line(0, 0, 0, -middleCircle/2+(trips/27/divisionFactor)*(-1));
    //      popMatrix();
    //    }

    //Build the main markers
    for (int j=1; j<25; j++) {
      trips = hourTable.getInt(i, j);
      percentage = trips/totalTrips;
      balance = balanceTable.getInt(i, j+2);
      noStroke();
      colorValue = 0;
      //fill(0, 0, 30);
      //arc(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), middleCircle/2+percentage*factor, middleCircle/2+percentage*factor, radians(-90+((j-1)*360/24)), radians(-90+(j*360/24)));
      if (balance >= 0) {
        fill(180, 100, 100, map(balance, 0, 100, 45, 100));
      } else {
        fill(24, 100, 100, map(balance, 0, -100, 45, 100));
      }
      arc(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), middleCircle/2+percentage*factor, middleCircle/2+percentage*factor, radians(-90+((j-1)*360/24)), radians(-90+(j*360/24)));
    }

    //Add the inner circle
    fill(0, 0, 20);
    noStroke();
    ellipse(sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween), middleCircle, middleCircle);
    fill(0, 0, 60);
    noStroke();
    textFont(font);
    text(stationName, sidePadding+30+(position%numberOfDials)*spaceBetweenDials, verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween)-47);
    fill(0, 0, 40);
    textFont(smallFont);    
    for (int j=1; j<9; j++) {
      int hour = j*3;
      String am = "AM";
      if (hour > 11 && hour<24) {
        am = "PM";
      } else {
        am = "AM";
      }
      if (hour > 12) {
        hour = hour - 12;
      }
      text(hour + am, sidePadding+30+(position%numberOfDials)*spaceBetweenDials+totalRadius*cos(radians(-90+(360/8*j))), verticalSpaceBetween/2+(floor(position/numberOfDials)*verticalSpaceBetween+totalRadius*sin(radians(-90+(360/8*j)))));
    }
  }

  endRecord();
}
```