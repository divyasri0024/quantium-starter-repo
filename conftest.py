import pytest
from selenium import webdriver

def pytest_setup_options():
    options = webdriver.ChromeOptions()
    # If you want to run tests in the background, uncomment the line below:
    # options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    return options