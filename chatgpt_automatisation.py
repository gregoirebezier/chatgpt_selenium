import sys
import signal
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from connexion import connexion
from decouple import config

sys.tracebacklimit = 0


def main():
    """Main function"""
    headless = True
    local_proxy = False
    proxy_server = False

    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            my_help()
            sys.exit(0)
        elif arg == "-t" or arg == "--text":
            arg = sys.argv[2]
            break
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)

    driver = connexion(
        headless=headless, local_proxy=local_proxy, proxy_server=proxy_server
    )
    try:
        chatgpt_automatisation(driver, arg)
    finally:
        driver.close()
        driver.quit()


def my_help():
    print("Usage: python3 chatgpt_automatisation.py [options]")
    print("Options:")
    print("  -h, --help: show this help message and exit")
    print("  -t, --text: text to send")
    print("Example:")
    print('  python3 chatgpt_automatisation.py -t "Bonjour, comment allez-vous ?"')


def handle_signal(sig, frame):
    """Handle Ctrl+C, Ctrl+Z and Ctrl+D"""
    print("\nYou pressed Ctrl+C, Ctrl+Z or Ctrl+D. Exiting gracefully.")
    sys.exit(0)


def chatgpt_login(driver):
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-testid='login-button']")
        )
    )
    login_button.click()
    sleep(1)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
    )
    email_input.send_keys(config("EMAIL"))
    sleep(1)
    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@name='action']"))
    )
    continue_button.click()
    sleep(1)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
    )

    password_input.send_keys(config("PASSWORD"))
    sleep(1)
    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/main/section/div/div/div/form/div[3]/button")
        )
    )
    continue_button.click()
    sleep(1)
    print("CONNECTED!\nWaiting for the OK button...")
    try:
        ok_button = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='btn relative btn-primary']")
            )
        )
        ok_button.click()
    except Exception:
        pass
    print("OK button clicked!, enjoy!\n\n")
    print("-" * 50 + "\n")
    return driver


def chatgpt_loop(driver):
    """Chatgpt loop"""

    while 1:
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-testid='send-button']")
            )
        )
        send_button.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='btn relative btn-neutral -z-0 whitespace-nowrap border-0 md:border']",  # noqa
                )
            )
        )
        responses = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='markdown prose w-full break-words dark:prose-invert light']",  # noqa
                )
            )
        )
        print("\nChatGPT:\n", responses[-1].text)
        text_to_send = input('\nEnvoyez un message (quitter: "exit") : ')
        if text_to_send == "exit":
            break
        chatgpt_prompt = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        chatgpt_prompt.send_keys(text_to_send)


def chatgpt_automatisation(driver, text_to_send):
    """Chatgpt automatisation"""

    base_url = "https://chat.openai.com/"

    driver.get(base_url)
    driver.implicitly_wait(10)
    chatgpt_prompt = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='prompt-textarea']"))
    )
    if chatgpt_prompt:
        chatgpt_prompt.send_keys(text_to_send)
        chatgpt_loop(driver)
    else:
        driver = chatgpt_login(driver)
        chatgpt_prompt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        chatgpt_prompt.send_keys(text_to_send)
        chatgpt_loop(driver)


signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
