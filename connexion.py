import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os
import platform

if (platform.system()) == "Windows":
    full_path = (
        "C:\\Users\\"
        + os.getlogin()
        + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default2"
    )
elif (platform.system()) == "Linux":
    full_path = "/home/" + os.getlogin() + "/.config/google-chrome/Default2"
elif (platform.system()) == "Darwin":
    full_path = "/Users/" + os.getlogin() + "/Library/Application Support/Google/Chrome/Default2"  # noqa
else:
    print("OS not supported")
    exit(1)

PROXY = "TO BE DEFINED"
PROXY_LOCAL = "TO BE DEFINED"


def connexion(headless=False, proxy_server=False, local_proxy=False):
    """Setup the chrome driver"""
    chrome_options = the_options(headless, proxy_server, local_proxy)
    driver = uc.Chrome(
        options=chrome_options,
        driver_executable_path="chromedriver",
        version_main=114,
    )
    return driver


def the_options(healess=False, proxy_server=False, local_proxy=False):
    """The options for the chrome driver"""
    chrome_options = Options()
    options_list = [
        "--ignore-certificate-errors-spki-list",
        "log-level=3",
        "--lang=fr",
        "--window-size=1920,1080",
        "--enable-javascript",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        f"--user-data-dir={full_path}",
    ]
    if healess:
        chrome_options.add_argument("--headless")

    if local_proxy:
        chrome_options.add_argument(f"--proxy-server=socks5://{PROXY_LOCAL}")
        chrome_options.add_argument(
            "--host-resolver-rules=MAP * 0.0.0.0 , EXCLUDE 127.0.0.1"
        )

    if proxy_server:
        chrome_options.add_argument(f"--proxy-server={PROXY}")

    for opt in options_list:
        chrome_options.add_argument(opt)
    return chrome_options
