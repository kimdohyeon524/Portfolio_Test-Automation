from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time, os, sys

APPIUM_URL = os.getenv('APPIUM_URL', 'http://127.0.0.1:4723')

# Appium 세션 생성
def make_driver():
    caps = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'R3CWCO5LYZP',
        'appPackage': 'com.saucelabs.mydemoapp.android',
        'appActivity': 'com.saucelabs.mydemoapp.android.view.activities.SplashActivity',
        'autoGrantPermissions': True,
        'newCommandTimeout': 180,
        'noReset': True
    }
    options = UiAutomator2Options().load_capabilities(caps)
    return webdriver.Remote(APPIUM_URL, options=options)

# UI 요소가 보일 때까지 대기
def wait_exposed(driver, by, value, t=10):
    return WebDriverWait(driver, t).until(EC.visibility_of_element_located((by, value)))

# UI 요소 확인 후 클릭
def click(driver, by, value, t=10):
    wait_exposed(driver, by, value, t).click()

# UI 요소 확인 후 clear 한 뒤 입력
def type_text(driver, by, value, text, t=10):
    el = wait_exposed(driver, by, value, t)
    el.clear()
    el.send_keys(text)

# 특정 UI가 보일 때까지 스크롤
def scroll_to_target_ui(driver, target_ui: str, timeout: int = 15, max_swipes: int = 20):
    locator = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).setAsVerticalList()'f'.setMaxSearchSwipes({max_swipes}).scrollIntoView({target_ui})')
    return wait_exposed(driver, *locator, timeout)


# 스크린샷 저장 후 경로 반환
def screenshot(driver, name):
    path = os.path.abspath(name)
    driver.get_screenshot_as_file(path)
    print(f'[screenshot] {path}')

# 테스트 케이스

# 로그인 성공
def test_login_success(driver):
    print('[step] open login screen')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Login Menu Item')

    print('[step] input id/password & log in')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/nameET', 'bod@example.com')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/passwordET', '10203040')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to login with given credentials')

    print('[step] assert success banner')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    wait_exposed(driver, AppiumBy.ACCESSIBILITY_ID, 'Logout Menu Item', 10)
    print('[ok] login success')

# 로그아웃
def test_logout(driver):
    print('[step] try logout')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Logout Menu Item')

    print('[step] log out confirm')
    click(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/button1")')

    print('[step] assert log out')
    wait_exposed(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to login with given credentials', 10)
    print('[ok] log out test success')

# 로그인 실패 : 아이디 미입력
def test_login_failure_no_username(driver):
    print('[step] open login screen')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Login Menu Item')

    print('[step] input id/password & log in')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/passwordET', '10203040')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to login with given credentials')

    print('[step] assert error message')
    wait_exposed(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/nameErrorTV").textContains("required")', 10)
    print('[ok] no username test success')

# 로그인 실패 : 비밀번호 미입력
def test_login_failure_no_pass(driver):
    print('[step] open login screen')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Login Menu Item')

    print('[step] input id/password & log in')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/nameET', 'fail@example.com')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to login with given credentials')

    print('[step] assert error message')
    wait_exposed(driver, AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/passwordErrorTV").textContains("Enter")', 10)
    print('[ok] no pass test success')

# 로그인 실패 : 잠긴 계정
def test_login_failure_locked_out(driver):
    print('[step] open login screen')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Login Menu Item')

    print('[step] input id/password & log in')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/nameET', 'alice@example.com')
    type_text(driver, AppiumBy.ID, 'com.saucelabs.mydemoapp.android:id/passwordET', '10203040')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to login with given credentials')

    print('[step] assert error message')
    wait_exposed(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/passwordErrorTV").textContains("locked")', 10)
    print('[ok] locked out test success')

# 장바구니에 아이템 추가
def test_add_item_to_cart(driver):
    print('[step] open catalog')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'View menu')
    click(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Catalog")')

    print('[step] add first item to cart')
    click(driver, AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(0)')
    scroll_to_target_ui(driver,'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartBt")')
    click(driver, AppiumBy.ACCESSIBILITY_ID, 'Tap to add product to cart')

    print('[step] open cart & assert count')
    click(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartIV")')
    badge = wait_exposed(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/cartTV")', 10)
    assert badge.text.strip() in ('1', '1 item'), f'cart badge text error : {badge.text}'
    print('[ok] add to cart')

# 각 테스트 실행/에러 처리 코드
def run_test(name, func, driver):
    try:
        func(driver)
        print(f'[PASS] {name}')
    except Exception as e:
        print(f'[Error : {func.__name__} failed] \n{e}')
        try:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            screenshot(driver, f'{func.__name__}_failed_{timestamp}.png')
        except Exception as se:
            print(f'[warn] screenshot error: \n{se}')

def main():
    driver = None
    try:
        print('[info] create driver session')
        driver = make_driver()
        time.sleep(2)

        run_test('test_login_success', test_login_success, driver)
        run_test('test_logout', test_logout, driver)
        run_test('test_login_failure_no_username', test_login_failure_no_username, driver)
        run_test('test_login_failure_no_pass', test_login_failure_no_pass, driver)
        run_test('test_login_failure_locked_out', test_login_failure_locked_out, driver)
        run_test('test_add_item_to_cart', test_add_item_to_cart, driver)

        print('\n=== TEST END ===')
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
