from float_bin import bin_to_float

with open("txnlog.dat", mode='rb') as file: # b is important -> binary
    fileContent = file.read()

recordTypes = {
    0x00: "Debit",
    0x01: "Credit",
    0x02: "StartAutopay",
    0x03: "EndAutopay"
}

def byteString(bin):
    return '{0:08b}'.format(bin)


def getRecordType(arr, curr_idx):
    if arr[curr_idx] in recordTypes.keys():
        # print(recordTypes[arr[curr_idx]])
        return recordTypes[arr[curr_idx]]

def createRecord(arr):
    newRecord = {
        "recordType": recordTypes[arr[0]]
    }

    timeStamp = ""
    for i in range(1, 5):
        timeStamp = timeStamp + byteString(arr[i])
    newRecord["timeStamp"] = int(timeStamp, 2)

    userId = ""
    for i in range(5, 13):
        userId = userId + byteString(arr[i])
    newRecord["userId"] = int(userId, 2)

    if len(arr) == 21:
        
        amount = ""
        for i in range(13, 21):
            amount = amount + byteString(arr[i])
        newRecord["amount"] = bin_to_float(amount)

    return newRecord


print("=== HEADER ===")
mps7 = byteString(fileContent[0]) + byteString(fileContent[1]) + byteString(fileContent[2]) + byteString(fileContent[3])
version = byteString(fileContent[4])
numOfRecords = byteString(fileContent[5]) + byteString(fileContent[6]) + byteString(fileContent[7]) + byteString(fileContent[8])
print("MPS7 ", int(mps7, 2))
print("Version ", int(version, 2))
print("# of records ", int(numOfRecords, 2))

records = []

count = 0
idx = 9

while idx < len(fileContent):
    recordType = getRecordType(fileContent, idx)
    r = 21 if recordType == "Debit" or recordType == "Credit" else 13

    newRecord = createRecord(fileContent[idx:idx+r])
    records.append(newRecord)

    idx += r

for r in records:
    print(r)