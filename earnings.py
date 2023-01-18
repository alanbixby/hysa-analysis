#%%
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
import pytz
from dateutil import parser

with open("./input/combinedSavings.json", "r") as json_file:
    data = json.load(json_file)

def calculate_earnings(data: List[Dict[str, Any]], starting_principal: float, years: int = 3) -> Dict[str, float]:
    earnings: Dict[str, float] = {}
    for institution in data:
        name = institution["name"]
        history = institution["history"]

        if (len(history) < 1 or parser.parse(history[0][0]) > (datetime.now() - timedelta(days=years*365)).replace(tzinfo=pytz.timezone('utc'))):
            continue
        
        history_df = pd.DataFrame(history,columns=["date","apy"])
        history_df["date"] = pd.to_datetime(history_df["date"])
        history_df = history_df.set_index("date").resample("D").ffill().tail(-1)
        filtered_df = history_df[(datetime.now() - timedelta(days=years*365)).replace(tzinfo=pytz.timezone('utc')):(datetime.now().replace(tzinfo=pytz.timezone('utc')))]
        
        principal: float = starting_principal
        for _, apy in filtered_df.itertuples():
            principal = principal * (1 + apy / 365)
        
        earnings[name] = principal - starting_principal
    
    earnings = {k: v for k, v in sorted(earnings.items(), key=lambda item: item[1], reverse=True)}

    if (years < 1):
        unit = f"month{int(years * 12)}" 
    else:
        unit = f"year{years}"

    with open(f'./output/output_{unit}.json', 'w') as f:
        json.dump(earnings, f, indent=2)

    return earnings

for i in range(1, 12):
    calculate_earnings(data, 10000, i/12)
    print(f"ran {i}")
for i in range(1, 14):
    calculate_earnings(data, 10000, i)
    print(f"ran {i}")
# %%
