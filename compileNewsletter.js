const newsletterFolder = "newsletter-23";

const handlebars = require("handlebars");
const fs = require("fs");

// Load the template from a file
const templateSource = fs.readFileSync("./template-2.hbs", "utf8");

// Load the JSON data from a file or API response
// const jsonData = JSON.parse(fs.readFileSync("./newsletter-10/data.js", "utf8"));
const compileData = require(`./${newsletterFolder}/data.js`);
const data = compileData(`${newsletterFolder}`);

console.log("data", data);

const template = handlebars.compile(templateSource);

const htmlOutput = template(data);
fs.writeFileSync(`./${newsletterFolder}/output.html`, htmlOutput, "utf8");
console.log(htmlOutput);
