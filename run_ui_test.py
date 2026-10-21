import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def execute_browser_automation_audit():
    print("[System] Booting up automated Google Chrome engine...")
    options = webdriver.ChromeOptions()
    
    # Modern Selenium automatically sets up Chrome driver paths natively!
    driver = webdriver.Chrome(options=options)
    
    try:
        print("[System] Navigating to login dashboard panel...")
        driver.get("http://127.0.0")
        driver.maximize_window()
        time.sleep(2)
        
        print("[System] Simulating human typing inputs...")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        # Make sure these credentials match your createsuperuser details
        username_field.send_keys("testdev") 
        password_field.send_keys("SecurePassword123") 
        time.sleep(1)
        
        print("[System] Executing click event handshake...")
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        time.sleep(3)
        
        assert "Site administration" in driver.page_source or "Django administration" in driver.page_source
        print("[SUCCESS] Selenium automated testing passed: Dashboard administration cleared!")
        
    except Exception as error:
        print(f"[FAIL] Selenium UI run error caught: {error}")
        
    finally:
        print("[System] Shutting down testing browser frame.")
        driver.quit()

if __name__ == "__main__":
    execute_browser_automation_audit()
