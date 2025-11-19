from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

PROXY = "mitmproxy:8080"

def start_sandbox():
    print("--- Initializing Secure Sandbox ---")
    
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        options=chrome_options
    )
    
    print("\n>>> Sandbox Ready!")
    print("1. Visual View: http://localhost:7900 (Password: secret)")
    print("2. Network Log: http://localhost:8081")
    print("-" * 30)

    try:
        while True:
            url = input("\nEnter a website to test (or type 'exit' to quit): ")
            
            if url.lower() == 'exit':
                break
            
            if not url.startswith("http"):
                url = "https://" + url
                
            print(f"Visiting: {url} ...")
            driver.get(url)
            print("Done! Check the logs.")

    finally:
        driver.quit()
        print("--- Sandbox Destroyed & Reset ---")

if __name__ == "__main__":
    start_sandbox()