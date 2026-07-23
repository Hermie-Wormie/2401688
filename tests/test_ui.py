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
    # strip declarative HTML5 checks to exercise the JS validation layer
    d.execute_script("""
        const t = document.getElementById('term');
        t.removeAttribute('pattern');
        t.removeAttribute('minlength');
        t.value = "<script>alert(1)</scr" + "ipt>";
    """)
    d.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert d.current_url.rstrip("/") == BASE                            # still home
    assert d.find_element(By.ID, "term").get_attribute("value") == ""   # JS cleared it
    d.quit()

def test_html5_pattern_blocks_submit():
    d = make_driver()
    d.get(BASE)
    d.find_element(By.ID, "term").send_keys("<script>")
    d.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert d.current_url.rstrip("/") == BASE   # constraint validation stopped the form
    d.quit()