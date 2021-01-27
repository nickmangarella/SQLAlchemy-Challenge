# SQLAlchemy-Challenge

## Description
Climate, Temperature, and Rainfall analysis on Honolulu, Hawaii using SQLAlchemy and Flask modules.


## Climate Analysis
### Reflect Tables into SQLAlchemy ORM
* Python SQL toolkit and Object Relational Mapper modules
* Engine Creation and Reflection of existing database
* References to each table and Session creation
### Exploratory Precipitation Analysis
* Query to find the most recent date
* Calculation of the date one year from the most recent date using Python Datetime module
* Query to find the precipitation scores using the calulated date of one year ago
* The query results saved as a DataFrame and a Pandas bar chart of these results
* Summary statistics of the precipitation data
### Exploratory Station Analysis
* Query to calculate the total number of stations in the dataset
* Query to show the most active stations
* Query to select the minimum, maximum, and average temperture observations of most active station
* Query of the last year of temperature observations of most acitve station and a Matplotlib histogram of the results
### Close Session
* Close of Session


## Temp Analysis 1
### Temperature Analysis I
* Python Datetime and SciPy Stats modules
* Read in of the temperature measurements CSV and DataFrame setup
    #### Compare June and December data across all years
    * Filters of the data for June and December
    * Calculations of average temperature for June and December from entire dataset
    * Unpaired t-test of June and December temperatures
    #### Analysis
    Since both June and December datasets are independent of one another, we should use a an un-paired t-test. The pvalue from these datasets is far less than 0.05 so we can conclude that a significant statistical difference exists between the means and reject the null hypothesis.

## Temp Analysis 2
### Reflect Tables into SQLAlchemy ORM
* Python SQL Toolkit and Object Relational Mapper modules
* Engine Creation and Reflection of existing database
* References to each table and Session creation
### Temperature Analysis II
* Function named 'calc_temps' that accepts start and end dates to return the temperature mininum, average, and maximum for the range of dates
* 'calc_temps' function to return temperature minimums, averages, and maximums for a week in August 2017
* Matplotlib bar chart of the results from 'calc_temps' function for the week in August 2017
    #### Daily Rainfall Average
    * Query to select station location data and total amount of rainfall for the same week in August 2017
    * Function named 'daily_normals' that accepts a month and day date and returns the temperature minimum, average, and maximum
    * For loop with 'daily_normals' function to return the temperature miminums, averages, and maximums for the same August week
    * Results saved as a DataFrame and a Pandas area plot of the results
### Close Session
* Close of Session

## App.py
* Python SQL toolkit, Object Relational Mapper, Flask, and Python Datetime modules
* Engine creation, references to the tables, and Flask setup
* Route to Homepage and 'welcome' function that reutrns the list of available API routes
* Route to Precipitation page and 'precipitation' function that returns Date-Precipiation dictionary in JSON format
* Route to Stations page and 'stations' function that returns a list in JSON format of all the stations
* Route to Temperature Observations (tobs) page and 'tobs' function that returns a list in JSON format of the latest year's tobs for the most active station
* Route to Start Date page and 'start' function that returns a list in JSON format of temperature minimums, averages, and maximums from a any chosen start date to the latest date in the dataset
* Route to Start and End Date page and 'start_end' function that returns a list in JSON format of temperature minimums, averages, and maximums from a any chosen start and end dates in the dataset

