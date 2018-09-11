def ride_counter() :
	
	import pandas as pd
	import numpy as np
	
    #######################################################################################
    # Creates a dataframe with the total count of rides from station start and station end
    # Start_id 	End_id 	counts
    #
    # Requires a data frame that has columns for station start_id's and End_id's
    #######################################################################################
    
	for year in [2010 + x for x in range(8)] :
		
		# Load in the data and change to pandas DataFrame
		ridership_dict = pd.read_csv("~/Projects/NiceRide/Nice_Ride_data/"+str(year)+"/NiceRide_trip_history_"+str(year)+".csv")
		NR_ridership = pd.DataFrame(ridership_dict)
		
		assert 'Start_id' in NR_ridership.columns, "Column named `Start_id` must be in arg DataFrame"
		assert 'End_id' in NR_ridership.columns, "Column named `End_id` must be in arg DataFrame"
		
		ride_counts = NR_ridership.drop(['Start_date', 'Start_name', 'End_date', 'End_name', 'duration', 'account'], axis=1)
    
		ride_counts['counts'] = int(0) # create a new column filled with zeroes for a default value
		
		# fill the count column by count aggregrating terminals by start_id and end_id
		ride_counts = ride_counts.groupby(by=['Start_id', 'End_id'],axis=0, as_index=False)['counts'].count()
		
		ride_counts.to_csv("~/Projects/NiceRide/Nice_Ride_data/"+str(year)+"/NiceRide_ride_count_"+str(year)+".csv")
