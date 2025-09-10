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
      title: "מהפכת ה-AI בפיתוח: כלים, טכניקות ותובנות מעשיות",
      content: introContent,
    },
    articles: [
      {
        title: "למה Claude Code איטי בכוונה? Serena MCP פותר את הבעיה וחוסך לכם זמן",
        content: article1Content,
        img: "https://img.youtube.com/vi/wYWyJNs1HVk/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=wYWyJNs1HVk",
      },
      {
        title: "איך Claude Code בונה Lovable ב-75 דקות? הדגמה מרתקת של AI בפעולה",
        content: article2Content,
        img: "https://img.youtube.com/vi/_GMtx9EsIKU/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=_GMtx9EsIKU",
      },
      {
        title: "Vibe Coding בפרודקשן: איך Anthropic דחפו 22,000 שורות קוד של Claude לפרודקשן",
        content: article3Content,
        img: "https://img.youtube.com/vi/fHWFF_pnqDk/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=fHWFF_pnqDk",
      },
      {
        title: "400 שעות ב-Cursor: הלקחים המתקדמים של עבודה עם AI IDE",
        content: article4Content,
        img: "https://img.youtube.com/vi/gYLNxUxVomY/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=gYLNxUxVomY",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;