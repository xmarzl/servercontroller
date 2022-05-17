#!/usr/bin/python3
import os
import sys
import subprocess
import discord

# -- Global Var
# --- Directory
directory_base   = '/home/discordbot/servercontroller'
directory_config = directory_base + '/config'

# --- Config
config_discord = directory_config + '/discord.cfg'
config_users   = directory_config + '/users.cfg'
config_server  = directory_config + '/server.cfg'

# --- Strings
string_usage = '!server help - for more help'

# -- Subs
# -- open config as hash
def open_config_hash(path_to_file):
    map_output = {}
    fh_config = open(path_to_file, 'r')
    for line_key_value in fh_config:
        if ':' in line_key_value:
            line_key, line_value = str(line_key_value).rstrip().split(':', 1)
            map_output[line_key] = line_value
    fh_config.close()
    return map_output
    
# -- open config as array
def open_config_array(path_to_file):
    array_output = []
    fh_config = open(path_to_file, 'r')
    for line_input in fh_config:
        array_output.append(str(line_input).rstrip())
    fh_config.close()
    return array_output

# -- create file and return success-state
def create_file(path_to_file):
    if not os.path.exists(path_to_file):
        print ('creating file: ' + path_to_file)
        open(path_to_file, 'w').close()
    if os.path.isfile(path_to_file):
        print ('file exists: ' + path_to_file)
        return True
    print ('file not found: ' + path_to_file)
    return False

# -- create directory and return success-state
def create_directory(path_to_directory):
    if not os.path.exists(path_to_directory):
        print ('creating directory: ' + path_to_directory)
        os.mkdir(path_to_directory)
    if os.path.isdir(path_to_directory):
        print ('directory exists: ' + path_to_directory)
        return True
    print ('directory not found: ' + path_to_directory)
    return False

