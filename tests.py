# Using the templates from "https://github.com/tangowithcode/tango_with_django_2_code/blob/master/progress_tests/"


import os
from django.test.utils import setup_test_environment, setup_databases, teardown_databases, teardown_test_environment
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

from typing import Callable
from test_config import *


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

# Source - https://stackoverflow.com/a/77159763
# Posted by Rafael C.
# Retrieved 2026-03-11, License - CC BY-SA 4.0

def visit_url(driver, url):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.common.exceptions import TimeoutException

    driver.get(f"http://{url}")

    try:
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
    except TimeoutException as err:
        raise TimeoutError("Page not loaded") from err

    # driver.save_screenshot(f"data/screenshots/{url}.png")


def test_close_announcements():
    driver.get("http://127.0.0.1:8000/")
    close_button = driver.find_element(by=By.CSS_SELECTOR, value="#announcements button")
    close_button.click()

    announcements = driver.find_element(by=By.ID, value="announcements")
    driver.implicitly_wait(0.1)
    assert announcements.value_of_css_property("display") == "none", "announcements couldn't be closed!"


def test_register_accessible():
    driver.get("http://127.0.0.1:8000/")
    # we shouldn't be logged in right now...
    register = driver.find_elements(by=By.CSS_SELECTOR, value="#topbar a")[1]
    register.click()


def test_password_special_characters():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("neon_Highlighter123")
    confirm_password.send_keys("neon_Highlighter123")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#req-special")
    driver.implicitly_wait(0.5)

    assert submit.get_attribute("class") != "valid", "Password should fail special character test"


def test_password_length():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("Ab1@")
    confirm_password.send_keys("Ab1@")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#req-length")
    driver.implicitly_wait(0.5)

    assert submit.get_attribute("class") != "valid", "Password should fail length check"


def test_password_upper_casing():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("ALL_UPPER_CASE@1")
    confirm_password.send_keys("ALL_UPPER_CASE@1")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#req-uppercase")
    driver.implicitly_wait(0.5)

    assert not submit.get_attribute("class") != "valid", "Password should fail upper casing check"


def test_password_lower_casing():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("all_lower_caseE@1")
    confirm_password.send_keys("all_lower_case@1")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#req-lowercase")
    driver.implicitly_wait(0.5)

    assert not submit.get_attribute("class") != "valid", "Password should fail upper casing check"


def test_password_match():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("goodPassword9123buta##NoMatch@!.")
    confirm_password.send_keys("goodPassword23buta##NoMatch@!.")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#password-match")
    driver.implicitly_wait(0.5)

    assert submit.get_text() != "✓ Passwords match", "Password should fail matching check"


def test_password_numbers():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("nONumBerz__@")
    confirm_password.send_keys("nONumBerz__@")

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#req-number")
    driver.implicitly_wait(0.5)

    assert not submit.get_attribute("class") != "valid", "Password should fail numbers check"


def test_password_pass():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p input")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    # should fail
    username.send_keys("new_username123")
    email.send_keys("anongus@topic.com")
    password.send_keys("goodPassword9123anda##Match@!.")
    confirm_password.send_keys("goodPassword9123anda##Match@!.")

    strength = driver.find_element(by=By.CSS_SELECTOR, value="#password-strong")
    match = driver.find_element(by=By.CSS_SELECTOR, value="#password-match")
    # driver.implicitly_wait(1)

    assert strength.get_attribute("class") == "strength-strong", "Password should be strong"
    assert match.get_text == "✓ Passwords match", "Password should match"



def run_tests(tests: Callable[[None], None]):
    print("RUNNING TESTS:")
    summary = []
    for test in tests:
        passed = True
        try:
            test()
        except BaseException as e:
            print(FAILURE_HEADER)
            passed = False
            print(e)
            print(FAILURE_FOOTER)
        summary.append((test.__name__, passed))
        print(f"{test.__name__} passed: {passed}")

    # print summary
    print("SUMMARY:")
    for (name, passed) in summary:
        print(f"{name} passed: {passed}")


if __name__ == "__main__":
    print("INITIALISING DRIVER...")
    driver = webdriver.Firefox() # type: ignore
    driver.get("http://127.0.0.1:8000/")

    tests = [
        test_close_announcements,
        test_register_accessible,
        test_password_length,
        test_password_lower_casing,
        test_password_upper_casing,
        test_password_special_characters,
        test_password_match,
        test_password_pass
    ]
    run_tests(tests)
    print("CLEANING UP")
    driver.quit()


