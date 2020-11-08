import subprocess
import shlex
import json
from configparser import ConfigParser
from pathlib import Path

# config file contains user settings
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

# get all settings from config file
access_token = config.get('your_settings', 'github_token')
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

    print("Creating repo: %s" % repo_directory)

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
    print("Adding file: %s" % file_path)

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
    header = 'Authorization: token ' + access_token
    response = subprocess.run(["curl", "--header", header, "--data", repo_config, "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    # confirm repo now exists under user
    response = subprocess.run(["curl", "--header", header, "--request", "GET", "https://api.github.com/user/repos"], check=True, stdout=subprocess.PIPE)

    # convert from completed process for easier parsing
    response_json = json.loads(response.stdout.decode("utf-8"))

    # confirm repo is created and extract url
    for repo_id in range(len(response_json)):
        remote_name = response_json[repo_id]['name']
        remote_url = response_json[repo_id]['html_url']

        if(remote_name == repo_name):
            print("Repo now created on github")
            break

    return remote_url


def add_remote_repo_url(remote_url):

    # url for repo
    server = remote_url + ".git"
    print("Repo URL: %s" % server)

    # add access token to url
    server = server.replace("//", "//%s:%s@" % (github_name, access_token))

    # add remote origin
    subprocess.run(["git", "remote", "add", "origin", server], cwd=repo_directory)

    return server


def push_local_repo_to_remote(server):

    push_url = server
    print("Pushing to remote...")

    # push to github repo
    subprocess.run(["git", "push", "-u", push_url, "master"], cwd=repo_directory)
    pass


def run_custom_cmd():

    # run the command listed in config file
    run_cmd = config.get('your_settings', 'cmd')
    print("Run custom command: %s" % run_cmd)

    cmd_split = shlex.split(run_cmd)
    subprocess.run(cmd_split, cwd=repo_directory)
    pass


def start_program_flow():

    print("------ Start ------")

    create_local_git_repo()

    create_local_repo_file()

    add_files_for_commit()

    commit_files()

    remote_url = create_github_repo()

    server = add_remote_repo_url(remote_url)

    push_local_repo_to_remote(server)

    run_custom_cmd()

    print("------ Done ------")

    pass


if __name__ == "__main__":
    start_program_flow()
