const compressor = require("./compressor");

if (process.argv.length < 3){
    console.error("argument expexted");
    process.exit(1);
}


console.log(compressor.o.compressToBase64(process.argv[2]));
