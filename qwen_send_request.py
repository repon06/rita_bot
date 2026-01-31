import logging
import time

import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD, BASE_DIR

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
button_copy_clipboard_located_list = (
    By.CSS_SELECTOR, "pre.qwen-markdown-code div.qwen-markdown-code-header-action-item")
message_copy_located = (By.CSS_SELECTOR, "div.qwen-message-content-text")
label_generation_location = (By.CSS_SELECTOR, "span.prompt-input-input-func-type-text")
button_generation_location = (By.XPATH, "//div[text()='Image Generation' or text()='Генерация изображений']")

generate_image_locator = (By.CSS_SELECTOR, "img.ant-image-img")

generate_image_path = (BASE_DIR / "img" / "generate_image.png")


def generate_poster_holiday(holiday: str | None):
    query_text = ("Создай краткий и емкий промт на английском языке для генерации постера открытки "
                  "с соотношением сторон: 9:16 "
                  "к знаменательному событию в истории: "
                  f"'{holiday}'. "
                  "Выведи в виде кода.")
    logging.info(f'Запускаем в qwen запрос: {query_text}')

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
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")

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

        wait.until(EC.element_to_be_clickable(button_submit_locator)).click()

        # ожидаем перехода на страницу с запросом
        wait.until(EC.visibility_of_element_located(text_title_locator))
        button_temporary_element = (By.CSS_SELECTOR, "div.temporary-chat-entry")
        button_temporary_element = wait.until(EC.visibility_of_element_located(button_temporary_element))
        button_temporary_element.click()
        time.sleep(1)

        textarea_input = wait.until(EC.visibility_of_element_located(textarea_query_locator))
        textarea_input.click()
        textarea_input.clear()
        # textarea_input.send_keys(query_text)
        for l in query_text:
            time.sleep(0.05)
            # if l == "\n":
            #    textarea_input.send_keys(Keys.ENTER)
            textarea_input.send_keys(l)
        time.sleep(0.1)
        # driver.save_screenshot("qwen_logged_1.png")

        '''pyperclip.copy(query_text)
        try:
            textarea_input.send_keys(Keys.COMMAND, "v")  # macOS
        except Exception:
            textarea_input.send_keys(Keys.CONTROL, "v")  # Windows/Linux
            pass'''

        # driver.save_screenshot("qwen_logged_2.png")

        button_send_element = wait.until(EC.element_to_be_clickable(button_send_locator))
        button_send_element.click()

        WebDriverWait(driver, 360).until(EC.presence_of_element_located(button_stop_locator))
        WebDriverWait(driver, 360).until(EC.invisibility_of_element_located(button_stop_locator))

        '''text_result_element_list = wait.until(
            EC.presence_of_all_elements_located(text_result_list_locator))
        text_result_element_list[-1].click()
        result_text = text_result_element_list[-1].text
        print(result_text)

        text_result_element_list = wait.until(
            EC.presence_of_all_elements_located(text_result_list_locator))
        text_result_element_list[-1].click()
        result_text = text_result_element_list[-1].text
        print(result_text)'''

        copy_to_clipboard_element_list = wait.until(
            EC.presence_of_all_elements_located(button_copy_clipboard_located_list))
        copy_to_clipboard_element_list[0].click()

        wait.until(EC.visibility_of_element_located(message_copy_located))

        query_generation = pyperclip.paste()
        print(query_generation)
        logging.info(f'Получили промт: {query_generation}')

        # driver.save_screenshot("qwen_logged.png")

        # переходим к генерации IMG
        button_generation_element = wait.until(EC.element_to_be_clickable(button_generation_location))
        button_generation_element.click()

        wait.until(EC.visibility_of_element_located(label_generation_location))

        textarea_input = wait.until(EC.visibility_of_element_located(textarea_query_locator))
        textarea_input.click()
        textarea_input.clear()
        # textarea_input.send_keys(query_generation)
        for l in query_generation:
            time.sleep(0.05)
            textarea_input.send_keys(l)
        time.sleep(0.1)

        button_send_element = wait.until(EC.element_to_be_clickable(button_send_locator))
        button_send_element.click()

        WebDriverWait(driver, 560).until(EC.presence_of_element_located(button_stop_locator))
        WebDriverWait(driver, 560).until(EC.invisibility_of_element_located(button_stop_locator))

        driver.save_screenshot((BASE_DIR / "img" / "qwen_response.png"))

        download_generate_image(driver, generate_image_path)

        # driver.quit()
        return generate_image_path
    except Exception as e:
        driver.save_screenshot((BASE_DIR / "img" / "error.png"))
        logging.info(f'Ошибка в работе selenium/qwen: {e}')
        print(e)
        return None


def download_generate_image(driver, img_name=None):
    img = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(generate_image_locator)
    )
    url = img.get_attribute("src")

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    with open(img_name, "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    img_holiday_path = generate_poster_holiday("Международный день ювелира")
