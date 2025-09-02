const fs = require("fs");

function buildJson(directoryName) {
  const introContent = fs.readFileSync(`./${directoryName}/intro.html`, "utf8");

  const article1Content = fs.readFileSync(
    `./${directoryName}/article-1.html`,
    "utf8"
  );
  const article2Content = fs.readFileSync(
    `./${directoryName}/article-2.html`,
    "utf8"
  );
  const article3Content = fs.readFileSync(
    `./${directoryName}/article-3.html`,
    "utf8"
  );

  const article4Content = fs.readFileSync(
    `./${directoryName}/article-4.html`,
    "utf8"
  );

  return {
    intro: {
      title: "לונג טיים נו סי",
      content: introContent,
    },
    articles: [
      {
        title: "Agentic AI - כשהסקייל הופך קריטי",
        content: article1Content,
        img: "https://img.youtube.com/vi/12v5S1n1eOY/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=12v5S1n1eOY",
      },
      {
        title: "Claude Code Subagents - העתיד של פיתוח עם Meta Agent",
        content: article2Content,
        img: "https://img.youtube.com/vi/7B2HJr0Y68g/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=7B2HJr0Y68g",
      },
      {
        title: "RAG בפרודקשן - למה רוב המערכות קורסות",
        content: article3Content,
        img: "https://img.youtube.com/vi/kPL-6-9MVyA/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=kPL-6-9MVyA",
      },
      {
        title: "Claude Code vs Cursor - ההבדל האמיתי",
        content: article4Content,
        img: "https://img.youtube.com/vi/i0P56Pm1Q3U/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=i0P56Pm1Q3U",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;
