def kmeans_builder() :
    
    # For KMeans model building
    from sklearn.cluster import KMeans

    # For Feature Optimizations
    from sklearn.decomposition import PCA

    #########################################################################
    # This sections builds the clusters for each (2010-2017) years data
    # The code uses KMeans clustering with a K value of 6
    # Appends to the DF `NR_station` the cluster each station belongs to
    # into a new column `Cluster`
    ########################################################################

    NR_station['Cluster'] = int(0)

    for year in [2010 + x for x in range(8)] :
    
        distance_matrix = pd.DataFrame() # Reinstantiate the  Distance Matrix DataFrame for clean run
    
        # Read in the distance matrix for the particular year
        distance_matrix = pd.read_csv("https://raw.githubusercontent.com/SethDKelly/NiceRideMN/master/Nice_Ride_data/" \
									+str(year)+"/distance_matrix_"+str(year)+".csv",index_col=0)
    
        # Optimize distance matrix to two primary x-y components
        pca = PCA(n_components=2).fit_transform(distance_matrix)
    
        #Append to the DF `NR_station` the cluster each station belongs to in column `Cluster`
        NR_station.loc[year, 'Cluster'] =  KMeans(n_clusters=6, n_init=200).fit(pca).labels_
        
    return NR_station
    
def ride_counter(NR_ride_df, year=2017) :

    #######################################################################################
    # Creates a dataframe with the total count of rides from station start and station end
    # Start_id 	End_id 	counts
    #
    # Requires a data frame that has columns for station start_id's and End_id's
    #######################################################################################

    assert 'Start_id' in NR_ride_df.columns, "Column named `Start_id` must be in arg DataFrame"
    assert 'End_id' in NR_ride_df.columns, "Column named `End_id` must be in arg DataFrame"
    
    ride_counts = NR_ride_df.loc[year,:].drop(['Start_date', 'Start_name', 
                                                 'End_date', 'End_name', 
                                                 'duration', 'account'], axis=1)
    
    ride_counts['counts'] = 0 # create a new column filled with zeroes for a default value
    
    # fill the count column by count aggregrating terminals by start_id and end_id
    ride_counts = ride_counts.groupby(by=['Start_id', 'End_id'],axis=0, as_index=False)['counts'].count()
    
    return ride_counts
    
def graph_builder(ride_df) :
    
    import networkx as nx

    ################################################################
    # Takes single arguements, ride_df
    # ride_df must have columns: 'Start_id', 'End_id', 'counts'
    # builds a networkX graph of type Graph()
    # returns the graph
    ################################################################

    assert 'counts' in ride_df.columns, "Column named `counts` must be in arg ride_df "
    assert 'End_id' in ride_df.columns, "Column named `End_id` must be in arg ride_df"
    assert 'Start_id' in ride_df.columns, "Column named `Start_id` must be in arg ride_df"


    graph = nx.from_pandas_edgelist(ride_df,\
                                    source = 'Start_id', \
                                    target = 'End_id', \
                                    edge_attr = 'counts', \
                                    create_using = nx.Graph())
    return graph

def get_edge_coor(graph, _station) :

    ################################################################
    # Takes two arguements, graph and _station
    # graph must be of type nx.Graph()
    # _station must have columns: 'Termina', 'Latitude', 'Longitude'
    #
    # function takes the edges in graph
    # finds the nodes locations:
    # node1(x, y) / node1(long/lat), node2(x, y) / node2(long/lat)
    # creates 3 different arrays: xs, ys, alpha
    # xs are the x values for node1/2, ys are the y values for node1/2
    # alpha is the `weight` of the node, to be used as edge alpha value
    # returns xs, ys, alpha
    ################################################################

    assert (type(graph) == nx.Graph),"arg graph must be of type Graph not of type DiGraph, MultiGraph, or MultiDiGraph"
    assert 'Terminal' in _station.columns, "Column named Terminal must be in arg DataFrame"
    assert 'Longitude' in _station.columns, "Column named Longitude must be in arg DataFrame"
    assert 'Latitude' in _station.columns, "Column named Latitude must be in arg DataFrame"

    xs = []
    ys = []
    alpha = []
    edge = dict(xs=[], ys=[], alpha=[])
    # example: { ..., ('30001.0', '300005.0', {'counts': 243}), ... }
    # u is origin_node, v is terminus_node, d is data ('counts')
    
    for u, v, d in graph.edges.data('counts', default = 0):
        
        edge['xs'].append([_station[_station.Terminal == u].Longitude.values[0], \
                  _station[_station.Terminal == v].Longitude.values[0]])

        edge['ys'].append([_station[_station.Terminal == u].Latitude.values[0], \
                  _station[_station.Terminal == v].Latitude.values[0]])
        edge['alpha'].append(d) # rescale for later alpha normalization
        
    # create values of alpha that are between 0 and 1
    edge['alpha'] = [a / max(edge['alpha']) for a in edge['alpha']]
    
    return edge
    
