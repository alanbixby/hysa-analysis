# %%
import json
from datetime import datetime, timedelta
from operator import itemgetter

import plotly.graph_objs as go
import pytz
from dateutil import parser

# Read the JSON file
with open('./input/combinedSavings.json') as json_file:
    savings_records_json = json.load(json_file)

timezone = pytz.timezone("UTC")

# filter the records that the oldest history entry is less than 5 years ago
savings_records = [record for record in savings_records_json if len(record["history"]) > 0 and parser.parse(record["history"][0][0]).replace(tzinfo=timezone) > (datetime.now(timezone) - timedelta(days=365 * 5))]

# set the attribute apy to the value of the latest history entry
for record in savings_records:
    record["apy"] = record["history"][-1][1]

# Sort the records by current APY
savings_records.sort(key=itemgetter("apy"), reverse=True)

# Take the top 25 savings institutions
savings_records = savings_records[:25]

# Add in 305301, 373739, and 314018
savings_records = savings_records + [record for record in savings_records_json if record["id"] in [305301, 373739, 314018, 264559, 392219]]

# Create a list to hold the data for the chart
data = []

# Loop through the array of savings records
for record in savings_records:
    # Extract the history attribute for the current record
    history = record["history"]

    # Create arrays to hold the data for the current record's chart
    dates = []
    apy_values = []

    # Loop through the history data and add it to the chart data
    for date, apy_value in history:
        date_time = parser.parse(date).replace(tzinfo=timezone)
        dates.append(date_time)
        apy_values.append(apy_value)

    # Create a line chart using the data
    trace = go.Scatter(x=dates, y=apy_values, name=record["name"] + " " + str(history[-1][1]) + "%")
    data.append(trace)

# data = sorted(data, key=lambda trace: trace.name)

layout = go.Layout(title="Last 5 Years, APY over Time", xaxis=dict(title='Dates'), yaxis=dict(title='APY'))

# restrict x axis to the last 5 years
layout.xaxis.range = [datetime.now(timezone) - timedelta(days=365 * 5), datetime.now(timezone)]

fig = go.Figure(data=data, layout=layout)

# Show the chart
fig.show()
# %%
