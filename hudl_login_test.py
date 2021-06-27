from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unittest
from selenium.common.exceptions import TimeoutException

class TestHudlLogin(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.hudl.com/login")

    def tearDown(self):
        self.browser.quit()

    def input(self, element, text):
        element.clear()
        element.send_keys(text)

    def test_given_incorrect_login_when_logging_in_then_error_message_appears(self):
        email_box = self.browser.find_element_by_id("email")
        self.input(email_box,"Blahblah@blah.com")

        password_box = self.browser.find_element_by_id("password")
        self.input(password_box,"password1234")

        submit_button = self.browser.find_element_by_id("logIn")
        submit_button.click()

        expected_text = "We didn't recognize that email and/or password. Need help?"

        try:
            WebDriverWait(self.browser, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "login-error-container"), expected_text)
            )
        except TimeoutException:
            self.fail("Element container, login-error-container, couldn't be found.")

        error_message = self.browser.find_element_by_class_name("login-error-container").find_element_by_tag_name("p")

        self.assertEqual(error_message.text, expected_text, "Error message didn't appear.")

    def test_given_unknown_login_details_when_logging_in_then_reset_message_appears(self):

        need_help_button = self.browser.find_element_by_id("forgot-password-link")
        need_help_button.click()

        expected_text = "Login Help"

        try:
            WebDriverWait(self.browser, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "reset-info"), expected_text)
            )
        except TimeoutException:
            self.fail("Element container, reset-info, couldn't be found.")

        error_message = self.browser.find_element_by_class_name("reset-info").find_element_by_tag_name("h1")

        self.assertEqual(error_message.text, expected_text, "Login Help message didn't appear.")

    def test_given_unknown_login_details_when_logging_in_then_resetting_message_successfully(self):

        need_help_button = self.browser.find_element_by_id("forgot-password-link")
        need_help_button.click()
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.ID, "forgot-email"))
            )
        except TimeoutException:
            self.fail("Element forgot email couldn't be found.")

        email_box = self.browser.find_element_by_id("forgot-email")
        self.input(email_box, "fatimaaldabagh@hotmail.com")

        send_password_button = self.browser.find_element_by_id("resetBtn")
        send_password_button.click()

        expected_text = "Check Your Email"

        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "reset-sent-container"))
            )
        except TimeoutException:
            self.fail("Element container, check email message, couldn't be found.")

        error_message = self.browser.find_element_by_xpath("//*[contains(@class, 'reset-sent-container')]").find_element_by_class_name("reset-info").find_element_by_tag_name("h4")

        self.assertEqual(error_message.text, expected_text, "Email wasn't sent successfully, reset message didn't appear.")

    def test_given_nonexistent_login_details_when_resetting_then_error_message_appears(self):

        need_help_button = self.browser.find_element_by_id("forgot-password-link")
        need_help_button.click()

        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "reset-info"))
            )
        except TimeoutException:
            self.fail("Element container, reset-info, couldn't be found.")

        email_box = self.browser.find_element_by_id("forgot-email")
        self.input(email_box, "thisis@hotmail.com")

        send_password_button = self.browser.find_element_by_id("resetBtn")
        send_password_button.click()

        expected_text = "That email address doesn't exist in Hudl. Check with your coach to ensure they have the right email address for you."

        try:
            WebDriverWait(self.browser, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "reset-error-container"), expected_text)
            )
        except TimeoutException:
            self.fail("Element container, reset-error-container, couldn't be found.")

        error_message = self.browser.find_element_by_class_name("reset-error-container").find_element_by_tag_name("p")

        self.assertEqual(error_message.text, expected_text, "Error message didn't appear.")

#Please change the elements in the brackets to include a valid login
    def test_given_correct_login_when_logging_in_then_home_button_appears(self):
        email_box = self.browser.find_element_by_id("email")
        self.input(email_box,"email")

        password_box = self.browser.find_element_by_id("password")
        self.input(password_box,"password")

        submit_button = self.browser.find_element_by_id("logIn")
        submit_button.click()

        expected_text = "View Profile"

        try:
            WebDriverWait(self.browser, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "profile-edit"), expected_text)
            )
        except TimeoutException:
            self.fail("Element with the ID, profile-edit, couldn't be found.")

        profile_message = self.browser.find_element_by_class_name("profile-edit")

        self.assertEqual(profile_message.text, expected_text, "View Profile button didn't appear.")


if __name__ == '__main__':
    unittest.main()
