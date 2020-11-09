var fs = require("fs");

function string64toDec(string) {
  let dec = 0;
//   console.log(string);
  for (let i = 0; i < string.length; i++) {
    //   console.log(string[i], i)
    c = Number(string[i]) * Math.pow(2, 63 - i);
    console.log(string[i], i, c);
    dec = c + dec;
  }

  //   4136353673894269217
  //   9223372036854776000

  return dec;
}

function byteString(bin) {
  let str = bin.toString(2);
  while (str.length < 8) {
    str = "0" + str;
  }
  return str;
}

const recordType = {
  0x00: "Debit",
  0x01: "Credit",
  0x02: "StartAutopay",
  0x03: "EndAutopay",
};

function getRecordType(arr, curr_idx) {
  if (arr[curr_idx] in recordType) {
    console.log(recordType[arr[curr_idx]]);
    return recordType[arr[curr_idx]];
  }
}

function createRecord(arr, hasAmount = false) {
  const newRecord = {
    type: recordType[arr[0]],
  };

  let timeStamp = "";
  for (let i = 1; i <= 4; i++) {
    timeStamp = timeStamp + byteString(arr[i]);
  }
  newRecord.unixTimeStamp = parseInt(timeStamp, 2);

  let userId = "";
  for (let i = 5; i <= 12; i++) {
    userId = userId + byteString(arr[i]);
  }
  console.log(userId);
  newRecord.userId = string64toDec(userId);

  return newRecord;
}

fs.readFile("txnlog.dat", function (err, data) {
  const mps7 =
    byteString(data[0]) +
    byteString(data[1]) +
    byteString(data[2]) +
    byteString(data[3]);
  const version = byteString(data[4]);
  const numOfRecords =
    byteString(data[5]) +
    byteString(data[6]) +
    byteString(data[7]) +
    byteString(data[8]);
  console.log("=== HEADER ===");
  console.log("MPS7 ", parseInt(mps7, 2));
  console.log("version ", parseInt(version, 2));
  console.log("# of records ", parseInt(numOfRecords, 2));

  const record1Type = data[9].toString();
  const record1Time =
    data[10].toString() +
    data[11].toString() +
    data[12].toString() +
    data[13].toString();
  const record1User =
    data[14].toString() +
    data[15].toString() +
    data[16].toString() +
    data[17].toString() +
    data[18].toString() +
    data[19].toString() +
    data[20].toString() +
    data[21].toString();
  const record1Dollars =
    data[22].toString() +
    data[23].toString() +
    data[24].toString() +
    data[25].toString() +
    data[26].toString() +
    data[27].toString() +
    data[28].toString() +
    data[29].toString();

  console.log("=== Data ===");
  console.log("type ", record1Type);
  console.log("time ", record1Time);
  console.log("user ", record1User);
  console.log("dollars ", record1Dollars);

  let count = 0;

  // idx start after header
  let i = 9;
  while (i < data.length) {
    const recordType = getRecordType(data, i);
    const range = recordType === "Debit" || recordType === "Credit" ? 21 : 13;
    console.log(createRecord(data.slice(i, i + range + 1)));

    i += range;
    count++;
  }
  console.log("records iterated ", count);
});
