from codecs import decode
import struct

class MainFrame:
    recordTypes = {
        0x00: "Debit", 
        0x01: "Credit", 
        0x02: "StartAutopay", 
        0x03: "EndAutopay" 
    }

    def __init__(self, fileData):
        self.records = self.createRecordsList(fileData)

    def byteString(self, bin):
        return '{0:08b}'.format(bin)

    def bin_to_float(self, b):
        """ Convert binary string to a float. """
        bf = self.int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
        return struct.unpack('>d', bf)[0]

    def int_to_bytes(self, n, length):  # Helper function
        """ Int/long to byte string.

            Python 3.2+ has a built-in int.to_bytes() method that could be used
            instead, but the following works in earlier versions including 2.x.
        """
        return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]
    
    def getRecordType(self, entry):
        if entry in self.recordTypes.keys():
            return self.recordTypes[entry]

    def createRecord(self, subArr):
        newRecord = {
            "recordType": self.recordTypes[subArr[0]]
        }

        timeStamp = ""
        for i in range(1, 5):
            timeStamp = timeStamp + self.byteString(subArr[i])
        newRecord["timeStamp"] = int(timeStamp, 2)

        userId = ""
        for i in range(5, 13):
            userId = userId + self.byteString(subArr[i])
        newRecord["userId"] = int(userId, 2)

        if len(subArr) == 21:
            amount = ""
            for i in range(13, 21):
                amount = amount + self.byteString(subArr[i])
            newRecord["amount"] = self.bin_to_float(amount)
        else:
            newRecord["amount"] = None
        

        return newRecord
    
    def createRecordsList(self, data):
        recordList = []
        # first idx of body
        idx = 9
        while idx < len(data):
            rType = self.getRecordType(data[idx])
            r = 21 if rType == "Debit" or rType == "Credit" else 13

            newRecord = self.createRecord(data[idx:idx+r])
            recordList.append(newRecord)

            idx += r
        return recordList

    def amountTotal(self, recordType):
        total = 0
        for r in self.records:
            if r["recordType"] == recordType:
                total += r["amount"]
        return total

    def countRecordType(self, recordType):
        count = 0
        for r in self.records:
            if r["recordType"] == recordType:
                count += 1
        return count

    def userBalanceById(self, id):
        balance = 0
        for r in self.records:
            if r["userId"] == id:
                if r["recordType"] == self.recordTypes[0x00]:
                    balance += r["amount"]
                elif r["recordType"] == self.recordTypes[0x01]:
                    balance -= r["amount"]
        return balance

    def printAllRecords(self):
        count = 0
        for r in self.records:
            if not count % 10:
                self.printLabel()
            count += 1
            idLen = 20-len(str(r['userId']))
            idPadding = " "*idLen
            amountLen = 20
            if r['amount'] is not None:
                amountLen = 20-len(str(r['amount']))
            amountPadding = " "*amountLen
            if 'Start' in r['recordType']:
                print(f"||  Start Autopay  ||  {r['timeStamp']}  ||  {r['userId']}{idPadding}  ||  {amountPadding}  ||")
            elif 'End' in r['recordType']:
                print(f"||  End Autopay    ||  {r['timeStamp']}  ||  {r['userId']}{idPadding}  ||  {amountPadding}  ||")
            elif 'Debit' in r['recordType']:
                print(f"||  {r['recordType']}          ||  {r['timeStamp']}  ||  {r['userId']}{idPadding}  ||  {r['amount']}{amountPadding}  ||")
            elif 'Credit' in r['recordType']:
                print(f"||  {r['recordType']}         ||  {r['timeStamp']}  ||  {r['userId']}{idPadding}  ||  {r['amount']}{amountPadding}  ||")
        if count % 10:
            print("||=================||==============||========================||========================||")    

    def printLabel(self):
        print("||=================||==============||========================||========================||")
        print("|| Type            || Time Stamp   || User ID                || Amount                 ||")
        print("||=================||==============||========================||========================||")