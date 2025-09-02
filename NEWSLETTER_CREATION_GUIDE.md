# מדריך יצירת ניוזלטר חדש

## סקירה כללית
יצירת ניוזלטר חדש עם 4 מאמרים ותוכן עברי, בעקבות אותו מבנה כמו newsletter-23.

## תהליך אוטומטי עם LinkedIn MCP

### שימוש ב-Claude Code עם LinkedIn MCP
כאשר משתמש מספק 4 לינקים ללינקדאין, Claude Code יבצע את התהליך הבא:

1. **חילוץ תוכן מלינקדאין**: שימוש ב-LinkedIn MCP לחילוץ טקסט, תמונות ולינקי YouTube
2. **יצירת תמציות**: המרת התוכן המחולץ ל-4 מאמרים בעברית
3. **יצירת מבנה הניוزלטר**: בניית כל הקבצים הנדרשים אוטומטית
4. **עדכון index.html**: הוספת הניוזלטר החדש לרשימת `availableNewsletters`
5. **קומפילציה והצגה**: הפעלת הסביבה עם live reload

### דוגמה לשימוש
```
משתמש: "צור ניוזלטר חדש עם 4 הלינקים הבאים:
1. https://www.linkedin.com/posts/...
2. https://www.linkedin.com/posts/...
3. https://www.linkedin.com/posts/...
4. https://www.linkedin.com/posts/..."
```

Claude Code יבצע:
- חילוץ תוכן מכל הלינקים
- יצירת newsletter-XX חדש
- כתיבת כל הקבצים (intro.html, article-1.html, etc.)
- **יצירת data.js** עם הנתונים המחולצים (כותרות, תמונות, URLs)
- **חשוב: אם נמצא לינק YouTube בפוסט, השתמש בו במקום לינק הלינקדאין**
- **קריאת תוכן הניוזלטר** לחילוץ כותרת ותיאור מדויקים
- עדכון index.html והוספת הניוזלטר החדש לרשימת `availableNewsletters`
- הפעלת `npm run dev` לתצוגה

## תהליך ידני שלב אחר שלב

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
**חשוב**: צור את קובץ `data.js` לפני הקומפילציה. השתמש ב-`newsletter-23/data.js` כדוגמה:

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
      title: "כותרת המבוא שלך", // חלץ מ-intro.html
      content: introContent,
    },
    articles: [
      {
        title: "כותרת מאמר 1", // חלץ מ-HTML comments או תוכן
        content: article1Content,
        img: "URL_תמונה_1", // תמונה מלינקדאין או YouTube
        url: "URL_לינקדאין_1", // לינק לפוסט או YouTube
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

**הערה**: אם הניוזלטר משתמש ב-`utils/genericData` (כמו newsletter-24), השתמש בזה במקום הקוד למעלה.

### 4. עדכון סקריפט הפיתוח
ערוך את `dev-server.js`:
```javascript
const newsletterFolder = "newsletter-XX"; // שנה את השורה הזו
```

### 5. עדכון index.html
עדכן את `index.html` והוסף את הניוזלטר החדש לרשימת `availableNewsletters`:

**חשוב**: קרא את תוכן הניוזלטר כדי לחלץ כותרת ותיאור מדויקים:

1. **קרא את `intro.html`** - חלץ את הכותרת מ-`<h2>` ואת התיאור מהפסקאות
2. **קרא את `article-1.html`** - בדוק את הכותרת ב-HTML comments (אם קיימים)
3. **הוסף לרשימה** עם הנתונים הנכונים:

```javascript
const availableNewsletters = [
    {
        folder: 'newsletter-23',
        title: 'AI Agents - מהמעבדה לשטח',
        description: 'השבוע אנחנו עוברים מהתיאוריה למעשה - איך AI Agents הופכים מכלי מעניין לכלי עבודה אמיתי'
    },
    {
        folder: 'newsletter-XX', // שנה ל-XX המתאים
        title: 'כותרת הניוזלטר החדש', // חלץ מ-intro.html
        description: 'תיאור קצר של הניוזלטר החדש' // חלץ מ-intro.html
    }
    // Add more newsletters here as they are created
];
```

**דוגמה לחילוץ נתונים**:
- **כותרת**: חלץ מ-`<h2>` ב-`intro.html`
- **תיאור**: חלץ מהפסקה הראשונה ב-`intro.html` או צור תמצית מהתוכן

### 6. הפעלת סביבת הפיתוח
**חשוב**: וודא שיצרת את `data.js` לפני הפעלת הסקריפט!

```bash
npm run dev
```

הסקריפט יבצע:
- קומפילציה ראשונית של הניוזלטר
- מעקב אחר שינויים בקבצים (auto-recompile)
- הפעלת live server ב-http://localhost:8080/output.html
- רענון אוטומטי של הדפדפן כשהקבצים משתנים

### 7. קומפילציה ידנית (אופציונלי)
אם נדרש רק לקמפל ללא live server:
```bash
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
- **חובה**: צור את `data.js` לפני הקומפילציה
- **חובה**: עדכן את `index.html` והוסף כל ניוזלטר חדש לרשימת `availableNewsletters`
- **חובה**: קרא את תוכן הניוזלטר (intro.html) כדי לחלץ כותרת ותיאור מדויקים
- השתמש ב-`npm run dev` לפיתוח עם live reload
- הדפדפן יפתח אוטומטית ב-http://localhost:8080/output.html
- שינויים בקבצים יגרמו לקומפילציה ורענון אוטומטי
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
