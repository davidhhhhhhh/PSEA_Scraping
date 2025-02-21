import requests
import re
import json
import pandas as pd

# Step 1: Fetch the data
url = "https://flo.uri.sh/visualisation/19069509/embed?auto=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise ValueError(f"Failed to fetch data: {response.status_code}")

# Step 2: Debugging - Print occurrences of "_Flourish_data"
flourish_occurrences = [m.start() for m in re.finditer(r"_Flourish_data", response.text)]
print(f"Found _Flourish_data {len(flourish_occurrences)} times in the response.")

# Step 3: Extract using boundary regex
flourish_data_pattern = re.compile(
    r"_Flourish_data\s*=\s*({.*?})\s*,\s*\"regions_geometry\"",
    re.DOTALL
)


match = flourish_data_pattern.search(response.text)

if not match:
    print("Response snippet around _Flourish_data:")
    print(response.text.split("_Flourish_data")[1][:1000])  # Debug snippet
    raise ValueError("Could not find _Flourish_data in the response.")

flourish_js = match.group(1)

# Step 4: Clean non-JSON syntax
flourish_js_cleaned = re.sub(
    r"new Date\((\d+)\)",
    lambda m: f'"{pd.to_datetime(int(m.group(1)), unit="ms").isoformat()}"',
    flourish_js
)

# Step 5: Parse JSON
flourish_data = json.loads(flourish_js_cleaned)

# Step 6: Extract and clean data
regions_data = flourish_data.get("regions", [])
cleaned_data = []
for region in regions_data:
    metadata = region.get("metadata", [])
    state_info = {
        "State": region.get("id", ""),
        "Data Current Through": metadata[0] if len(metadata) > 0 else None,
        "Solar Installed (MW)": metadata[1] if len(metadata) > 1 else None,
        "National Ranking": metadata[2] if len(metadata) > 2 else None,
        "Enough Solar Installed to Power": metadata[3] if len(metadata) > 3 else None,
        "Percentage of State's Electricity from Solar": metadata[4] if len(metadata) > 4 else None,
        "Solar Jobs": metadata[5] if len(metadata) > 5 else None,
        "Link": metadata[6] if len(metadata) > 6 else None,
    }
    cleaned_data.append(state_info)

df = pd.DataFrame(cleaned_data)
print(df)