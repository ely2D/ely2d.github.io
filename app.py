from flask import Flask, jsonify
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)

# Setup the service and options for the driver
service = Service(executable_path="D:/Uni/Diplomatiki/chromedriver-win64/chromedriver.exe")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run without opening the browser window
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

def get_electricity_bill(username, password):
    driver.get("https://app.ydata.eu/login")  # Replace with the actual site
    try:
        # Wait for the body to be visible (indicating page is loaded)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

        # Locate and interact with the email field
        email = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        email.send_keys(username)

        # Locate and interact with the password field
        password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_input.send_keys(password)

        # Simulate pressing the Enter key to submit the form
        password_input.send_keys(Keys.RETURN)

        # Wait for the bill amount element to be visible and extract the bill amount
        bill_amount_element = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Συνολικό ποσό προς πληρωμή')]/following-sibling::h5//strong")
        ))

        # Get the text from the <strong> element
        bill_amount = bill_amount_element.text.strip()
        return bill_amount

    except TimeoutException:
        print("Timeout error")
        return None

    finally:
        driver.quit()


@app.route('/get_bill_amount', methods=['GET'])
def get_bill_amount():
    # Example usage: username and password would ideally be taken securely
    username = "romanos.kotsis135@gmail.com"
    password = "!730197227LoL"
    bill_amount = get_electricity_bill(username, password)
    
    if bill_amount:
        return jsonify({"bill_amount": bill_amount})
    else:
        return jsonify({"error": "Failed to fetch bill amount"}), 500


if __name__ == '__main__':
    app.run(debug=True)
