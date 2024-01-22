#%% parsing database
"""
TUTORIAL FROM PAPER | MARIO: A Versatile and User-Friendly Software for Building Input-Output Models
(https://doi.org/10.5334/jors.473)

In this example, we show a simple yet comprehensive tutorial on 
the main features of the MARIO modelling framework.
This example requires the user to first download the 
Exiobase hybrid supply-use table referred to year 2011 
from this link: https://zenodo.org/record/7244919#.ZGOGbk_P23A

The downloaded folder can be stored in any directory. 
The path to this folder is indicated henceforth with "exio_path".

To start parsing the downloaded table, it is necessary to have MARIO installed 
(link to the installation guide here: https://mario-suite.readthedocs.io/en/latest/installation.html),
to import it and to call the saved MARIO Database object
called "world" by using the hybrid_sut_exiobase function. 
Also, it is possible to filter over the desired environmental extensions.
Any of the sheets stored in the "MR_HSUTs_2011_v3_3_18_extensions.xlsx" files can be provided, 
as a list. In this case we are going to use only the "Emiss" extensions, 
referring to the emissions transactions.    

"""

import mario

exio_path = "Exiobase Hybrid.zip"  # provide the path of the folder where you stored the downloaded Exiobase hybrid table (replace the path with your path)
world = mario.hybrid_sut_exiobase(path=exio_path, extensions=['Emiss']) # parse the table by providing the type of table and the type of unit

#%% check database properties
"""It is possible to check the sets of the parsed table by just calling it"""
world

#%% get aggregation template
""" 
The first operation we are going to perform is an aggregation of the Database. 
It is possible to export an empty Excel template by calling the "get_aggregation_excel" function 
"""

aggr_template_path = r"Aggregation\aggregation_template.xlsx" # path to the empty Excel template for aggregation
world.get_aggregation_excel(aggr_template_path) # export empty template

#%% check commodity units
"""
In this repository, we provided the already-filled aggregation Excel file whose path is indicated as "aggr_path". 
Note that when aggregating commodities, it is important to be consistent with the units of measure. 
To check the units of measure, it is possible to explore the "commodity_units" DataFrame. 
"""

commodity_units = world.units['Commodity'] # extracting the commodity units
print(commodity_units)

#%% Aggregate
"""
To aggregate the Database, it is just required to read back the filled Excel file by using the "aggregate" function.
It is finally possible to check the new dimension of the Database by printing it. 
The aggregated database has now 5 regions, 50 activities and 44 commodities and just 1 Satellite account which is CO2.
"""

aggr_path = r"Aggregation\aggregation.xlsx" # providing path to filled Excel aggregation file
world.aggregate(aggr_path) # aggregating Database object
print(world) # checking object dimensions

#%% get indices
"""
It is often useful to use get a list of labels of a desired set. 
To do so, it is enough to call the "get_index" function by specifying the set
"""

world.get_index("Activity") # exporting a list of all activities included in the Database 

#%% search
"""
Another useful function to navigate the database is the "search" function. 
Supposing the user desires to get a list of all the activities names containing the "gas" string, 
it is possible to use such function as follows.
"""

world.search("Activity","gas") # extracting all the activities including the "gas" string

#%% calc matrices
"""
It is also possible to calculate and explore matrices just by calling their name. 
For the full terminology, please refer to MARIO documentation (https://mario-suite.readthedocs.io/en/latest/terminology.html).
"""

world.f # calculate the footprint coefficients matrix

#%% get add sectors for activity
"""
Let's suppose now the user wants to model a new industrial activity within the database, 
which is the European supply chain of batteries manufacturing called "Manufacture of batteries", 
which produces the commodity "Batteries". 
Again, it is required to export two empty Excel files, one to add the "Batteries" commodity 
and to add the new "Manufacture of batteries" activity. Let's start with the new activity. 
It is necessary to provide at good description of the input structure of the new activity in the "input_from" sheet, 
as well as the related "Satellite account" transactions and the unit.
"""

new_activities = ['Manufacture of batteries'] # defining the list of new commodities to be added
add_activity_template_path = r"Add_sectors\add_activity_template.xlsx"  # provide the path to the empty template to fill information on the new activities to be added
world.get_add_sectors_excel(
    new_sectors=new_activities,  # specify which are the new sectors (activities) to be added
    regions=world.get_index("Region"), # specify in which regions these activities should be added (in this case, all the Database regions)
    item='Activity', # specify whether they are commodities or activities
    path=add_activity_template_path # specify the path where to save the template
    )

