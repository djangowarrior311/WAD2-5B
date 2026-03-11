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

    driver.save_screenshot(f"data/screenshots/{url}.png")


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


def test_register():
    test_register_accessible()
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="form p label")
    [
        username,
        email,
        password,
        confirm_password
    ] = inputs

    username.send_keys("Skrubunger")
    username.send_email()

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#submit-btn")
    submit.click()


def pre_test():
    assert EMAIL != "", "Fill out the email in test_config.py"
    assert USERNAME != "", "Fill out the username in test_config.py"
    assert PASSWORD != "", "Fill out the password in test_config.py"


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
    pre_test()

    print("INITIALISING DRIVER...")
    driver = webdriver.Firefox() # type: ignore
    driver.get("http://127.0.0.1:8000/")

    tests = [
        test_close_announcements,
        test_register_accessible,
        test_register
    ]
    run_tests(tests)
    print("CLEANING UP")
    driver.quit()


