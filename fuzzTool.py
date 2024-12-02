import urllib.request
import urllib.parse
import threading
import queue
import random

RESET = "\033[0m"
RED = "\033[91m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"

def display_design():
        directory_tree = f"""
        {BOLD}/root{RESET}
        │
        ├── {CYAN}/folder1{RESET}
        │   ├── {GREEN}/subfolder1{RESET}
        │   │   └── {BLUE}/subsubfolder1{RESET}
        │   └── {GREEN}/subfolder2{RESET}
        │       └── {BLUE}/subsubfolder2{RESET}
        └── {CYAN}/folder2{RESET}
            └── {GREEN}/subfolder3{RESET}
                └── {YELLOW}/subsubfolder3{RESET}    {BOLD}V1 created by L9jaa3xMA{RESET}
        """

        print(directory_tree)

threads = 50
target_url = ""
wordlist_file = "./res/all.txt"
user_agent_file = "./res/user_agent.txt"
resume = None


def load_user_agent(user_agent_file):
    try:
        with open(user_agent_file, "r", encoding="utf-8") as f:
            user_agents = f.readlines()
        return random.choice(user_agents).strip()
    except IOError:
        return "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"


def build_wordlist(wordlist_file):
    with open(wordlist_file, "rb") as fd:
        raw_words = fd.readlines()
    found_resume = False
    words = queue.Queue()
    for word in raw_words:
        word = word.rstrip().decode("utf-8")
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
        else:
            words.put(word)
    return words


def dir_bruter(word_queue, user_agent, target_url, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        if extensions:
            attempt_list.extend([f"{attempt}.{ext}" for ext in extensions])
        else:
            attempt_list.append(attempt)

        for brute in attempt_list:
            url = f"{target_url}/{urllib.parse.quote(brute)}"
            try:
                headers = {"User-Agent": user_agent}
                request = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(request)
                if response.getcode() == 200:
                    print(f"{BOLD} {GREEN}[+] Found: %s {RESET}" % url)
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print(f"{BOLD}{YELLOW}[-] {e.code}: {url}{RESET}")
            except urllib.error.URLError as e:
                print(f"{BOLD}{RED}[-] Failed: {url} ({e.reason}){RESET}")


if __name__ == "__main__":
    display_design()
    target_url_input = input(f"{BOLD}Enter target URL: {RESET}").strip()
    while target_url_input == "" :
        target_url_input = input(f"{BOLD}Please Enter target URL: {RESET}").strip()
    target_url = target_url_input
    
        

    wordlist_file_input = input(f"{BOLD}Enter wordlist file path (default: all.txt): {RESET}").strip()
    if wordlist_file_input:
        wordlist_file = wordlist_file_input

    threads_input = input(f"{BOLD}Enter number of threads (default: {threads}):{RESET}").strip()
    if threads_input.isdigit():
        threads = int(threads_input)

    user_agent = load_user_agent(user_agent_file)
    word_queue = build_wordlist(wordlist_file)
    extensions = ["php", "bak", "orig", "old", "txt"]

    print(f"{BOLD}{BLUE}Starting brute-force attack with {threads} threads using User-Agent: {user_agent}{RESET}")
    thread_list = []

    for i in range(threads):
        t = threading.Thread(target=dir_bruter, args=(word_queue, user_agent, target_url, extensions))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()
