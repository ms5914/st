
import csv
# 1. Basic CSV reading
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for row in reader:
        print(row)  # row is a list: ['acct_123', '1', 'usd', '1000']


# 2. CSV as dictionaries (keys = header names)
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)  # {'account_name': 'acct_123', 'timestamp': '1', ...}

# 3. Writing CSV
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age'])       # header
    writer.writerow(['Alice', 30])         # single row
    writer.writerows([['Bob', 25], ['Carol', 28]])  # multiple rows


import json
# 1. Read JSON file
with open('data.json', 'r') as f:
    data = json.load(f)        # returns dict or list
print(data['key'])

# 2. Parse JSON string
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)  # load"s" = load string
print(data['name'])

# 3. Write JSON file
data = {"name": "Alice", "scores": [90, 85, 92]}
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)  # indent for pretty printing