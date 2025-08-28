# מדריך יצירת ניוזלטר חדש

## סקירה כללית
יצירת ניוזלטר חדש עם 4 מאמרים ותוכן עברי, בעקבות אותו מבנה כמו newsletter-23.

## תהליך שלב אחר שלב

### 1. יצירת מבנה תיקיות
```bash
mkdir -p packages/html-emails/newsletter/newsletter-XX
```

### 2. יצירת קבצי תוכן
צור את הקבצים הבאים בתיקיית newsletter-XX:

#### intro.html
- כתוב כותרת מבוא מרתקת (2-3 מילים מקסימום)
- 2-3 פסקאות המסבירות את נושא הניוזלטר
- שמור על תוכן תמציתי ומרתק

#### article-1.html עד article-4.html
- כל מאמר צריך להיות 3-4 פסקאות
- השתמש ב-`<div dir="rtl">` כעטיפה
- כתוב בעברית עם פורמט RTL נכון
- שמור על תוכן תמציתי אך אינפורמטיבי

### 3. יצירת data.js
```javascript
const fs = require("fs");

function buildJson(directoryName) {
  const introContent = fs.readFileSync(`./${directoryName}/intro.html`, "utf8");
  const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, "utf8");
  const article2Content = fs.readFileSync(`./${directoryName}/article-2.html`, "utf8");
  const article3Content = fs.readFileSync(`./${directoryName}/article-3.html`, "utf8");
  const article4Content = fs.readFileSync(`./${directoryName}/article-4.html`, "utf8");

  return {
    intro: {
      title: "כותרת המבוא שלך",
      content: introContent,
    },
    articles: [
      {
        title: "כותרת מאמר 1",
        content: article1Content,
        img: "URL_תמונה_1",
        url: "URL_לינקדאין_1",
      },
      {
        title: "כותרת מאמר 2", 
        content: article2Content,
        img: "URL_תמונה_2",
        url: "URL_לינקדאין_2",
      },
      {
        title: "כותרת מאמר 3",
        content: article3Content,
        img: "URL_תמונה_3", 
        url: "URL_לינקדאין_3",
      },
      {
        title: "כותרת מאמר 4",
        content: article4Content,
        img: "URL_תמונה_4",
        url: "URL_לינקדאין_4",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;
```

### 4. עדכון סקריפט הקומפילציה
ערוך את `compileNewsletter.js`:
```javascript
const newsletterFolder = "newsletter-XX"; // שנה את השורה הזו
```

### 5. קומפילציה של הניוזלטר
```bash
cd packages/html-emails/newsletter
node compileNewsletter.js
```

## הנחיות תוכן

### מבנה מאמר
- **כותרת**: 3-7 מילים, מרתקת
- **תוכן**: 3-4 פסקאות, עברית RTL
- **תמונה**: תמונה מלינקדאין או YouTube
- **URL**: כתובת הפוסט בלינקדאין

### סגנון כתיבה
- השתמש בעברית עם פורמט RTL נכון
- שמור על פסקאות קצרות (2-3 משפטים)
- צור תוכן מרתק ואינפורמטיבי
- כלול תובנות טכניות כשמתאים

### מידע נדרש לכל מאמר
1. **כותרת** (עברית)
2. **תוכן** (עברית, 3-4 פסקאות)
3. **URL תמונה** (תמונה מלינקדאין או YouTube)
4. **URL לינקדאין** (כתובת מלאה של הפוסט)

## מבנה קבצים
```
newsletter-XX/
├── intro.html
├── article-1.html
├── article-2.html
├── article-3.html
├── article-4.html
├── data.js
└── output.html (נוצר אוטומטית)
```

## הערות חשובות
- תמיד השתמש ב-`<div dir="rtl">` לתוכן עברי
- וודא שכל כתובות הלינקדאין מלאות ועובדות
- בדוק קומפילציה לפני סיום
- שמור על תוכן תמציתי אך בעל ערך
- שמור על פורמט עקבי בכל המאמרים

## דוגמה למבנה תוכן
### intro.html
```html
<div dir="rtl">
  <h2>כותרת המבוא</h2>
  <p>
    פסקה ראשונה - הסבר על נושא הניוזלטר
  </p>
  <p>
    פסקה שנייה - מה הקוראים ילמדו
  </p>
</div>
```

### article-X.html
```html
<div dir="rtl">
  <p>
    פסקה ראשונה - מבוא למאמר
  </p>
  <p>
    פסקה שנייה - תוכן עיקרי
  </p>
  <p>
    פסקה שלישית - סיכום או נקודה חשובה
  </p>
</div>
```
