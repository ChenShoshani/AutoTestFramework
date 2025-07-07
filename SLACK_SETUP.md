# 🔔 מדריך הגדרת Slack Notifications

מדריך זה מסביר איך להגדיר התראות Slack אוטומטיות עבור הפרויקט.

## 🎯 מה נדרש

1. **Slack Workspace** - גישה לSlack workspace
2. **GitHub Repository** - הפרויקט צריך להיות בGitHub
3. **הרשאות Admin** - כדי להוסיף Incoming Webhooks

---

## 📋 שלב 1: יצירת Slack Webhook

### 1.1 פתיחת Slack App Directory
1. עבור לSlack workspace שלך
2. לחץ על הגלגל שיניים (Settings) ← **Browse Apps**
3. או עבור ישירות ל: `https://[YOUR-WORKSPACE].slack.com/apps`

### 1.2 חיפוש Incoming Webhooks
1. בחיפוש הכתב: **"Incoming Webhooks"**
2. לחץ על **"Incoming Webhooks"** מהתוצאות
3. לחץ על **"Add to Slack"**

### 1.3 הגדרת הערוצים
תצטרך ליצור שני webhooks נפרדים:

#### Webhook #1: Sanity Tests
1. לחץ על **"Add Incoming Webhook integration"**
2. בחר ערוץ: **`#sanity`** (אם הערוץ לא קיים, צור אותו)
3. לחץ על **"Add Incoming Webhook integration"**
4. **העתק את ה-Webhook URL** - שמור אותו!

#### Webhook #2: Nightly Tests  
1. חזור לעמוד Incoming Webhooks
2. לחץ על **"Add Configuration"**
3. בחר ערוץ: **`#nightly`** (אם הערוץ לא קיים, צור אותו)
4. לחץ על **"Add Incoming Webhook integration"**
5. **העתק את ה-Webhook URL** - שמור אותו!

### 1.4 דוגמה לWebhook URL
הURL צריך להיראות כך:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 🔐 שלב 2: הוספת Secrets לGitHub

### 2.1 פתיחת הגדרות Repository
1. עבור לGitHub repository שלך
2. לחץ על **Settings** (למעלה בתפריט)
3. בתפריט השמאלי, לחץ על **"Secrets and variables"**
4. לחץ על **"Actions"**

### 2.2 הוספת Slack Webhook
1. לחץ על **"New repository secret"**
2. בשדה **Name** הכתב: `SLACK_WEBHOOK_URL`
3. בשדה **Secret** הדבק את ה-Webhook URL שהעתקת
4. לחץ על **"Add secret"**

### 2.3 וידוא שהSecret נוסף
אמור לראות ברשימה:
- ✅ `SLACK_WEBHOOK_URL` (Updated X seconds ago)

---

## 🧪 שלב 3: בדיקת הגדרות

### 3.1 בדיקה מהירה של Webhook
תוכל לבדוק אם הWebhook עובד עם curl:

```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"🧪 Test message from YitAutomationTest", "channel":"#sanity"}' \
YOUR_WEBHOOK_URL
```

### 3.2 הרצת GitHub Actions
1. עבור לGitHub repository
2. לחץ על **Actions**
3. בחר **"Tests"** workflow
4. לחץ על **"Run workflow"**
5. לחץ על **"Run workflow"** (כפתור ירוק)

### 3.3 בדיקת התראות
לאחר הרצת הworkflow:
1. בדוק את הערוץ `#sanity` בSlack
2. אמורה להופיע התראה עם תוצאות הבדיקה
3. אם הבדיקה נכשלה, התראה תישלח גם ל`#nightly`

---

## 📊 שלב 4: הבנת ההתראות

### 4.1 התראות Sanity (ערוץ #sanity)
- **מתי**: כל push למain או PR
- **מה**: תוצאות בדיקות sanity
- **סוג**: Success ✅ או Failure ❌

### 4.2 התראות Nightly (ערוץ #nightly)
- **מתי**: כל לילה ב-02:00 UTC
- **מה**: תוצאות כל הבדיקות
- **סוג**: Success ✅ או Failure ❌

