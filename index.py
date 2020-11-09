
with open("txnlog.dat", mode='rb') as file: # b is important -> binary
    fileContent = file.read()

for thing in fileContent:
    print(thing)