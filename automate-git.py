#Init a local git repo, create remote repo using github API and push local to remote. prompts for user input

import subprocess
import json
from pathlib import Path


#--------------- local set up ---------------#

def create_local_git_repo():
    
    #ask for repo directory
    global directory #TODO avoid use of global
    directory = input("Enter repo directory path: ")

    #create directory if it doesn't exist
    check_dir = Path(directory)
    if check_dir.exists():
        print("Directory exists. Skip create directory")
    else:
        subprocess.run(["mkdir", directory])

    #ask for repo name
    global repo_name #TODO avoid use of global
    repo_name = input("Enter repo name: ") 

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


def create_local_repo_file():

    #ask for file name
    global first_file #TODO avoid use of global
    first_file = input("Enter name of first file to commit: ")

    #create file if it doesn't exist
    check_file = Path(first_file)
    if check_file.exists():
        print("File already exists. Skip create file") 
    else:
        subprocess.run(["touch", first_file], cwd=directory)
    pass


def add_files_for_commit():

    #stage file created
    subprocess.run(["git", "add", first_file], cwd=directory)
    pass

def commit_files():

    #enter commit message
    msg = input("Enter commit message: ")

    #commit file
    subprocess.run(["git", "commit", "-m", msg], cwd=directory)


    pass


#--------------- remote setup ---------------#

def create_github_repo():

    #ask for user github account name
    global github_name #TODO avoid use of global
    github_name  = input("Enter your github user name: ")

    #generate data for request, set repo to private
    repo_config = '{"name": "%s", "private": "true"}' %repo_name

    response = subprocess.run(["curl", "--user", github_name, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    #confirm repo now exists under user
    response = subprocess.run(["curl", "--user", github_name, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)
    
    #convert from completed process for easier parsing
    response_json = json.loads(response.stdout.decode("utf-8"))
    print("%d repos by user" %len(response_json))

    #confirm repo is created and extract url
    for repo_id in range(len(response_json)):        
        remote_name = response_json[repo_id]['name']
        global remote_url #TODO avoid use of global
        remote_url = response_json[repo_id]['html_url'] 
        # print(remote_name) 
        # print(remote_url) 
    
        if(remote_name == repo_name):
            print("Repo now created on github")
            break
    pass




#--------------- link local and remote ---------------#

def add_remote_repo_url():

    #url for repo
    global server #TODO avoid use of global
    server = remote_url + ".git"
    print("server: %s" %server)

    #add as origin
    subprocess.run(["git", "remote", "add", "origin", server], cwd=directory)
    pass


def push_local_repo_to_remote():

    #insert username to origin url
    push_url = server.replace("//", "//%s@" %github_name)
    print("repo link: %s" %push_url)

    #push to server
    subprocess.run(["git", "push", "-u", push_url, "master"], cwd=directory)
    pass
    



def start_program_flow():
    
    print("------ Start ------")
    create_local_git_repo()
    create_local_repo_file()
    add_files_for_commit()
    commit_files()
    create_github_repo()
    add_remote_repo_url()
    push_local_repo_to_remote()

def main():
    start_program_flow()

if __name__ == "__main__":
    main()


#End of file