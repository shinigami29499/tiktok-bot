from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


options = ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.tiktok.com/")

input("Press any key to close.")
