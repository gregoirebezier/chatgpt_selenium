import sys
import signal
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from connexion import connexion
from decouple import config
import os
from selenium.webdriver.common.keys import Keys

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
        elif arg in ("-r", "--readme"):
            print("Generating README.md file...")
            driver = connexion(
                headless=headless, local_proxy=local_proxy, proxy_server=proxy_server
            )
            driver = readme_generator(driver, sys.argv[2])
            driver.close()
            driver.quit()
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
    print("  -r, --readme <PYTHON_FILE> : generate README.md file")
    print("  --headless: remove headless mode")
    print("  --local-proxy: use local proxy")
    print("  --proxy-server: use proxy server")


def handle_signal(sig, frame):
    """Handle Ctrl+C, Ctrl+Z and Ctrl+D"""
    print("\nYou pressed Ctrl+C, Ctrl+Z or Ctrl+D. Exiting gracefully.")
    sys.exit(0)


def effacement_conversation(driver):
    trash_button = driver.find_elements(
        By.XPATH, "//button[@class='p-1 hover:text-token-text-primary']"
    )
    trash_button[1].click()
    confirm_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@class='btn relative btn-danger']")
        )
    )
    confirm_button.click()
    return driver


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
                    driver = effacement_conversation(driver)
                except Exception:
                    print("La conversation est déjà vide")
            else:
                print("La conversation n'a pas été supprimée")
            exit()
        text_to_send = input("\nEnvoyez un message (aide: /help) : ")

    return text_to_send


def chatgpt_loop(driver):
    """Chatgpt loop"""

    send_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-testid='send-button']")
        )
    )
    send_button.click()
    WebDriverWait(driver, 50).until(
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

    return driver, responses


def setup_chatgpt(driver):
    """Setup chatgpt"""
    base_url = "https://chat.openai.com/"

    driver.get(base_url)
    driver.implicitly_wait(10)
    try:
        chatgpt_prompt = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        chatgpt_prompt = 1
    except Exception:
        chatgpt_prompt = 0

    if chatgpt_prompt:
        print("CONNECTED!\n\n")
    else:
        print("NOT CONNECTED!\n\n")
        with open("source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver = chatgpt_login(driver)
        chatgpt_prompt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
    return driver


def chatgpt_automatisation(driver):
    """Chatgpt automatisation"""
    print("ChatGPT automatisation\n")
    driver = setup_chatgpt(driver)
    while 1:
        text_to_send = manage_message(driver)

        chatgpt_prompt = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@id='prompt-textarea']")
            )
        )
        chatgpt_prompt.send_keys(text_to_send)

        driver, responses = chatgpt_loop(driver)
        print("\nChatGPT:\n", responses[-1].text)
    return driver


def write_prompt(driver, text_to_send):
    """Write prompt"""
    print("Writing prompt...\n It may take a while... ~ 30s")
    chatgpt_prompt = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='prompt-textarea']"))
    )
    for line in text_to_send:
        chatgpt_prompt.send_keys(line.replace("\n", ""))
        chatgpt_prompt.send_keys(Keys.SHIFT + Keys.ENTER)

    return driver


def readme_generator(driver, filepath):
    """Generate README.md file"""
    gpt_readme_generator_prompt = "Je te présente le code source principal de mon nouveau projet Python. À partir de ce code, génère un README.md détaillé en format Markdown. Assure-toi d'inclure: Le titre du projet. Une brève description. Les prérequis nécessaires pour exécuter le code. Les étapes d'installation. Un exemple d'utilisation basé sur le code fourni. Les fonctionnalités principales basées sur les fonctions présentes dans le code. Une section 'Contributeurs' (même si elle est vide pour l'instant). Seul le contenu Markdown du README.md est attendu en réponse. Aucun commentaire, explication supplémentaire, ou autre format que le Markdown n'est nécessaire. Voici le code :"  # noqa

    driver = setup_chatgpt(driver)
    sleep(2)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            code_text = f.readlines()
            code_text.insert(0, gpt_readme_generator_prompt)
            driver = write_prompt(driver, code_text)
            driver, responses = chatgpt_loop(driver)
            responses = (
                responses[-1].text.replace("markdown", "").replace("Copy code", "")
            )
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(responses)
            driver = effacement_conversation(driver)
    else:
        print("File not found")
        sys.exit(1)
    return driver


signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
