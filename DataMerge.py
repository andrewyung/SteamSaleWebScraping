'''
Combine 2 json files (duplicates are only added once). Merge used if data from multiple genres needed
'''
import json

with open("dataAction1.json") as fo:
    data1 = json.load(fo)

with open("dataComplete1.json") as fo:
    data2 = json.load(fo)

print (len(data1))
print (len(data2))

data1.update(data2)

unique_stuff = { each : each for each in data1 }.values()

print (len(data1))
with open("dataComplete1.json", "w") as fo:
    json.dump(data1, fo)