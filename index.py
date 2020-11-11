from mainframe import MainFrame

with open("txnlog.dat", mode='rb') as file: # b is important -> binary
    fileContent = file.read()

m = MainFrame(fileContent)

print("Total amount of dollars in debits:", m.amountTotal(m.recordTypes[0x00]))
print("Total amount of dollars in credits:", m.amountTotal(m.recordTypes[0x01]))
print("Total autopays started:", m.countRecordType(m.recordTypes[0x02]))
print("Total autopays ended:", m.countRecordType(m.recordTypes[0x03]))
print("UserID 2456938384156277127 balance:", m.userBalanceById(2456938384156277127))

m.printAllRecords()