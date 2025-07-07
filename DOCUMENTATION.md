# תיעוד מלא - תשתית אוטומציה

## סקירה כללית

התשתית הזו היא פרויקט אוטומציה מינימלי המיועד להדגמה בראיון עבודה. היא מציגה הבנה של עקרונות בסיסיים בבדיקות אוטומטיות, כולל Page Object Model, API testing, וארגון קוד נכון.

---

## מבנה הפרויקט - הסבר מעמיק

```
automation-framework/
├── api/                    # תיקיית API clients
├── pages/                  # Page Object Model
├── tests/                  # קבצי בדיקה
├── utils/                  # כלים משותפים
├── config/                 # קבצי הגדרות
├── conftest.py            # Pytest fixtures
├── pytest.ini            # הגדרות Pytest
├── requirements.txt       # Dependencies
├── run_tests.bat         # הרצה Windows
├── run_tests.sh          # הרצה Linux/Mac
└── README.md             # תיעוד בסיסי
```

---

## 📁 api/ - תיקיית API Clients

### `api/__init__.py`
```python
# API package
```
**מטרה**: מגדיר את התיקייה כ-Python package כדי שנוכל לייבא ממנה.

### `api/search_client.py`
```python
"""
Simple API client for search functionality.
"""

import requests
from utils.config import get_api_base_url, get_timeout


class SearchClient:
    """Simple search API client."""
    
    def __init__(self):
        """Initialize the search client."""
        self.base_url = get_api_base_url()
        self.timeout = get_timeout()
    
    def get_posts(self):
        """Get all posts from the API."""
        url = "{}/posts".format(self.base_url)
        response = requests.get(url, timeout=self.timeout)
        return response
    
    def get_post_by_id(self, post_id):
        """Get a single post by ID."""
        url = "{}/posts/{}".format(self.base_url, post_id)
        response = requests.get(url, timeout=self.timeout)
        return response
    
    def search_users(self):
        """Get users from the API."""
        url = "{}/users".format(self.base_url)
        response = requests.get(url, timeout=self.timeout)
        return response
```

**מטרה**: מחלקה שמנהלת את כל הקשר עם ה-API. 

**עקרונות חשובים**:
- **Single Responsibility**: המחלקה רק מתקשרת עם API
- **Configuration**: משתמשת בהגדרות מרכזיות מ-config
- **Error Handling**: משתמשת ב-timeout למניעת תקיעות
- **Clear Methods**: כל method עושה דבר אחד ברור

**איך זה עובד**:
1. `__init__()` טוען את ההגדרות מ-config
2. כל method בונה URL ושולח בקשת HTTP
3. מחזיר את ה-response הגולמי (לא מעבד אותו)

---

## 📁 pages/ - Page Object Model

### `pages/__init__.py`
```python
# Pages package
```

### `pages/base_page.py`
```python
"""
Base page class for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import get_timeout


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        """Initialize the base page."""
        self.driver = driver
        self.wait = WebDriverWait(driver, get_timeout())
    
    def open(self, url):
        """Navigate to a specific URL."""
        self.driver.get(url)
    
    def get_title(self):
        """Get the current page title."""
        return self.driver.title
    
    def find_element(self, locator):
        """Find a single element with explicit wait."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise TimeoutException("Element not found: {}".format(locator))
    
    def click_element(self, locator):
        """Click an element with explicit wait."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into an input field."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from an element."""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
```

**מטרה**: מחלקת בסיס שמכילה פונקציות נפוצות לכל הדפים.

