const newsletterFolder = "newsletter-23";

const handlebars = require("handlebars");
const fs = require("fs");
const path = require("path");
const liveServer = require("live-server");

// Function to compile newsletter
const compileNewsletter = () => {
  try {
    // Load the template from a file
    const templateSource = fs.readFileSync("./template-2.hbs", "utf8");

    // Load the JSON data from a file or API response
    const compileData = require(`./${newsletterFolder}/data.js`);
    const data = compileData(`${newsletterFolder}`);

    console.log("📝 Compiling newsletter...");

    const template = handlebars.compile(templateSource);
    const htmlOutput = template(data);
    
    fs.writeFileSync(`./${newsletterFolder}/output.html`, htmlOutput, "utf8");
    console.log(`✅ Newsletter compiled successfully to ${newsletterFolder}/output.html`);
  } catch (error) {
    console.error("❌ Compilation error:", error.message);
  }
};

// Initial compilation
compileNewsletter();

// Watch for changes in article files
const articleFiles = [
  `./${newsletterFolder}/intro.html`,
  `./${newsletterFolder}/article-1.html`,
  `./${newsletterFolder}/article-2.html`,
  `./${newsletterFolder}/article-3.html`,
  `./${newsletterFolder}/article-4.html`,
  `./template-2.hbs`,
  `./${newsletterFolder}/data.js`
];

console.log("🔍 Watching for changes in newsletter files...");

articleFiles.forEach(file => {
  fs.watchFile(file, (curr, prev) => {
    if (curr.mtime > prev.mtime) {
      console.log(`📝 ${file} changed, recompiling...`);
      compileNewsletter();
    }
  });
});

// Configure live server
const serverParams = {
  port: 8080,
  host: "0.0.0.0",
  root: path.join(__dirname, newsletterFolder),
  open: "/output.html",
  file: "output.html",
  wait: 1000,
  mount: [['/images', './images']],
  logLevel: 2
};

console.log("🚀 Starting live server...");
console.log(`📱 Opening http://localhost:8080/output.html`);
console.log("Press Ctrl+C to stop");

liveServer.start(serverParams);
