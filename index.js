var fs = require('fs');

fs.readFile('txnlog.dat', function(err, data) {
    console.log(data)
    for(let i=0; i<data.length; i++) {
        console.log("i", i, String(data[i]))
        // console.log(data.readInt8())
    }
})