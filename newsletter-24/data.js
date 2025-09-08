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
      title: "הפיתוח החכם: כשהטכנולוגיה פוגשת אסטרטגיה",
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
        title: "למה לנהל State במקום לגזור אותו? עקרון מהפכני בפיתוח React",
        content: article2Content,
        img: "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg",
        url: "https://tkdodo.eu/blog/deriving-client-state-from-server-state",
      },
      {
        title: "Vibe Coding בפרודקשן: איך Anthropic דחפו 22,000 שורות קוד של Claude לפרודקשן",
        content: article3Content,
        img: "https://img.youtube.com/vi/fHWFF_pnqDk/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=fHWFF_pnqDk",
      },
      {
        title: "TanStack DB: המהפכה הבאה בניהול State לאפליקציות ווב",
        content: article4Content,
        img: "https://img.youtube.com/vi/bfOmM1FKsaQ/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=bfOmM1FKsaQ",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;