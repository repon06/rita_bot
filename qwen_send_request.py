from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD

input_mail_locator = (By.CSS_SELECTOR, "input[name='email']")  # "input[name='login']"
input_password_locator = (By.CSS_SELECTOR, "input[name='password']")
button_submit_locator = (By.CSS_SELECTOR, "button.qwenchat-auth-pc-submit-button.brandprimary")
text_title_locator = (
    By.XPATH, "//div[contains(@class,'placeholder-logo-text')]")  # (By.CSS_SELECTOR, "div.placeholder-logo-text")
textarea_query_locator = (By.CSS_SELECTOR, "textarea.chat-input")
button_send_locator = (By.CSS_SELECTOR, "button.send-button")
text_result_list_locator = (By.CSS_SELECTOR, 'div.qwen-markdown-code-body')
button_stop_locator = (By.CSS_SELECTOR, "button.stop-button")
text_full_result_list_locator = (By.CSS_SELECTOR, "div.view-line")


def main():
    opts = Options()

    # Отключаем автосохранение паролей
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }
    opts.add_experimental_option("prefs", prefs)

    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-infobars")

    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # opts.add_argument("--headless=new")

    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 120)

    '''driver.get("https://chat.qwen.ai/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.auth-buttons")))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.auth-buttons button.brandprimary"))).click()'''
    try:
        driver.get("https://chat.qwen.ai/auth")

        email_input = wait.until(EC.element_to_be_clickable(input_mail_locator))
        email_input.send_keys(EMAIL)

        pass_input = wait.until(EC.visibility_of_element_located(input_password_locator))
        pass_input.send_keys(PASSWORD)
        # driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        wait.until(EC.element_to_be_clickable(button_submit_locator)).click()

        wait.until(EC.visibility_of_element_located(text_title_locator))

        textarea_input = wait.until(EC.visibility_of_element_located(textarea_query_locator))
        textarea_input.send_keys("создай краткий и емкий промт для генерации изображения открытки к "
                                 "Знаменательному событию в истории: "
                                 "Зарегистрирован товарный знак «Кока-Кола»")

        button_send_element = wait.until(EC.element_to_be_clickable(button_send_locator))
        button_send_element.click()

        WebDriverWait(driver, 360).until(EC.visibility_of_element_located(button_stop_locator))
        WebDriverWait(driver, 360).until(EC.invisibility_of_element_located(button_stop_locator))

        text_result_element_list = wait.until(
            EC.presence_of_all_elements_located(text_result_list_locator))
        result_text = text_result_element_list[-1].text
        print(result_text)

        text_result_element_list = wait.until(
            EC.presence_of_all_elements_located(text_result_list_locator))
        result_text = text_result_element_list[-1].text
        print(result_text)

        driver.save_screenshot("qwen_logged.png")
        # driver.quit()
    except Exception as e:
        driver.save_screenshot("error.png")
        print(e)
        raise


if __name__ == "__main__":
    main()
