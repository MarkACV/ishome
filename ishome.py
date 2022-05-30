from distutils.command.config import config
import subprocess
import pyfiglet
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


banner = pyfiglet.figlet_format('Welcome to ishome!')



def manage():
    print('** Manage devices **\n')
    file = open('devices.txt','r')
    lines =file.readlines()
    for line in lines:
        print(line.strip('\n'))
    file.close()
        

    opt = int(input('----------------------\n1) Add device\n2) Remove device\n99) Return\n Choose option: '))
    while (opt != 99):

        if (opt == 1):
            name = input("Insert device's name: ")
            ip = input("Insert devices IP address: ")
            file = open('devices.txt','a')
            file.write(name+';'+ip+'\n')
            file.close()
            break


        if (opt == 2):
            file = open('devices.txt','w')
            name_to_del = input("Insert device's name: ")
            for line in lines:
                if(name_to_del in line):
                    pass
                else:
                    file.write(line)
            file.close()

            break



def check():
    print('** Check **')
    file = open('devices.txt','r')
    lines =file.readlines()
    for line in lines:
        print(line.strip('\n'))
    name = str(input("Insert device's name: "))
    for line in lines:
        if (name in line):
            print('[+] Verifying connection with device\n')
            namelist =line.strip('\n').split(';')
            
            response = subprocess.run('ping '+namelist[1]+' -w 2',stdout=subprocess.DEVNULL)
           
            if (response.returncode == 0):
                print(name+' is connected to de LAN!')
            else:
                print(name+" is NOT connected to de LAN\nconsider there might be trouble if the phone's screen is turned off")  
  
def monitor():

   
    nameslist = []
    file = open('devices.txt','r')
    lines =file.readlines()
    print('[+] Devices:')
    for line in lines:
        print(line.strip('\n'))
    while True:
        name = input('Device to be monitored (enter to end): ')
        if (name != ''):
            nameslist.append(name)
        else:
            break
    option = int(input('[+] Notify when the device(s)...\n1) Connect\n2) Disconnect\n3) Both\n Choose option: '))
    interval = int(input('[+] Insert time interval (minutes): '))
    print('[+] Monitoring...')

    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        file1 = open('monitorfile.txt','w')
        file1.write('')
        for name in nameslist:
            file = open('devices.txt','r')
            lines =file.readlines()
            for line in lines:
                if (name in line):
                    linelist = line.strip('\n').split(';')
                    response = subprocess.run('ping '+linelist[1]+' -w 2',stdout=subprocess.DEVNULL)
                   

                   
                    if (response.returncode == 0 and option ==1):
                        file1 = open('monitorfile.txt','a')
                        file1.write(name+' is connected to the LAN\n')   
                      
                                       
                    

                    
                    if (response.returncode != 0 and option ==2):
                        file1 = open('monitorfile.txt','a')
                        file1.write(name+' is NOT connected to the LAN\n')
                        
                        

                    
                    if (response.returncode != 0 and option ==3):
                        file1 = open('monitorfile.txt','a')
                        file1.write(name+' is NOT connected to the LAN\n')
                        
                
                            
                        
                    if (response.returncode == 0 and option ==3):
                        file1 = open('monitorfile.txt','a')
                        file1.write(name+' is connected to the LAN\n')
                     
                  
                    
                    file1.close()


        mail_content = ''
        file = open('monitorfile.txt','r')
        lines=file.readlines()
        for line in lines:
            mail_content += line+'\n'
    
        file.close()
        if (mail_content != ''):
            #The mail addresses and password
            sender_address = config.sender
            sender_pass = config.password
            receiver_address = config.receiver
            #Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Connection report ['+ current_time+']'   #The subject line
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()

            print('email sent')
        


        time.sleep(interval*60)
    




def menu():
    while True:
        print(banner)
        opt =int(input('\n1) Check if someone is connected to LAN\n2) Manage devices\n3) Monitor mode\n99) Exit\nChoose option: '))
        if (opt == 1):
            check()
            break
        if (opt == 2):
            manage()
        if (opt == 3):
            monitor()
        if (opt == 99):
            break




if __name__ =="__main__":
    menu()