# hawaii-weather-analysis

## Description
Climate, Temperature, and Rainfall analysis of Honolulu, Hawaii using SciPy Stats, SQLAlchemy, and Flask.

## Climate Analysis
### Reflect Tables into SQLAlchemy ORM
* Python SQL toolkit and Object Relational Mapper modules
* Engine Creation and Reflection of existing database
* References to each table and Session creation
```
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///D:\Data Science\HW\8-SQLAlchemy\hawaii-weather-analysis\Resources\hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
```

### Exploratory Precipitation Analysis
* Query to find the most recent date
* Calculation of the date one year from the most recent date using Python Datetime module
* Query to find the precipitation scores using the calulated date of one year ago
* The query results saved as a DataFrame and a Pandas bar chart of these results
* Summary statistics of the precipitation data
```
# Find the most recent date in the data set.
session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date one year from the last date in the data set.
one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= one_year).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(prcp_scores, columns=['date','precipitation'])
df.set_index(df['date'], inplace=True)

# Sort the dataframe by date
sort_df = df.sort_index()

# Use Pandas Plotting with Matplotlib to plot the data
sort_df.plot(rot=90)
plt.xlabel('Date')
plt.ylabel('Inches')
plt.legend(loc=(.25,.85))
plt.show()

# Use Pandas to calcualte the summary statistics for the precipitation data
sort_df.describe()
```

### Exploratory Station Analysis
* Query to calculate the total number of stations in the dataset
* Query to show the most active stations
* Query to select the minimum, maximum, and average temperture observations of most active station
* Query of the last year of temperature observations of most acitve station and a Matplotlib histogram of the results
```
# Design a query to calculate the total number of stations in the dataset
session.query(func.count(Station.id)).all()

# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
session.query(Station.name, Measurement.station, func.count(Measurement.station)).\
        filter(Station.station == Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
        
# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
sel = [Station.station,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]
session.query(*sel).\
        filter(Station.station == 'USC00519281').all()

# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
most_active_station = session.query(Measurement.tobs).\
                                filter(Measurement.station == 'USC00519281').\
                                filter(Measurement.date >= one_year).all()

most_active_station_df = pd.DataFrame(most_active_station)

most_active_station_df.plot(kind='hist', bins=12)
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()
```

## temp_analysis_1
### Temperature Analysis I
* Python Datetime and SciPy Stats modules
* Read in of the temperature measurements CSV and DataFrame setup

### Compare June and December data across all years
* Filters of the data for June and December
* Calculations of average temperature for June and December from entire dataset
* Unpaired t-test of June and December temperatures
```
Ttest_indResult(statistic=31.60372399000329, pvalue=3.9025129038616655e-191)
```

## Temp Analysis 2
### Reflect Tables into SQLAlchemy ORM
* Python SQL Toolkit and Object Relational Mapper modules
* Engine Creation and Reflection of existing database
* References to each table and Session creation
### Temperature Analysis II
* Function named 'calc_temps' that accepts start and end dates to return the temperature mininum, average, and maximum for the range of dates
* 'calc_temps' function to return temperature minimums, averages, and maximums for a week in August 2017
* Matplotlib bar chart of the results from 'calc_temps' function for the week in August 2017
```
# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's 
# matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)]

results = session.query(*sel).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date >= '2017-08-01').\
    filter(Measurement.date <= '2017-08-07').\
    group_by(Station.station).\
    order_by(func.sum(Measurement.prcp).desc()).all()
```

### Daily Rainfall Average
* Query to select station location data and total amount of rainfall for the same week in August 2017
* Function named 'daily_normals' that accepts a month and day date and returns the temperature minimum, average, and maximum
* For loop with 'daily_normals' function to return the temperature miminums, averages, and maximums for the same August week
* Results saved as a DataFrame and a Pandas area plot of the results
```
# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's 
# matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)]

results = session.query(*sel).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date >= '2017-08-01').\
    filter(Measurement.date <= '2017-08-07').\
    group_by(Station.station).\
    order_by(func.sum(Measurement.prcp).desc()).all()

print(results)

def daily_normals(date):
  sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()

# Calculate the daily normals for your trip
# and push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip
start_date = '2017-08-01'
end_date = '2017-08-07'

# Use the start and end date to create a range of dates
dates_range = pd.date_range(start_date, end_date, freq='D')

# Store 'dates_range' as a list called 'trip_dates' for plotting
trip_dates = list(np.ravel((dates_range.strftime('%Y-%m-%d'))))

# Strip off the year and save a list of strings in the format %m-%d
trip_month_day = list(np.ravel(dates_range.strftime('%m-%d')))

# Use the `daily_normals` function to calculate the normals for each date string 
# and append the results to a list called `normals`.
normals = []

for x in trip_month_day:
    normals.append(list(np.ravel(daily_normals(x))))
    
# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index
trip_normals = pd.DataFrame(normals, index=trip_dates, columns=['tmin', 'tavg', 'tmax'])
trip_normals.index.names = ['date']
```

## App.py
* Python SQL toolkit, Object Relational Mapper, Flask, and Python Datetime modules
* Engine creation, references to the tables, and Flask setup
* Route to Homepage and 'welcome' function that reutrns the list of available API routes
* Route to Precipitation page and 'precipitation' function that returns Date-Precipiation dictionary in JSON format
* Route to Stations page and 'stations' function that returns a list in JSON format of all the stations
* Route to Temperature Observations (tobs) page and 'tobs' function that returns a list in JSON format of the latest year's tobs for the most active station
* Route to Start Date page and 'start' function that returns a list in JSON format of temperature minimums, averages, and maximums from a any chosen start date to the latest date in the dataset
* Route to Start and End Date page and 'start_end' function that returns a list in JSON format of temperature minimums, averages, and maximums from a any chosen start and end dates in the dataset
```
# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Calculate the date from 1 year ago
    one_year = dt.date(2017, 8, 23) - dt.datetime(days)

    # Query date and prcp
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()

    # Create a dictionary from results
    precipitation_dict = {}
    for date, prcp in prcp_scores:
        precipitation_dict[date] = prcp
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

    # Query stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query one year of temperature observations from the most active station
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs=tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    
    # Query the min. max, and average tobs for a given start and start-end dates 
    sel = [func.min(Measurement.tobs),
      func.avg(Measurement.tobs),
      func.max(Measurement.tobs)]
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).all()

    # List of temp min, avg, and max
    start_tobs = list(np.ravel(results))

    return jsonify(start_tobs=start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    # Query the min. max, and average tobs for a given start and start-end dates 
    sel = [func.min(Measurement.tobs),
      func.avg(Measurement.tobs),
      func.max(Measurement.tobs)]
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # List of temp min, avg, and max
    start_end_tobs = list(np.ravel(results))

    return jsonify(start_end_tobs=start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)
```

