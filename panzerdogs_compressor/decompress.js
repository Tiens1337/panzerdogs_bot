const compressor = require("./compressor");

if (process.argv.length < 3){
    console.error("argument expexted");
    process.exit(1);
}

let data = process.argv[2];

console.log(compressor.o.decompressFromBase64(data));
