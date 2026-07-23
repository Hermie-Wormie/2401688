import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE = "http://localhost:5000"

def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    return webdriver.Chrome(options=opts)

def test_home_has_form():
    d = make_driver()
    d.get(BASE)
    assert d.find_element(By.ID, "term")
    assert d.find_element(By.XPATH, "//button[@type='submit']")
    d.quit()

def test_valid_search_shows_result():
    d = make_driver()
    d.get(BASE)
    d.find_element(By.ID, "term").send_keys("hello world")
    d.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert "You searched for: hello world" in d.page_source
    d.find_element(By.XPATH, "//button[text()='Return to home']")
    d.quit()

def test_attack_input_stays_home_and_clears():
    d = make_driver()
    d.get(BASE)
    box = d.find_element(By.ID, "term")
    d.execute_script("document.getElementById('term').value = \"<script>alert(1)</script>\"")
    d.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert d.current_url.rstrip("/") == BASE          # still home
    assert d.find_element(By.ID, "term").get_attribute("value") == ""  # cleared
    d.quit()