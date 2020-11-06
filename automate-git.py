import subprocess
import json
from pathlib import Path
from configparser import ConfigParser

# config file contains user settings
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

# get all settings from config
auth_type = config.get('your_settings', 'auth_type')
access_token = config.get('your_settings', 'your_token')
repo_name = config.get('your_settings', 'repo_name')
first_file = config.get('your_settings', 'commit_file')
msg = config.get('your_settings', 'first_commit_msg')
github_name = config.get('your_settings', 'github_name')
pc_directory = config.get('your_settings', 'directory')
repo_directory = pc_directory + '/' + repo_name


def create_local_git_repo():

    # create directory if it doesn't exist
    check_dir = Path(pc_directory)
    if check_dir.exists():
        print("Directory exists. Skip create directory")
    else:
        subprocess.run(["mkdir", pc_directory])

    print("You selected repo %s" % repo_directory)

    # create repo folder if it doesn't exist
    check_repo = Path(repo_directory)
    if check_repo.exists():
        print("Repo already exists. Skip git init")
    else:
        subprocess.run(["mkdir", repo_directory])
        # init repo
        subprocess.run(["git", "init"], cwd=repo_directory)

    pass


def create_local_repo_file():

    file_path = repo_directory + "/" + first_file
    print(file_path)

    # create file if it doesn't exist
    check_file = Path(file_path)
    if check_file.exists():
        print("File already exists. Skip create file")
    else:
        subprocess.run(["touch", first_file], cwd=repo_directory)
    pass


def add_files_for_commit():

    # stage file created
    subprocess.run(["git", "add", first_file], cwd=repo_directory)
    pass


def commit_files():

    # commit file
    subprocess.run(["git", "commit", "-m", msg], cwd=repo_directory)

    pass


def create_github_repo():

    # generate data for request, set repo to private
    repo_config = '{"name": "%s", "private": "true"}' % repo_name

    # create repo
    if auth_type == 'token':
        header = 'Authorization: token ' + access_token
        response = subprocess.run(["curl", "--header", header, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    else:
        response = subprocess.run(["curl", "--user", github_name, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    # confirm repo now exists under user
    if auth_type == 'token':
        response = subprocess.run(["curl", "--header", header, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    else:
        response = subprocess.run(["curl", "--user", github_name, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    # convert from completed process for easier parsing
    response_json = json.loads(response.stdout.decode("utf-8"))
    print("%d repos by user" % len(response_json))

    # confirm repo is created and extract url
    for repo_id in range(len(response_json)):
        remote_name = response_json[repo_id]['name']
        remote_url = response_json[repo_id]['html_url']

        if(remote_name == repo_name):
            print("Repo now created on github")
            break
    pass
    return remote_url


def add_remote_repo_url(remote_url):

    print(remote_url)
    # url for repo
    server = remote_url + ".git"
    print("server: %s" % server)

    if auth_type == 'token':
        server = server.replace("//", "//%s:%s@" % (github_name, access_token))

    else:
        server = server.replace("//", "//%s@" % (github_name))

    print("server: %s" % server)

    # set origin
    subprocess.run(["git", "remote", "set-url", "origin", server], cwd=repo_directory)

    pass
    return server


def push_local_repo_to_remote(server):

    # insert username to origin url
    push_url = server
    print("push url: %s" % push_url)

    # push to server
    subprocess.run(["git", "push", "-u", push_url, "master"], cwd=repo_directory)
    pass


def remote_auth_option():
    print("Select authentication type to github")

    if auth_type == 'token':
        print("Using Token")
    elif auth_type == "login":
        print("Using Password")
    else:
        print("ERROR! Ivalid option for authorisation type in config.ini file")
        exit()

    pass


def start_program_flow():

    print("------ Start ------")

    remote_auth_option()

    create_local_git_repo()

    create_local_repo_file()

    add_files_for_commit()

    commit_files()

    r_remote_url = create_github_repo()

    r_server = add_remote_repo_url(r_remote_url)

    push_local_repo_to_remote(r_server)

    pass


if __name__ == "__main__":
    start_program_flow()
