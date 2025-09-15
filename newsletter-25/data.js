const fs = require('fs');

function buildJson(directoryName) {
    const introContent = fs.readFileSync(`./${directoryName}/intro.html`, 'utf8');
    const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, 'utf8');
    const article2Content = fs.readFileSync(`./${directoryName}/article-2.html`, 'utf8');
    const article3Content = fs.readFileSync(`./${directoryName}/article-3.html`, 'utf8');
    const article4Content = fs.readFileSync(`./${directoryName}/article-4.html`, 'utf8');

    return {
        intro: {
            title: "טכניקות מתקדמות בפיתוח מודרני",
            content: introContent,
        },
        articles: [
            {
                title: "TanStack DB: מהפכה בניהול מידע באפליקציות ווב",
                content: article1Content,
                img: "https://img.youtube.com/vi/bfOmM1FKsaQ/maxresdefault.jpg",
                url: "https://www.youtube.com/watch?v=bfOmM1FKsaQ"
            },
            {
                title: "React Query Selectors: אופטימיזציה מתקדמת לביצועים",
                content: article2Content,
                img: "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg",
                url: "https://tkdodo.eu/blog/react-query-selectors-supercharged"
            },
            {
                title: "נגזור State מהשרת: עקרון עיצוב חכם",
                content: article3Content,
                img: "https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png",
                url: "https://tkdodo.eu/blog/deriving-client-state-from-server-state"
            },
            {
                title: "useCallback: מתי באמת צריך ומתי זה מיותר",
                content: article4Content,
                img: "https://blog-cdn.codefinity.com/images/84cf0089-4483-4124-8388-a52baff28a6e_8fcdc9988f47418092f5013c41d6f358.png.png",
                url: "https://tkdodo.eu/blog/the-useless-use-callback"
            }
        ],
        unsubscribe_url: "{{unsubscribe_url}}",
        message_content: "{{message_content}}",
        subscriber: { first_name: "{{subscriber.first_name}}" }
    };
}

module.exports = buildJson;