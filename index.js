var fs = require("fs");

fs.readFile("txnlog.dat", function (err, data) {
  console.log(data);
  // for(let i=0; i<data.length; i++) {
  //     const string = String(data[i])
  //     console.log("i", i, string)
  //     // console.log(data.readInt8())
  // }
  const mps7 =
    data[0].toString() +
    data[1].toString() +
    data[2].toString() +
    data[3].toString();
  const version = data[4].toString();
  const numOfRecords =
    data[5].toString() +
    data[6].toString() +
    data[7].toString() +
    data[8].toString();
  console.log("=== HEADER ===");
  console.log("MPS7 ", mps7);
  console.log("version ", version);
  console.log("# of records ", numOfRecords);

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
});