#%% add activities
"""
Once the template to add the activities is filled (the already filled file is provided as "add_activity_path")
it is necessary to call the "add_sectors" function. Afterwards, it is possible to notice that the Database 
now have 51 activities
"""

add_activity_path = r"Add_sectors\add_activity.xlsx"  # indicate the path to the filled template containing info on the new activities to be added
world.add_sectors(
    new_sectors=new_activities,  # specify which are the new sectors (commodities) to be added
    regions=world.get_index("Region"), # specify in which regions these commodities should be added (in this case, all the Database regions)
    item='Activity', # specify whether they are commodities or activities
    io=add_activity_path # specify the path where to save the template
    )
print(world)

#%% get add sectors for commodities
"""
Now the same procedure can be done with the commodity. 
Generate the path to the template and fill in the template: in this case we will 
indicate that these batteries are produced by the new activity ("output from" sheet), 
and that the only consumption of batteries is in the European final demand ("Final consumption" sheet).
The "Batteries" commodity is measured in "kWh" ("units" sheet).
"""

new_commodities = ['Batteries'] # defining the list of new commodities to be added
add_commodity_template_path = r"Add_sectors\add_commodity_template.xlsx"  # provide the path to the empty template to fill information on the new commodities to be added
world.get_add_sectors_excel(
    new_sectors=new_commodities,  # specify which are the new sectors (commodities) to be added
    regions=world.get_index("Region"), # specify in which regions these commodities should be added (in this case, all the Database regions)
    item='Commodity', # specify whether they are commodities or activities
    path=add_commodity_template_path # specify the path where to save the template
    )

#%% add commodities
"""
Once the template to add the commodities is filled 
(the already filled file is provided as "add_commodity_path") 
it is necessary to call the "add_sectors" function once more. 
Afterwards, it is possible to notice that the Database now have 45 commodities
"""

add_commodity_path = r"Add_sectors\add_commodity.xlsx"  # indicate the path to the filled template containing info on the new activities to be added
world.add_sectors(
    new_sectors=new_commodities,  # specify which are the new sectors (commodities) to be added
    regions=world.get_index("Region"), # specify in which regions these commodities should be added (in this case, all the Database regions)
    item='Commodity', # specify whether they are commodities or activities
    io=add_commodity_path # specify the path where to save the template
    )
print(world)

#%% get shock 
"""
Let's complete the analysis by implementing a shock. 
MARIO allows to export an empty Excel template to fill in with 
information regarding the desired modifications to be applied to the original table. 
It is enough to call the "get_shock_excel" function. 
Let's assume that it is of our interest to investigate the environmental impact 
of the increase in final consumption of batteries up to 1 TWh.
"""

shock_template_path = r"Shocks\shock_template.xlsx" # indicating the path to the save the empty shock Excel template
world.get_shock_excel(shock_template_path) # exporting the template

#%% shock calc
"""
Once the shock template is filled (the already filled file is provided as "shock_path") 
it is necessary to call the "shock_calc" function. 
It is necessary to provide which matrices are to be modified and the name of the new scenario 
which will be created ("increased batteries demand" in this case)
"""

shock_path = r"Shocks\shock.xlsx" # indicating the path to the filled shock Excel template
world.shock_calc(
    io = shock_path, # providing the path
    Y = True, # indicating matrix Y (final demand matrix) is modified
    scenario = "increased batteries demand" # naming the new scenario,
)

#%% It is possible to check that the Database object has now two scenarios
print(world)

#%% plot
"""
To conclude, it is possible to visualize, for example, 
the impacted caused by the implemented shock on the consumption of commodities 
required to the production of batteries. 
Such impact can be provided with respect to the baseline scenario. 
To do so, we can use the "plot_matrix" function, which is based on the Plotly library.
"""

world.plot_matrix(
    matrix = 'U', # plotting the use transaction matrix,
    item = 'Commodity',  # it is necessary to specify the row items for the selected matrix
    facet_col='Commodity_from', # arrange the subplots: importing regions on the rows of the grid
    # facet_row='Region_from', # arrange the subplots: exporting regions on the columns of the grid
    x = 'Activity_to', # putting the activities on the x-axis 
    color='Region_from', # putting the commodities on the legend
    path='Plots\plot.html', # providing a path where to save the file
    base_scenario = "baseline", # indicate the results must be shown as a difference with respect to the baseline scenario
    filter_Activity_to= ['Manufacture of batteries'], # filter activities
    filter_Region_from=['China','EU27+UK','RoW'], # filter exporting regions
    filter_Region_to=['EU27+UK'], # filter importing regions
    filter_Commodity_from=['Chemicals','Non-ferrous metal ores','Electricity','Natural gas'], # filter consumed commodities 
)
