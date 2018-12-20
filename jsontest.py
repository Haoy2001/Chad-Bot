import json

with open("data/coin.json", "r") as infile:
    data = json.load(infile)
    infile.close()

print(data)


cfrom = '31139254648722685952'
cto = '44717923649093468160'
amount = 1

if not data.__contains__(str(cfrom)):
    data[cfrom] = 0

if not data.__contains__(str(cto)):
    data[cto] = 0

if data[cfrom] < amount:
    print("Not enough money")
else:
    data[cfrom] -= amount
    data[cto] += amount

print(data)

with open("data/coin.json", "w") as write_file:
    json.dump(data, write_file)
    write_file.close()

