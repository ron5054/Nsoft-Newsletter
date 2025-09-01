const newsletterFolder = "newsletter-23";

const handlebars = require("handlebars");
const fs = require("fs");

// Function to update index.html with new newsletter
function updateIndexWithNewsletter(folder, data) {
  try {
    const indexPath = "./index.html";
    if (!fs.existsSync(indexPath)) {
      console.log("⚠️ index.html not found, skipping newsletter list update");
      return;
    }

    let indexContent = fs.readFileSync(indexPath, "utf8");
    
    // Extract newsletter info
    const newsletterInfo = {
      folder: folder,
      title: data.intro?.title || `Newsletter ${folder.split('-')[1]}`,
      description: data.intro?.content?.replace(/<[^>]*>/g, '').substring(0, 150) + '...' || 'ללא תיאור זמין'
    };

    // Find the availableNewsletters array
    const arrayStart = indexContent.indexOf('const availableNewsletters = [');
    const arrayEnd = indexContent.indexOf('];', arrayStart) + 2;
    
    if (arrayStart === -1) {
      console.log("⚠️ Could not find availableNewsletters array in index.html");
      return;
    }

    // Extract current array content
    const currentArrayContent = indexContent.substring(arrayStart, arrayEnd);
    
    // Check if this newsletter already exists
    if (currentArrayContent.includes(`folder: '${folder}'`)) {
      console.log(`📄 Newsletter ${folder} already exists in index.html`);
      return;
    }

    // Find the closing bracket and add new newsletter
    const closingBracketIndex = indexContent.lastIndexOf('];', arrayEnd);
    const beforeClosing = indexContent.substring(0, closingBracketIndex);
    const afterClosing = indexContent.substring(closingBracketIndex);
    
    // Determine if we need a comma (check if array is empty or has items)
    const needsComma = currentArrayContent.includes('folder:');
    const comma = needsComma ? ',' : '';
    
    const newEntry = `${comma}
            {
                folder: '${newsletterInfo.folder}',
                title: '${newsletterInfo.title.replace(/'/g, "\\'")}',
                description: '${newsletterInfo.description.replace(/'/g, "\\'")}'
            }`;

    const updatedContent = beforeClosing + newEntry + '\n            // Add more newsletters here as they are created\n        ' + afterClosing;
    
    fs.writeFileSync(indexPath, updatedContent, "utf8");
    console.log(`📝 Added ${folder} to newsletter list in index.html`);
    
  } catch (error) {
    console.error("❌ Error updating index.html:", error.message);
  }
}

// Function to compile newsletter
function compileNewsletter() {
  try {
    // Load the template from a file
    const templateSource = fs.readFileSync("./template-2.hbs", "utf8");

    // Load the JSON data from a file or API response
    const compileData = require(`./${newsletterFolder}/data.js`);
    const data = compileData(`${newsletterFolder}`);

    console.log("Compiling newsletter...");

    const template = handlebars.compile(templateSource);
    const htmlOutput = template(data);
    
    fs.writeFileSync(`./${newsletterFolder}/output.html`, htmlOutput, "utf8");
    console.log(`✅ Newsletter compiled successfully to ${newsletterFolder}/output.html`);
    
    // Update index.html with this newsletter
    updateIndexWithNewsletter(newsletterFolder, data);
    
  } catch (error) {
    console.error("❌ Compilation error:", error.message);
  }
}

// Initial compilation
compileNewsletter();

// Watch for changes in article files
const articleFiles = [
  `./${newsletterFolder}/intro.html`,
  `./${newsletterFolder}/article-1.html`,
  `./${newsletterFolder}/article-2.html`,
  `./${newsletterFolder}/article-3.html`,
  `./${newsletterFolder}/article-4.html`
];

console.log("🔍 Watching for changes in article files...");
console.log("Press Ctrl+C to stop watching");

articleFiles.forEach(file => {
  fs.watchFile(file, (curr, prev) => {
    if (curr.mtime > prev.mtime) {
      console.log(`📝 ${file} changed, recompiling...`);
      compileNewsletter();
    }
  });
});
