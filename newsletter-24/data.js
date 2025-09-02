const fs = require("fs");

function buildJson(directoryName) {
  const introContent = fs.readFileSync(`./${directoryName}/intro.html`, "utf8");
  const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, "utf8");
  const article2Content = fs.readFileSync(`./${directoryName}/article-2.html`, "utf8");
  const article3Content = fs.readFileSync(`./${directoryName}/article-3.html`, "utf8");
  const article4Content = fs.readFileSync(`./${directoryName}/article-4.html`, "utf8");

  return {
    intro: {
      title: "טכנולוגיות React מתקדמות",
      content: introContent,
    },
    articles: [
      {
        title: "TanStack DB - המהפכה החדשה",
        content: article1Content,
        img: "https://img.youtube.com/vi/bfOmM1FKsaQ/maxresdefault.jpg",
        url: "https://www.youtube.com/watch?v=bfOmM1FKsaQ",
      },
      {
        title: "React Query Selectors - כלי סודי",
        content: article2Content,
        img: "https://media.licdn.com/dms/image/v2/D4D16AQGTluEAsi1FRw/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1704992863787?e=2147483647&v=beta&t=KFQrD9tpODUNnkTe06w3rtzdCaUozeJBy_oUsUtAoYk",
        url: "https://www.linkedin.com/posts/nadavleb_react-query-selectors-supercharged-activity-7367857622911311874-jBrw?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEEhIvABoTlOznpn5Fnnz84WLmYc_okCPkg",
      },
      {
        title: "אמנות העבודה עם Coding Agents",
        content: article3Content,
        img: "https://media.licdn.com/dms/image/v2/D4D16AQGTluEAsi1FRw/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1704992863787?e=2147483647&v=beta&t=KFQrD9tpODUNnkTe06w3rtzdCaUozeJBy_oUsUtAoYk",
        url: "https://www.linkedin.com/posts/nadavleb_coding-agents-101-the-art-of-actually-getting-activity-7366814659280015360-sA-n?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEEhIvABoTlOznpn5Fnnz84WLmYc_okCPkg",
      },
      {
        title: "useCallback - מתי זה באמת שווה?",
        content: article4Content,
        img: "https://media.licdn.com/dms/image/v2/D4D16AQGTluEAsi1FRw/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1704992863787?e=2147483647&v=beta&t=KFQrD9tpODUNnkTe06w3rtzdCaUozeJBy_oUsUtAoYk",
        url: "https://www.linkedin.com/posts/nadavleb_the-useless-usecallback-activity-7363134222011711488-N0Nk?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEEhIvABoTlOznpn5Fnnz84WLmYc_okCPkg",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;