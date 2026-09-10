from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

image_id = "2d484387-2509-5e8e-2c43-22f9981972eb"

url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

driver = webdriver.Chrome()

driver.get("https://www.artic.edu/")

print("Waiting on Art Institute homepage...")
time.sleep(10)

print("Opening image...")
driver.get(url)

time.sleep(5)

print("Current URL:", driver.current_url)
print("Page title:", driver.title)

try:
    image = WebDriverWait(driver, 20).until(
        lambda d: (
            d.find_element(By.TAG_NAME, "img")
            if d.execute_script(
                """
                return document.images.length > 0 &&
                       document.images[0].complete &&
                       document.images[0].naturalWidth > 0;
                """
            )
            else False
        )
    )

    print("Image loaded!")
    print("src:", image.get_attribute("src"))

    print(
        "natural width:",
        driver.execute_script(
            "return arguments[0].naturalWidth;",
            image
        )
    )

    print(
        "natural height:",
        driver.execute_script(
            "return arguments[0].naturalHeight;",
            image
        )
    )

    driver.save_screenshot("whole_page.png")

except Exception as e:
    print("Image did not load.")
    print(e)

input("Press Enter to close Chrome...")

driver.quit()