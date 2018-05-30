## NiceRideMN Capstone project

**Client**: NiceRideMN and Similar Bike Share Programs

**Problem**: 
* The NiceRideMN program runs from April through October. If NiceRideMN wanted to extend their season what kind of ridership could be expected in earlier and later months of the year. 
* Riders have membership and non-membership rental opportunities. What riding habits do members have that can be used to market to non-member users to increase membership in NiceRideMN programs
* With a hybrid dock & dockless system can we look at current dock usage demonstrate that areas with less dock density will see growth under hybrid systems?

#### Data and Sources:

**NiceRideMN** [data set](https://github.com/SethDKelly/NiceRideMN/tree/master/Nice_Ride_data) contains 5 years (2010-2017) worth of rider data and station identification in a .csv format.
Included in the rider data is: 
* Start date
* Start station
* Start station number
* End date, End station
* End station number
* Account type
* Total duration (Seconds)

Included in the station data is: 
* Number
* Name
* Latitude
* Longitude
* Total docks

**Weather** [data set](https://github.com/SethDKelly/NiceRideMN/tree/master/Weather_data) will include 5 years worth (2010-2017) of weather data from the Minneapolis-St.Paul international Airport (USW00014922 station ID).
Included in the weather data is: 
* _Precipitation_: precipitation (PRCP), snow depth (SNWD), snowfall (SNOW)
* _Air temperature_: avg. temp (TAVG), max temp. (TMAX), min. temp. (TMIN)
* _Wind_: avg. wind speed (AWND)

**Approach to solve**: 
Exploratory and visualization process of the data sets will look at use patterns for members and non-members: median and mean use time, which stations (non-)members are renting from. Station usage rates: trip times by stations, migration patterns (stations outcoming/incoming rates), proximity to nearest stations from rental station. Weather and daily ridership patterns: max/min temperature, precipitation (rain/snow), accumulation (snow depth), wind speed.

**Deliverables**: Jupyter notebook, Slidedeck of findings, github repository of code use.

**Data Resource Recommendations**: For rentals, did non-members use per ½ hour or 24 hour pass. For members their type of membership (yearly, monthly).

Data used under NiceRideMN [terms](https://www.niceridemn.org/data_license/) and weather [terms](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt)