### 4.3 מידע שנשלח בהתראה
- שם הrepository
- שם הbranch
- מספר commit
- שם המשתמש שגרם לריצה
- קישור לworkflow run
- קישור להורדת דוח

---

## 🛠️ שלב 5: התאמות אישיות

### 5.1 שינוי ערוצים
אם תרצה לשנות ערוצים, ערוך את `.github/workflows/tests.yml`:

```yaml
# לשינוי ערוץ sanity
channel: '#your-sanity-channel'

# לשינוי ערוץ nightly  
channel: '#your-nightly-channel'
```

### 5.2 שינוי מבנה ההתראות
תוכל לערוך את הטקסט בקובץ `tests.yml`:

```yaml
text: |
  ✅ *Your Custom Message*
  
  📊 *Details:*
  • Custom field: value
```

### 5.3 הוספת מידע נוסף
אפשר להוסיף fields נוספים:

```yaml
text: |
  ✅ *Tests Status*
  
  📊 *Details:*
  • Environment: Production
  • Duration: ${{ steps.test.outputs.duration }}
  • Coverage: ${{ steps.test.outputs.coverage }}
```

---

## 🚨 פתרון בעיות נפוצות

### בעיה 1: "Secret not found"
**סיבה**: הSecret לא הוגדר נכון בGitHub
**פתרון**: 
1. ודא שהשם הוא בדיוק `SLACK_WEBHOOK_URL`
2. ודא שהSecret הוגדר בrepository הנכון
3. ודא שהWebhook URL תקין

### בעיה 2: "Channel not found"
**סיבה**: הערוץ לא קיים בSlack
**פתרון**:
1. צור את הערוצים `#sanity` ו-`#nightly`
2. או שנה את שמות הערוצים בworkflow

### בעיה 3: "Webhook not authorized"
**סיבה**: הWebhook לא מוסמך
**פתרון**:
1. ודא שהWebhook נוצר נכון בSlack
2. ודא שהURL הועתק במלואו
3. בדוק שהWorkspace נכון

### בעיה 4: "No notifications"
**סיבה**: הWorkflow לא רץ
**פתרון**:
1. בדוק ש-push התבצע למain branch
2. בדוק שהworkflow קיים ב-`.github/workflows/`
3. בדוק logs בGitHub Actions

---

## 📱 דוגמאות התראות

### התראה מוצלחת
```
✅ Sanity Tests PASSED

📊 Details:
• Repository: username/YitAutomationTest
• Branch: main
• Commit: abc123
• Author: username

🔗 Links:
• View Workflow Run
• Download Report

🎉 Great job! All systems are healthy.
```

### התראה כושלת
```
❌ Sanity Tests FAILED

📊 Details:
• Repository: username/YitAutomationTest
• Branch: main
• Commit: abc123
• Author: username

🔗 Links:
• View Workflow Run
• Download Report

⚠️ Action Required: Please check the test failures immediately.
```

---

## 🔄 שלב 6: אימות הגדרות

### 6.1 Checklist הגדרות
- [ ] Slack webhook נוצר
- [ ] ערוצים `#sanity` ו-`#nightly` קיימים
- [ ] GitHub Secret `SLACK_WEBHOOK_URL` הוגדר
- [ ] Workflow קיים ב-`.github/workflows/tests.yml`
- [ ] Push לmain מפעיל את הworkflow

### 6.2 בדיקה מלאה
1. בצע שינוי קטן בקוד
2. Push למain
3. בדוק שהworkflow רץ בGitHub Actions
4. בדוק שהתראה הגיעה לSlack

---

## 📞 עזרה נוספת

אם יש בעיות:
1. בדוק את הלוגים בGitHub Actions
2. ודא שכל הערוצים קיימים בSlack
3. בדוק שהWebhook URL נכון
4. נסה לשלוח הודעה ידנית לWebhook

**🎯 הגדרת Slack הושלמה בהצלחה!** 