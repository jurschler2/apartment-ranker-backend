import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# run selenium headless
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
options = webdriver.ChromeOptions()
options.binary_location = chrome_bin
options.add_argument("—-disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=options)


def get_apartment(url):
    """ Get an apartment from craigslist with the url """

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    output = {}

    try:
        apartment_pics_raw = driver.find_elements_by_tag_name('img') or ""
        apartment_price = driver.find_element_by_class_name('price').text or ""
        apartment_address = driver.find_element_by_class_name('mapaddress').text or ""

    except TimeoutException:
        output["error"] = "Form data took too long to load"

    except NoSuchElementException:
        output["error"] = "One or more form elements could not be found"

    finally:
        if not output.get("error"):
            output["success"] = "Obtained pictures"

        apartment_pics = set()

        for image in apartment_pics_raw:

            im = image.get_attribute('src')
            CORRECT_IMAGE_URL_START = 'https://images'

            if im[:14] == CORRECT_IMAGE_URL_START:
                im = resize_pic(im)
                apartment_pics.add(im)

        output["pics"] = list(apartment_pics)
        output["price"] = apartment_price
        output["address"] = apartment_address
        output["url"] = url

        driver.quit()

        return output


def resize_pic(pic):
    """
    Accepts a URL string for a picture from craigslist
    and resizes the picture to be uniform.
    """

    CORRECT_SIZE = '600x450.jpg'

    if pic[-11:] != CORRECT_SIZE:
        pic = pic[:-10] + CORRECT_SIZE

    return pic