# -- start systemctl service
def server_start(servername):
    os.system('systemctl start {service}'.format(service=servername))
    output = subprocess.run('systemctl status {service} | grep Active:'.format(service=servername),
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
    return output

# -- stop systemctl service
def server_stop(servername):
    os.system('systemctl stop {service}'.format(service=servername))
    output = subprocess.run('systemctl status {service} | grep Active:'.format(service=servername),
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
    return output

# -- see status of systemctl service
def server_status(servername):
    output = subprocess.run('systemctl status {service} | grep Active:'.format(service=servername),
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
    return output

# -- command subs
def command_help(author_rank):
    output = 'Keine Hilfe für dich.';
    if(author_rank == 'user' or author_rank == 'admin'):
        output = 'So bekommt man die UserID:\n\
Rechtsklick auf den User (rechts) -> ID kopieren -> Einfügen\n\
!server \n\
!server start <servername>\n\
!server stop <servername>\n\
!server status <servername>\n\
!server list\n\
!server listuser\n\
!server checkrank <userid>'
    if(author_rank == 'admin'):
        output = output + '\n!server setuser <userid>\n\
!server remuser <userid>'
    return output



# -- init
# --- create client
client = discord.Client()

# --- create directory
if not create_directory(directory_config):
    print ('cant proceed without directory: ' + directory_config)
    sys.exit(1)
    
# --- create files
if not create_file(config_discord):
    print ('cant proceed without config: ' + config_discord)
    sys.exit(1)
if not create_file(config_users):
    print ('cant proceed without config: ' + config_discord)
    sys.exit(1)
if not create_file(config_server):
    print ('cant proceed without config: ' + config_discord)
    sys.exit(1)

# -- config contains token and guild
hash_discord = open_config_hash(config_discord)

guild_id = hash_discord['guild']
guild = None;

# -- start
# -- when client login
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('id: ' + str(client.user.id))
    print('guild_id: ' + guild_id)

# -- when user sends message
@client.event
async def on_message(message):
    
    guild = client.get_guild(int(guild_id))
    
    # --- do not reply yourself
    if message.author == client.user:
        return
    
    # --- return if guild is not the selected one
    if message.author.guild != guild:
        print ('Authors\'s guild is not ' + guild_id)
        return
    
    # --- split arguments in 
    args = message.content.lower().split(' ')
    args_length = len(args)
    
    # --- return if its not bot's command
    if not args[0] == '!server':
        return
    
    array_server = open_config_array(config_server)
    hash_users = open_config_hash(config_users)
    
    author_name = message.author.name
    author_id = str(message.author.id)
    author_rank = 'none'
    
    # -- set rank if id exists in users config
    if(author_id in hash_users.keys()):
        author_rank = hash_users[author_id]
    
    print ('Command from: ' + author_name + ':' + author_id + ':' + author_rank)
    print ('Executed: ' + ' '.join(args))
    msg = string_usage
    
    # -- send help if command is only "!server"
    if args_length == 1:
        msg = command_help(author_rank)
    
    # -- two arguments
    elif args_length == 2:
    
        # --- list all server
        if args[1] == 'list':
            if(author_rank == 'user' or author_rank == 'admin'):
                msg = 'Serverlist:\n'
                for server in array_server:
                    msg = msg + ' - ' + server + "\n"
                
        # --- list all roles (e.g. admin, user)
        elif args[1] == 'listuser':
            if(author_rank == 'user' or author_rank == 'admin'):
                msg = 'Userlist:\n'
                for user_id in hash_users.keys():
                    msg = msg + ' - ' + user_id + ' -> ' + hash_users[user_id] + "\n"
        
        # --- args_length==2 - no command found
        else:
            msg = string_usage

    # -- three arguments
    elif args_length == 3:
        
        # --- command start <server>
        if(args[1] == 'start'):
            if(author_rank == 'user' or author_rank == 'admin'):
                
                # ---- check if server/service allowed
                if(args[2] in array_server):
                    msg = server_start(args[2])
                else: 
                    msg = 'Den Server habe ich nicht gefunden...'
                    
        # --- command status <server>
        elif(args[1] == 'status'):
            if(author_rank == 'user' or author_rank == 'admin'):
        
            # ---- check if server/service allowed
                if(args[2] in array_server):
                    msg = server_status(args[2])
                else: 
                    msg = 'Was meinst du denn mit "' + args[2] + '"?'
        
        # --- command stop <server>
        elif(args[1] == 'stop'):
            if(author_rank == 'user' or author_rank == 'admin'):
        
            # ---- check if server/service allowed
                if(args[2] in array_server):
                    msg = server_stop(args[2])
                else: 
                    msg = 'Von dem Server habe ich noch nie gehört.'
        
        # --- command adduser <username> 
        elif(args[1] == 'setuser'):
            if(author_rank == 'admin'): 
            
                target_rank = None    
                
                # -- check if input is a number
                if(args[2].isnumeric()):
                
                    # ---- searching for targets rank               
                    if(args[2] in hash_users.keys()):
                        target_rank = hash_users[args[2]]
                
                    # ---- checking if target is admin or user
                    if(target_rank == 'admin'):
                        msg = 'Ich degradiere keinen Admin.'
                    elif(target_rank == 'user'):
                        msg = 'Mit der ID existiert bereits ein user.'
                    else:
                        msg = 'Ein Fehler ist augetreten. Oh mann...'
                        hash_users[args[2]] = 'user'
                        fh_config_users = open(config_users, 'w')
                        for user_id in hash_users:
                            user_rank = hash_users[user_id]
                            fh_config_users.write(user_id + ':' + user_rank + "\n")
                            if(user_id == args[2]):
                                msg = user_id + ' wurde hinzugefügt!'
                        fh_config_users.close()
                        
                # ---- if input is not a number
                else:
                    msg = 'Deine Eingabe muss numerisch sein.'
        
        # --- command remuser <username>
        elif(args[1] == 'remuser'):
            if(author_rank == 'admin'): 
            
                target_rank = None
                
                # -- check if input is a number
                if(args[2].isnumeric()):
                
                    # ---- searching for targets rank               
                    if(args[2] in hash_users.keys()):
                        target_rank = hash_users[args[2]]
                
                    # ---- checking if target is admin or user
                    if(target_rank == 'admin'):
                        msg = 'Tut mir leid, aber einem Admin die Rolle zu entziehen?!'
                    else:
                        msg = 'Ein Fehler ist augetreten. Ups.'
                        fh_config_users = open(config_users, 'w')
                        for user_id in hash_users:
                            if(user_id == args[2]):
                                msg = user_id + ' wurde entfernt.'
                                continue
                            user_rank = hash_users[user_id]
                            fh_config_users.write(user_id + ':' + user_rank + "\n")
                        fh_config_users.close()
                        
                # ---- if input is not a number
                else:
                    msg = 'Deine Eingabe muss numerisch sein.'
        # --- check rank of target user
        elif(args[1] == 'checkrank'):
            if(author_rank == 'user' or author_rank == 'admin'):
            
                target_rank = 'none'
                
                # ---- searching for targets rank               
                if(args[2] in hash_users.keys()):
                    target_rank = hash_users[args[2]]
                
                if(target_rank == 'none'):        
                    msg = 'Das Mitglied besitzt noch keine Rolle.'
                else:
                    msg = 'That\'s it --> ' + target_rank
        
    # -- send message
    await message.channel.send(msg)    

# -- start client
print ('running client')
token = hash_discord['token']
print ('token:' + token)
client.run(token)