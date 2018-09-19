def get_ridership_data(start=2010, end=2017) :

######################################################
# Made to pull ridership data from local directory
# Will return the csv file as a DataFrame
# Requires DataFrame to be saved as a local variable
# The start and end parameters can be changed
# to only pull specific years worth of data
# Only ranges from 2010 through and including 2017
# are valid ranges
######################################################

	import pandas as pd
	from collections import defaultdict

	ridership_dict = defaultdict()
	
	range_var = (end - start) + 1
	
	for year in [start + x for x in range(range_var)] :
		ridership_dict[year] = pd.read_csv("~/Projects/NiceRide/Nice_Ride_data/"+str(year)+"/NiceRide_trip_history_"+str(year)+".csv")
	
	NR_ridership = pd.concat(ridership_dict)
	
	return NR_ridership
