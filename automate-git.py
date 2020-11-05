#Init a local git repo, create remote repo using github API and push local to remote. prompts for user input

import subprocess
import json
from pathlib import Path
from configparser import ConfigParser

# config file contains user settings
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

#--------------- local set up ---------------#

def create_local_git_repo():
    
    # set directory to create repo
    directory = config.get('your_settings', 'directory')

    #create directory if it doesn't exist
    check_dir = Path(directory)
    if check_dir.exists():
        print("Directory exists. Skip create directory")
    else:
        subprocess.run(["mkdir", directory])

    # set repo name
    repo_name = config.get('your_settings', 'repo_name')

    directory = directory + '/' + repo_name
    print("You selected repo %s" %directory)

    #create repo folder if it doesn't exist
    check_repo = Path(directory)
    if check_repo.exists():
        print("Repo already exists. Skip git init")
    else:
        subprocess.run(["mkdir", directory])
        #init repo
        subprocess.run(["git", "init"], cwd=directory)

    pass
    return directory, repo_name


def create_local_repo_file(directory):

    # set file to commit
    first_file = config.get('your_settings', 'commit_file')
    file_path = directory + "/" + first_file

    #create file if it doesn't exist
    check_file = Path(file_path)
    if check_file.exists():
        print("File already exists. Skip create file") 
    else:
        subprocess.run(["touch", first_file], cwd=directory)
    pass
    return first_file


def add_files_for_commit(directory, first_file):

    #stage file created
    subprocess.run(["git", "add", first_file], cwd=directory)
    pass

def commit_files(directory):

    # set commit message
    msg = config.get('your_settings', 'first_commit_msg')

    #commit file
    subprocess.run(["git", "commit", "-m", msg], cwd=directory)


    pass


#--------------- remote setup ---------------#

def create_github_repo(repo_name, auth_type):

    #ask for user github account name
    github_name  = config.get('your_settings', 'github_name')

    #generate data for request, set repo to private
    repo_config = '{"name": "%s", "private": "true"}' %repo_name

    #create repo
    if auth_type == 'token':
        access_token = config.get('your_settings', 'your_token')
        header = 'Authorization: token ' + access_token
        response = subprocess.run(["curl", "--header", header, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)
    
    else:
        response = subprocess.run(["curl", "--user", github_name, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    #confirm repo now exists under user
    if auth_type == 'token':
        response = subprocess.run(["curl", "--header", header, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)
    
    else:
        response = subprocess.run(["curl", "--user", github_name, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)
    
    #convert from completed process for easier parsing
    response_json = json.loads(response.stdout.decode("utf-8"))
    print("%d repos by user" %len(response_json))

    #confirm repo is created and extract url
    for repo_id in range(len(response_json)):        
        remote_name = response_json[repo_id]['name']
        remote_url = response_json[repo_id]['html_url'] 
        # print(remote_name) 
        # print(remote_url) 
    
        if(remote_name == repo_name):
            print("Repo now created on github")
            break
    pass
    return github_name, remote_url


#--------------- link local and remote ---------------#

def add_remote_repo_url(directory, github_name, remote_url, auth_type):

    #url for repo
    server = remote_url + ".git"
    print("server: %s" %server)
    
    if auth_type == 'token':
        access_token = config.get('your_settings', 'your_token')
        server = server.replace("//", "//%s:%s@" %(github_name, access_token))

    else:
        server = server.replace("//", "//%s@" %(github_name))

    print("server: %s" %server)

    #set origin
    subprocess.run(["git", "remote", "set-url", "origin", server], cwd=directory)

    pass
    return server


def push_local_repo_to_remote(directory, server):

    #insert username to origin url
    push_url = server
    print("push url: %s" %push_url)

    #push to server
    subprocess.run(["git", "push", "-u", push_url, "master"], cwd=directory)
    pass
    

def remote_auth_option():
    print("Select authentication type to github")

    auth_type = config.get('your_settings', 'auth_type')

    if auth_type == 'token':
        print("Using Token")
    elif auth_type == "login":
        print("Using Password")
    else:
        print("ERROR! Ivalid option for authorisation type in config.ini file")
        exit()

    pass
    return auth_type


# def read_token_from_file():

#     TOKEN_LEN = 40
    
#     #read token from file
#     with open('token', 'r') as token_file:
#         token = token_file.read(TOKEN_LEN)
#         print("Access token found: %s" %token)

#     return token


def start_program_flow():
    
    print("------ Start ------")

    r_auth_type = remote_auth_option()

    r_directory, r_repo_name = create_local_git_repo()

    r_first_file = create_local_repo_file(r_directory)

    add_files_for_commit(r_directory, r_first_file)

    commit_files(r_directory)

    r_github_name, r_remote_url = create_github_repo(r_repo_name, r_auth_type)

    r_server = add_remote_repo_url(r_directory, r_github_name, r_remote_url, r_auth_type)

    push_local_repo_to_remote(r_directory, r_server)

    pass


def main():
    start_program_flow()

if __name__ == "__main__":
    main()


#End of file