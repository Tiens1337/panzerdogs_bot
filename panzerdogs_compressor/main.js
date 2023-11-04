const compressor = require("./compressor");

console.log(compressor);
let data = "N4Igtg9gbgpgIgSwM4BcCGA7AxjEAuANgIBoQAjCCVRVTHfARgFZSATMAczhjQBsV8AFgCcABlGkA1gl68k+FiABmCAE6oAQr0qtGbTgCUYOBLF15BAZgAcAXyA=";

let compressed = compressor.o.compressToBase64(JSON.stringify({"hello":"asd"}));
console.log(compressed);

let decompressed = compressor.o.decompressFromBase64(data);
console.log(decompressed);

console.log(compressor.o.compressToBase64(decompressed))

a=1