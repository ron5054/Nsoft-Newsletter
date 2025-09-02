const newsletterFolder = "newsletter-23";

const handlebars = require("handlebars");
const fs = require("fs");
const path = require("path");
const liveServer = require("live-server");
const glob = require("glob");

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

// Dynamically find all .js and .html files excluding node_modules
const watchedFiles = glob.sync("**/*.{js,html,hbs}", {
  ignore: ["**/node_modules/**", "**/output.html"]
});

console.log("🔍 Watching for changes in newsletter files...");

watchedFiles.forEach(file => {
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
  root: path.join(__dirname),
  open: "/index.html",
  file: "index.html",
  wait: 1000,
  mount: [['/images', './images']],
  logLevel: 2
};

console.log("🚀 Starting live server...");
console.log(`📱 Opening http://localhost:8080/index.html`);
console.log("Press Ctrl+C to stop");

liveServer.start(serverParams);
