# svc.py
discordbot that can manage ubuntu services

Here is no explanation on how to setup the discordbot.  
Only how to install the script.  
More help here:  
https://discordpy.readthedocs.io/en/stable/discord.html  
  
(Output language is German)  
  
## Help output:
```
So bekommt man die UserID:
Rechtsklick auf den User (rechts) -> ID kopieren -> Einfügen
!server 
!server start <servername>
!server stop <servername>
!server status <servername>
!server list
!server listuser
!server checkrank <userid>
```
## Admin can see two more commands:
```
!server setuser <userid> 
!server remuser <userid> 
```

## Installation:
```sh
mkdir /opt/servercontroller
cd /opt/servercontroller
wget https://raw.githubusercontent.com/xmarzl/servercontroller/main/svc.py
chmod 750 /opt/servercontroller/svc.py
./svc.py
```
Exit script with ctrl + c
```sh
cd ./config
vim discord.cfg
token:xxxxxxxxxxxxxxxxxx
guild:xxxxxxxxxxxxxxxxxx
```
ESC + :wq  
  
Add as many services as you want to server.cfg  
Be careful with adding specific services.  
It could affect the security.  
  
The only way to add an admin is by writing it to the users.cfg:  
insert your DiscordID, separate with colon and insert "admin"  
After that, save and start the client.  
```sh
vim users.cfg
1234567890:admin
```