def main() :

    # Perform necessary imports for Bokeh plotting
    from bokeh.io import output_file, show, curdoc
    from bokeh.plotting import figure

    # Import the models modules
    from bokeh.models import ColumnDataSource, HoverTool, Slider, ColorMapper
    from bokeh.models.widgets import CheckboxGroup

    # Import the layout modules
    from bokeh.layouts import widgetbox, column, row

    # To build graph as an application
    from bokeh.io import curdoc

    # For cluster coloring
    from bokeh.palettes import Spectral6

    # Base dependancies
    import pandas as pd
    import numpy as np
    from collections import defaultdict

    ################################################
    # Load in Data:
    #
    # Make an empty DefaultDict
    # fill dictionary {year: dataframe}
    # build hierarchal dataframe using dictionary
    ################################################

    # Example of data location, uses year 2010
    # https://raw.githubusercontent.com/SethDKelly/NiceRideMN/master/Nice_Ride_data/2010/NiceRide_station_2010.csv

    station_dict = defaultdict()
    ridership_dict = defaultdict()
    
    for year in [2010 + x for x in range(8)] :
        station_dict[year] = pd.read_csv("https://raw.githubusercontent.com/SethDKelly/NiceRideMN/master/Nice_Ride_data/" \
                                 +str(year)+"/NiceRide_station_"+str(year)+".csv")
		ridership_dict[year] = pd.read_csv("https://raw.githubusercontent.com/SethDKelly/NiceRideMN/master/Nice_Ride_data/" \
                                 +str(year)+"/NiceRide_trip_history_"+str(year)+".csv")
    NR_station = pd.concat(station_dict)
    NR_ridership = pd.concat(ridership_dict)    


    #########################################
    # Section to instantiate graph properties
    #########################################

    # File Name
    output_file('TEST')

    # Creating hovertool tip
    hover = HoverTool(tooltips=[('Terminal', '@terminal'), 
                           ('Name', '@station'),
                           ('Location', '($x, $y)')])
    
    # Setting boundaries for x-y axis ranges
    xmin, xmax = (NR_station.loc[:,:].Longitude.values.min() - .01) , (NR_station.loc[:,:].Longitude.values.max() + .01)
    ymin, ymax = (NR_station.loc[:,:].Latitude.values.min() - .01) , (NR_station.loc[:,:].Latitude.values.max() + .01)
    
    # Create the figure: plot
    plot = figure(plot_height=750, plot_width=1000,
              x_range = (xmin, xmax), y_range = (ymin, ymax),
              tools=[hover, 'box_zoom', 'reset', 'wheel_zoom', 'pan', 'lasso_select'])

    # Set the x/y-axis label
    plot.xaxis.axis_label = 'Longitude'
    plot.yaxis.axis_label = 'Latitude'

    ###############################
    # Add Node Data
    ###############################
    
    # Make the ColumnDataSource: source
    node_source = ColumnDataSource(data={
        'x'        : NR_station.loc[2017,:].Longitude,
        'y'        : NR_station.loc[2017,:].Latitude,
        'terminal' : NR_station.loc[2017,:].Terminal,
        'station'  : NR_station.loc[2017,:].Station,
        'cluster'  : NR_station.loc[2017,:].Cluster
        })



    # Add the nodes to the circle glyph
    r_circles = plot.circle(x='x', y='y', source=node_source,
                fill_alpha=0.8, legend='cluster', size = 10) # Add color mapper by cluster, add node size by

    # Set the legend.location attribute of the plot to 'top_right'
    plot.legend.location = 'top_right'

    ###############################
    # Section to load ridership data
    # build NetworkX graph model
    # and add NetworkX edges to graph
    ###############################
    
    NR_ridership = kmeans_builder(NR_ridership)
    ride_counts = ride_counter(NR_ridership)
    graph = graph_builder(ride_counts)
    
    edge_source = ColumnDataSource(data = get_edge_coor(graph, NR_station.loc[2017,:]))
    r_lines = plot.multi_line(xs = 'xs',ys = 'ys', source=edge_source,
                          line_width=1.5, alpha=.06, color='navy')

    ########################################
    # Graph Node and Edge interaction policy TEMPLATE
    ########################################

    '''
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    '''

    ######################################################
    # Section is to set up year slider widget
    # Allow Users to update graph by year using the slider
    ######################################################

    # Define the callback function: update_plot
    def update_plot(attr, old, new):

        # set the `yr` name to `slider.value` and `source.data = new_data`
        yr = slider.value
    
        new_node_data = {
            'x'        : NR_station.loc[yr, :].Longitude,
            'y'        : NR_station.loc[yr, :].Latitude,
            'terminal' : NR_station.loc[yr, :].Terminal,
            'station'  : NR_station.loc[yr, :].Station,
            'cluster'  : NR_station.loc[yr, :].Cluster,
        }
    
        new_edge_data = ColumnDataSource(data = get_edge_coor(graph, NR_station.loc[yr,:]))
    
        # Assign updated data to: *_source.data
        node_source.data = new_node_data
        edge_source.data = new_edge_data
    
        # Add title to figure: plot.title.text
        plot.title.text = 'NiceRideMN data for %d' % yr


    # Make a slider object: slider
    slider = Slider(start=2010, end=2017, step=1, value=2017, title='Year')

    # Attach the callback to the 'value' property of slider
    slider.on_change('value', update_plot)
    
    ######################################################
    # Section is to set up cluster checkboxes
    # Allow Users to choose which clusters to show
    ######################################################
    '''
    checkbox_group = CheckboxGroup(
            labels=["Cluster 1", "Cluster 2", "Cluster 3"
                    "Cluster 4", "Cluster 5", "Cluster 6"], active=[0,1,2,3,4,5])
    Need to figure out how to change active cluster based on                 
                
    '''
    ######################################################
    # Section is to setup how the plot and widgets are displayed
    ######################################################
    
    # Make a row layout of widgetbox(slider) and plot and add it to the current document
    layout = column(plot, widgetbox(slider))
    curdoc().add_root(layout)


    # Add the plot to the current document and add a title
    curdoc().add_root(plot)
    curdoc().title = 'Nice Ride stations'
