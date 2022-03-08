# Whatsapp-automation
whatsapp automation using selenium and chrome webdriver
# this whatsapp bot has not been updated for a while.
Chromedriver is required. Check your chrome version before installing chromedriver. Dowload chrome driver according to your version an OS from https://chromedriver.chromium.org/ 
Put chrome driver in same place as the python file.
The function takes a total of 8 arguments.
All arguments have default value and in below given order, so passing all is not important.
message="", file="no.csv", delay=10, number=0, session_id=0, a=0, b=1, c=2.
Message argument is a custom message. Use <> wherever you want the recipient's name to enter from the csv. If no name is given against the number a generic sir/ma'am is used.
eg: message = "Hi <>, good morning.<>, this is a system generated message."
Generic output:  Hi Sir/ma'am, good morning.Sir/Ma'am, this is a system generated message.
Custom output: Hi YourName, good morning. YourName, this is a system generated message.
If a generic message using same format is given against the number that message will be modified according to the given name or generic name.
if neither message argument nor custom message in column is given the number is skipped.
If No file name is given or invalid filename. The function use the given number and message to send only that recipient.
Delay is in seconds. Delay may vary depending on the network speed.
Todo:
Using multiple sessions to speedup the process
A further modification can be done to add multiple arguments using <1>,<2> etc placeholder strings. 
a,b,c are number, name, message columns respectively defining the order of columns in your csv file.
Default order is number,name,message
