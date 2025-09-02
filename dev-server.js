const handlebars = require("handlebars");
const fs = require("fs");
const path = require("path");
const liveServer = require("live-server");
const glob = require("glob");

// Auto-detect the latest newsletter folder
const getLatestNewsletterFolder = () => {
  const folders = fs.readdirSync('.').filter(name => 
    fs.statSync(name).isDirectory() && name.match(/^newsletter-\d+$/)
  );
  if (folders.length === 0) return null;
  
  // Sort by number and get the highest
  return folders.sort((a, b) => {
    const numA = parseInt(a.match(/newsletter-(\d+)/)[1]);
    const numB = parseInt(b.match(/newsletter-(\d+)/)[1]);
    return numB - numA;
  })[0];
};

const defaultFolder = getLatestNewsletterFolder() || "newsletter-23";

// Function to compile newsletter
const compileNewsletter = (folder) => {
  try {
    console.log(`📝 Compiling ${folder}...`);
    
    // Clear require cache for data.js to get fresh data
    const dataPath = path.resolve(`./${folder}/data.js`);
    delete require.cache[dataPath];
    
    // Load the template from a file
    const templateSource = fs.readFileSync("./template-2.hbs", "utf8");

    // Load the JSON data from a file or API response
    const compileData = require(`./${folder}/data.js`);
    const data = compileData(`${folder}`);

    const template = handlebars.compile(templateSource);
    const htmlOutput = template(data);

    fs.writeFileSync(`./${folder}/output.html`, htmlOutput, "utf8");
    console.log(`✅ Newsletter compiled successfully to ${folder}/output.html`);
  } catch (error) {
    console.error("❌ Compilation error:", error.message);
  }
};

// Initial compilation
compileNewsletter(defaultFolder);

// Dynamically find all .js and .html files excluding node_modules and output files
const watchedFiles = glob.sync("**/*.{js,html,hbs}", {
  ignore: [
    "**/node_modules/**",
    "**/output.html",
    "**/*output.html"
  ]
});

console.log("🔍 Watching for changes in newsletter files...");

watchedFiles.forEach(file => {
  // Skip output.html files to prevent infinite loops
  if (file.includes('output.html')) {
    return;
  }
  
  fs.watchFile(file, (curr, prev) => {
    if (curr.mtime > prev.mtime) {
      console.log(`📝 ${file} changed, recompiling...`);
      
      // Determine which newsletter folder to compile based on the changed file
      const folderMatch = file.match(/newsletter-(\d+)\//);
      if (folderMatch) {
        const targetFolder = `newsletter-${folderMatch[1]}`;
        compileNewsletter(targetFolder);
      } else {
        // If not in a newsletter folder, compile the default
        compileNewsletter(defaultFolder);
      }
    }
  });
});

// Configure live server - exclude output.html files to prevent page reloads
const serverParams = {
  port: 8080,
  host: "0.0.0.0",
  root: path.join(__dirname),
  open: "/index.html",
  wait: 1000,
  mount: [['/images', './images']],
  logLevel: 2,
  ignore: "**/output.html"
};

console.log("🚀 Starting live server...");
console.log(`📱 Opening http://localhost:8080/index.html`);
console.log("Press Ctrl+C to stop");

liveServer.start(serverParams);
