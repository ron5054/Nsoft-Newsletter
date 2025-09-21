const fs = require('fs');

function buildJson(directoryName) {
    const introContent = fs.readFileSync(`./${directoryName}/intro.html`, 'utf8');
    const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, 'utf8');
    const article2Content = fs.readFileSync(`./${directoryName}/article-2.html`, 'utf8');
    const article3Content = fs.readFileSync(`./${directoryName}/article-3.html`, 'utf8');
    const article4Content = fs.readFileSync(`./${directoryName}/article-4.html`, 'utf8');

    return {
        intro: {
            title: "כלים מתקדמים לפיתוח ובינה מלאכותית",
            content: introContent,
        },
        articles: [
            {
                title: "Cursor AI Agents: עבודה כמו 10 מפתחים",
                content: article1Content,
                img: "https://img.youtube.com/vi/8QN23ZThdRY/maxresdefault.jpg",
                url: "https://www.youtube.com/watch?v=8QN23ZThdRY"
            },
            {
                title: "TanStack DB: המדריך האינטראקטיבי החדש",
                content: article2Content,
                img: "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg",
                url: "https://frontendatscale.com/blog/tanstack-db/"
            },
            {
                title: "ניקוי קוד עם nip: הסרת JavaScript מת",
                content: article3Content,
                img: "https://img.youtube.com/vi/uhEkgWt-pUM/maxresdefault.jpg",
                url: "https://www.youtube.com/watch?v=uhEkgWt-pUM"
            },
            {
                title: "המעבר ל-AI Engineering: מדריך מעשי",
                content: article4Content,
                img: "https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png",
                url: "https://x.com/akshay_pachaar/status/1954158220727263311"
            }
        ],
        unsubscribe_url: "{{unsubscribe_url}}",
        message_content: "{{message_content}}",
        subscriber: { first_name: "{{subscriber.first_name}}" }
    };
}

module.exports = buildJson;