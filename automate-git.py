#Init a local git repo, create remote repo using github API and push local to remote. prompts for user input

import subprocess
import json
from pathlib import Path


#--------------- local set up ---------------#

def create_local_git_repo():
    
    #ask for repo directory
    directory = input("Enter repo directory path: ")

    #create directory if it doesn't exist
    check_dir = Path(directory)
    if check_dir.exists():
        print("Directory exists. Skip create directory")
    else:
        subprocess.run(["mkdir", directory])

    #ask for repo name
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
    return directory, repo_name


def create_local_repo_file(directory):

    #ask for file name
    first_file = input("Enter name of first file to commit: ")

    #create file if it doesn't exist
    check_file = Path(first_file)
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

    #enter commit message
    msg = input("Enter commit message: ")

    #commit file
    subprocess.run(["git", "commit", "-m", msg], cwd=directory)


    pass


#--------------- remote setup ---------------#

def create_github_repo(repo_name):

    #ask for user github account name
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
        remote_url = response_json[repo_id]['html_url'] 
        # print(remote_name) 
        # print(remote_url) 
    
        if(remote_name == repo_name):
            print("Repo now created on github")
            break
    pass
    return github_name, remote_url




#--------------- link local and remote ---------------#

def add_remote_repo_url(directory, remote_url):

    #url for repo
    server = remote_url + ".git"
    print("server: %s" %server)

    #add as origin
    subprocess.run(["git", "remote", "add", "origin", server], cwd=directory)
    pass
    return server


def push_local_repo_to_remote(directory, github_name, server):

    #insert username to origin url
    push_url = server.replace("//", "//%s@" %github_name)
    print("repo link: %s" %push_url)

    #push to server
    subprocess.run(["git", "push", "-u", push_url, "master"], cwd=directory)
    pass
    



def start_program_flow():
    
    print("------ Start ------")
    r_directory, r_repo_name = create_local_git_repo()
    r_first_file = create_local_repo_file(r_directory)
    add_files_for_commit(r_directory, r_first_file)
    commit_files(r_directory)
    r_github_name, r_remote_url = create_github_repo(r_repo_name)
    r_server = add_remote_repo_url(r_directory, r_remote_url)
    push_local_repo_to_remote(r_directory, r_github_name, r_server)

def main():
    start_program_flow()

if __name__ == "__main__":
    main()


#End of file