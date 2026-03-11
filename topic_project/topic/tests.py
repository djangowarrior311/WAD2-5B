# Using the templates from "https://github.com/tangowithcode/tango_with_django_2_code/blob/master/progress_tests/"


import os
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

print("INITIALISING DRIVER...")
driver = webdriver.Firefox() # type: ignore
driver.get("http://127.0.0.1:8000/")

def test_close_announcements():
    close_button = driver.find_element(by=By.CSS_SELECTOR, value="#announcements button")
    close_button.click()

    announcements = driver.find_element(by=By.ID, value="announcements")
    assert not announcements.is_displayed, "announcements couldn't be closed!"

def 