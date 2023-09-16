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
        elif arg == "--headless":
            headless = False
        elif arg == "--local-proxy":
            local_proxy = True
        elif arg == "--proxy-server":
            proxy_server = True
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)

    driver = connexion(
        headless=headless, local_proxy=local_proxy, proxy_server=proxy_server
    )
    try:
        driver = chatgpt_automatisation(driver)
    finally:
        driver.close()
        driver.quit()


def my_help():
    print("Usage: python3 chatgpt_automatisation.py [options]")
    print("Options:")
    print("  -h, --help: show this help message and exit")
    print("  --headless: remove headless mode")
    print("  --local-proxy: use local proxy")
    print("  --proxy-server: use proxy server")


def handle_signal(sig, frame):
    """Handle Ctrl+C, Ctrl+Z and Ctrl+D"""
    print("\nYou pressed Ctrl+C, Ctrl+Z or Ctrl+D. Exiting gracefully.")
    sys.exit(0)


def effacement_conversation(driver):
    trash_button = driver.find_elements(
        By.XPATH, "//button[@class='p-1 hover:text-white']"
    )
    trash_button[1].click()
    confirm_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@class='btn relative btn-danger']")
        )
    )
    confirm_button.click()


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


def help_command():
    print(
        "\n\nCommandes disponibles :\n\n"
        "/help : Affiche l'aide\n"
        "/exit : Quitte le programme\n"
        "/clean : Supprime la conversation et en recommance une nouvelle\n"
    )


def manage_message(driver):
    text_to_send = input("\nEnvoyez un message (aide: /help) : ")

    while (
        text_to_send == "/help" or text_to_send == "/clean" or text_to_send == "/exit"
    ):
        if text_to_send == "/help":
            help_command()
        elif text_to_send == "/clean":
            try:
                effacement_conversation(driver)
            except Exception:
                print("La conversation est déjà vide")
        elif text_to_send == "/exit":
            reponse = input("Voulez vous supprimer la conversation ? (O/N) : ")
            if reponse == "O" or reponse == "o":
                try:
                    effacement_conversation(driver)
                except Exception:
                    print("La conversation est déjà vide")
            else:
                print("La conversation n'a pas été supprimée")
            exit()
        text_to_send = input("\nEnvoyez un message (aide: /help) : ")

    return text_to_send


def chatgpt_loop(driver):
    """Chatgpt loop"""

    while 1:
        text_to_send = manage_message(driver)
        chatgpt_prompt = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        chatgpt_prompt.send_keys(text_to_send)

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

    return driver


def chatgpt_automatisation(driver):
    """Chatgpt automatisation"""

    base_url = "https://chat.openai.com/"

    driver.get(base_url)
    driver.implicitly_wait(10)
    try:
        chatgpt_prompt = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
    except Exception:
        chatgpt_prompt = None
    if chatgpt_prompt:
        driver = chatgpt_loop(driver)
    else:
        driver = chatgpt_login(driver)
        chatgpt_prompt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        driver = chatgpt_loop(driver)
    return driver


signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