**עקרונות חשובים**:
- **DRY (Don't Repeat Yourself)**: כל הפונקציות הנפוצות במקום אחד
- **Explicit Waits**: משתמש ב-WebDriverWait במקום sleep() שחוסך זמן
- **Error Handling**: תופס TimeoutException ומספק הודעות שגיאה ברורות
- **Inheritance**: דפים אחרים יורשים ממנה

**איך זה עובד**:
1. `__init__()` מקבל driver ויוצר WebDriverWait
2. כל method משתמש בexplicit wait לפני פעולה
3. אם element לא נמצא, זורק exception עם הודעה ברורה

### `pages/home_page.py`
```python
"""
Home page object for Ynet website.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import get_base_url


class HomePage(BasePage):
    """Home page object for Ynet website."""
    
    # Page locators - פשוטים ואמינים
    LOGO = (By.CSS_SELECTOR, "img[alt*='ynet'], a[href*='ynet'], img[src*='logo']")
    MAIN_CONTENT = (By.TAG_NAME, "main")
    NEWS_ARTICLES = (By.CSS_SELECTOR, "article, .article, [class*='story'], [class*='news']")
    
    def __init__(self, driver):
        """Initialize the HomePage."""
        super(HomePage, self).__init__(driver)
        self.base_url = get_base_url()
    
    def load(self):
        """Navigate to the homepage."""
        self.open(self.base_url)
    
    def is_logo_displayed(self):
        """Check if the header logo is displayed."""
        return self.is_element_visible(self.LOGO)
    
    def get_main_headline(self):
        """Get the main headline text."""
        try:
            # חיפוש כותרת ראשית
            headline_selectors = ["h1", "h2", ".headline", "[class*='title']"]
            for selector in headline_selectors:
                try:
                    element = self.find_element((By.CSS_SELECTOR, selector))
                    text = element.text.strip()
                    if text:
                        return text
                except:
                    continue
            return ""
        except:
            return ""
    
    def get_article_count(self):
        """Get the number of news articles on the page."""
        try:
            articles = self.driver.find_elements(*self.NEWS_ARTICLES)
            return len(articles)
        except:
            return 0
    
    def verify_page_loaded(self):
        """Verify that the homepage has loaded correctly."""
        # בדיקה פשוטה - שהכותרת מכילה ynet והדף נטען
        try:
            title_ok = "ynet" in self.get_title().lower()
            page_ready = self.driver.execute_script("return document.readyState") == "complete"
            body_exists = len(self.driver.find_elements(By.TAG_NAME, "body")) > 0
            return title_ok and page_ready and body_exists
        except:
            return False
```

**מטרה**: מימוש של Page Object לדף הבית של Ynet.

**עקרונות חשובים**:
- **Page Object Model**: הפרדה בין locators לבין לוגיקת הבדיקה
- **Robust Locators**: locators שעובדים גם אם האתר משתנה קצת
- **Inheritance**: יורש מ-BasePage ומשתמש בפונקציות שלה
- **Defensive Programming**: כל method מטפל בשגיאות אפשריות

**איך זה עובד**:
1. **Locators**: מוגדרים כ-constants בראש המחלקה
2. **load()**: פותח את האתר
3. **verify_page_loaded()**: בודק 3 דברים - title, readyState, ו-body קיים
4. **Robust Design**: אם locator אחד לא עובד, מנסה אחרים

---

## 📁 tests/ - קבצי בדיקה

### `tests/test_ui.py`
```python
"""
Basic UI test for homepage.
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_homepage_loads(driver):
    """Test that the homepage loads successfully."""
    # Create homepage object
    homepage = HomePage(driver)
    
    # Load the page
    homepage.load()
    
    # Verify page loaded
    assert homepage.verify_page_loaded(), "Homepage should load successfully"
    
    # Verify title contains ynet
    title = homepage.get_title()
    assert "ynet" in title.lower(), "Page title should contain 'ynet'"
```

**מטרה**: בדיקת UI בסיסית שבודקת שהדף נטען.

**עקרונות חשובים**:
- **Markers**: `@pytest.mark.ui` ו-`@pytest.mark.smoke` לסינון בדיקות
- **Page Object Usage**: משתמש ב-HomePage במקום selenium ישיר
- **Clear Assertions**: assertions עם הודעות ברורות
- **Single Responsibility**: בדיקה אחת עושה דבר אחד

### `tests/test_api.py`
```python
"""
Basic API test for search functionality.
"""

import pytest
from api.search_client import SearchClient


@pytest.mark.api
@pytest.mark.smoke
def test_get_posts():
    """Test that we can get posts from the API."""
    # Create search client
    client = SearchClient()
    
    # Get posts
    response = client.get_posts()
    
    # Verify response
    assert response.status_code == 200, "API should return 200 status"
    
    # Verify response has data
    posts = response.json()
    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) > 0, "Should return some posts"


@pytest.mark.api
def test_get_single_post():
    """Test that we can get a single post by ID."""
    # Create search client
    client = SearchClient()
    
    # Get specific post
    response = client.get_post_by_id(1)
    
    # Verify response
    assert response.status_code == 200, "API should return 200 status"
    
    # Verify post data
    post = response.json()
    assert post["id"] == 1, "Post ID should match requested ID"
    assert "title" in post, "Post should have a title"
    assert "body" in post, "Post should have a body"
```

**מטרה**: בדיקות API שבודקות ש-JSONPlaceholder עובד.

**עקרונות חשובים**:
- **API Testing**: בדיקת status codes, response structure, data validation
- **Multiple Assertions**: כל בדיקה בודקת כמה דברים
- **Real API**: משתמש ב-API אמיתי (JSONPlaceholder)
- **Markers**: לסינון בדיקות

---

## 📁 utils/ - כלים משותפים

### `utils/__init__.py`
```python
# Utils package
```

### `utils/config.py`
```python
"""
Simple configuration loader.
"""

import json
import os


def load_config(config_path="config/config.json"):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        raise Exception("Configuration file not found: {}".format(config_path))
    
    with open(config_path, 'r') as file:
        return json.load(file)


def get_base_url():
    """Get the base URL for UI tests."""
    config = load_config()
    return config.get("base_url", "https://www.ynet.co.il")


def get_api_base_url():
    """Get the base URL for API tests.""" 
    config = load_config()
    return config.get("api_base_url", "https://jsonplaceholder.typicode.com")


def get_browser():
    """Get the browser type."""
    config = load_config()
    return config.get("browser", "chrome")


def get_timeout():
    """Get the timeout value."""
    config = load_config()
    return config.get("timeout", 10)


def is_headless():
    """Check if browser should run in headless mode."""
    config = load_config()
    return config.get("headless", False)
```

**מטרה**: ניהול הגדרות מרכזי.

**עקרונות חשובים**:
- **Centralized Config**: כל ההגדרות במקום אחד
- **Default Values**: אם משהו חסר בconfig, יש default
- **Error Handling**: בודק שהקובץ קיים
- **Simple Functions**: כל function עושה דבר אחד

---

## 📁 config/ - הגדרות

### `config/config.json`
```json
{
  "base_url": "https://www.ynet.co.il",
  "api_base_url": "https://jsonplaceholder.typicode.com",
  "browser": "chrome",
  "headless": false,
  "timeout": 10,
  "environment": "demo"
}
```

**מטרה**: קובץ הגדרות שקל לשנות בלי לגעת בקוד.

**יתרונות**:
- **Flexibility**: אפשר לשנות URLs בלי לשנות קוד
- **Environment Support**: אפשר להוסיף environments
- **Easy Maintenance**: כל ההגדרות במקום אחד

---

## ⚙️ קבצי תצורה

### `conftest.py`
```python
"""
Pytest configuration and fixtures.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import get_timeout, is_headless


@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture that provides a clean browser instance for each test."""
    # Setup Chrome options
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    if is_headless():
        options.add_argument("--headless")
    
    # Create driver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(get_timeout())
    
    yield driver
    
    # Cleanup
    driver.quit()
```

**מטרה**: Pytest fixture שמספק WebDriver לכל בדיקה.

**עקרונות חשובים**:
- **Fixture Scope**: `function` אומר driver חדש לכל בדיקה
- **Automatic Cleanup**: `yield` מבטיח ש-`driver.quit()` יקרה תמיד
- **WebDriver Manager**: אוטומטית מוריד ChromeDriver הנכון
- **Configuration**: משתמש בהגדרות מ-config

### `pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    ui: UI tests using Selenium
    api: API tests using requests
    smoke: Basic functionality tests

addopts = -v --tb=short
```

**מטרה**: הגדרות Pytest.

**חשיבות**:
- **Test Discovery**: איפה למצוא בדיקות
- **Markers**: מגדיר markers כדי שלא יהיו warnings
- **Output**: `-v` לפלט מפורט, `--tb=short` לשגיאות קצרות

---

## 🚀 קבצי הרצה

### `run_tests.bat` (Windows)
```batch
@echo off
echo Running Automation Tests...
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Running UI Tests...
pytest tests/test_ui.py -m ui -v
echo.

echo Running API Tests...
pytest tests/test_api.py -m api -v
echo.

echo Running All Tests with HTML Report...
pytest tests/ --html=reports/test_report.html --self-contained-html -v
echo.

echo Tests completed! Check reports/test_report.html for results.
pause
```

### `run_tests.sh` (Linux/Mac)
```bash
#!/bin/bash
echo "Running Automation Tests..."
echo

echo "Installing dependencies..."
pip install -r requirements.txt
echo

echo "Running UI Tests..."
pytest tests/test_ui.py -m ui -v
echo

echo "Running API Tests..."
pytest tests/test_api.py -m api -v
echo

echo "Running All Tests with HTML Report..."
pytest tests/ --html=reports/test_report.html --self-contained-html -v
echo

echo "Tests completed! Check reports/test_report.html for results."
```

**מטרה**: הרצת הבדיקות בצורה אוטומטית.

**מה הם עושים**:
1. מתקינים dependencies
2. מריצים UI tests בנפרד
3. מריצים API tests בנפרד  
4. מריצים הכל עם HTML report

---

## 📋 Dependencies

### `requirements.txt`
```
pytest==8.4.1
selenium==4.34.0
webdriver-manager==4.0.2
requests==2.32.4
pytest-html==4.1.1
```

**הסבר על כל dependency**:
- **pytest**: Framework לבדיקות
- **selenium**: אוטומציה של דפדפן
- **webdriver-manager**: ניהול אוטומטי של ChromeDriver
- **requests**: HTTP requests ל-API testing
- **pytest-html**: יצירת HTML reports

---

## 🎯 עקרונות עיצוב מתקדמים

### 1. Page Object Model
```
✅ Separation of Concerns: locators נפרדים מלוגיקת בדיקה
✅ Reusability: אפשר להשתמש ב-HomePage בבדיקות רבות
✅ Maintainability: אם האתר משתנה, משנים רק ב-HomePage
```

### 2. Single Responsibility Principle
```
✅ SearchClient: רק API communication
✅ HomePage: רק פעולות על דף הבית
✅ BasePage: רק פונקציות selenium בסיסיות
```

### 3. Configuration Management
```
✅ Centralized: כל ההגדרות ב-config.json
✅ Flexible: קל לשנות environment
✅ Default Values: הקוד עובד גם בלי config מושלם
```

### 4. Error Handling
```
✅ Graceful Failures: אם element לא נמצא, מחזיר False במקום לקרוס
✅ Clear Messages: assertions עם הודעות מובנות
✅ Timeouts: מניעת תקיעות עם WebDriverWait
```

### 5. Test Organization
```
✅ Markers: ui/api/smoke לסינון בדיקות
✅ Fixtures: driver fixture מספק setup/cleanup אוטומטי
✅ Reports: HTML reports עם מידע מפורט
```

---

## 🏃‍♂️ איך להריץ

### התקנה ראשונית
```bash
# Clone הפרויקט
git clone <repository>
cd automation-framework

# יצירת virtual environment (מומלץ)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# התקנת dependencies
pip install -r requirements.txt
```

### הרצת בדיקות
```bash
# כל הבדיקות
pytest tests/ -v

# רק UI
pytest tests/test_ui.py -m ui -v

# רק API
pytest tests/test_api.py -m api -v

# רק smoke tests
pytest tests/ -m smoke -v

# עם HTML report
pytest tests/ --html=reports/test_report.html --self-contained-html -v
```

### שימוש בקבצי הרצה
```bash
# Windows
run_tests.bat

# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh
```

---

## 🎓 נקודות חשובות לראיון

### 1. למה Page Object Model?
**תשובה**: 
- הפרדה בין UI elements לבין לוגיקת בדיקה
- אם האתר משתנה, משנים רק ב-Page Object
- קוד יותר קריא ולא חוזר על עצמו

### 2. למה לא להשתמש ב-sleep()?
**תשובה**:
- WebDriverWait יותר מהיר - מחכה רק עד שהelement מוכן
- יותר יציב - לא תלוי במהירות המחשב
- פחות flaky tests

### 3. איך מטפלים בשגיאות?
**תשובה**:
- TimeoutException עם הודעות ברורות
- try/except blocks במקומות הנכונים
- Default values בconfig

### 4. איך מוודאים שהבדיקות עצמאיות?
**תשובה**:
- כל בדיקה מקבלת driver חדש
- אין שיתוף מידע בין בדיקות
- cleanup אוטומטי עם fixtures

### 5. איך הקוד ניתן לתחזוקה?
**תשובה**:
- Configuration מרכזי
- Clear naming conventions
- Documentation בעברית ובאנגלית
- מבנה תיקיות הגיוני

---

## 🔍 דוגמאות הרצה

### בדיקות עוברות בהצלחה:
```
========================================= test session starts ==========================================
collected 3 items                                                                                       

tests/test_api.py::test_get_posts PASSED                                                          [ 33%]
tests/test_api.py::test_get_single_post PASSED                                                    [ 66%]
tests/test_ui.py::test_homepage_loads PASSED                                                      [100%]

========================================== 3 passed in 11.06s ==========================================
```

### HTML Report נוצר ב:
```
reports/test_report.html
```

**התשתית הזו מוכנה להצגה מקצועית בראיון!** 🎯 