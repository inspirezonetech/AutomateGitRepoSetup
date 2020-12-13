# AutomateGitRepoSetup

*You are welcome to contribute to this repo. See the [**CONTRIBUTING.md**](./CONTRIBUTING.md) for more info.*

![AutomateGitRepoSetup](https://inspirezone.tech/wp-content/uploads/2020/11/github-api-with-python-1024x512.png)

## Tutorial available

A full tutorial walking you through this program is detailed on the [inspirezone.tech](https://inspirezone.tech) blog post: [Github API use case: Automate git local and remote repo setup with Python](https://inspirezone.tech/automate-git-local-and-remote-repo-setup-python/). 

The repo source files have gone through major modifications since the tutorial was written. You can see the original tutorial files under the folder [blog-tutorial-original-code/](blog-tutorial-original-code/). Use the code found in this folder to follow along with the blog tutorial.

## About this repo

Automate creation of a local repo on your PC and a remote repo on Github.

One a single run of the script it will:
- Init a local repo
- Create a file in the repo 
- Commit the file
- Create a repo on Github using same name as local repo
- Get origin URL for created repo on Github
- Push local repo to Github repo

## Technologies used

- [Curl](https://curl.se/docs/manpage.html)
- [Github API](https://docs.github.com/en/free-pro-team@latest/rest)

## Setup instructions

### Step 1: Install Curl
Curl is a command line tool for transferring data using network protocols such as HTTPS. We use this tool to interact with the Github API.

For Ubuntu systems curl can be installed by running:
```
sudo apt-get install curl
```
For other systems see the [curl installation guidelines](https://curl.se/docs/install.html)

### Step 2: Setup the [config.ini](./config.ini) file

Fill in your settings before running the script. An example configuration:
```
[your_settings]

; enter your github token for authorization purposes
github_token = 0000111122223333444455556666777788889999

; directory to create the repo on your computer
directory = /pathto/yourfolder/

; name of the repo
repo_name = your_repo_name

; first committed file
commit_file = README.md

; first commit message
first_commit_msg = first commit

; your github user name
github_name = your_github_name

; optional final command to run in repo directory e.g. "code ."
cmd = code .
```

The github_token is a personal access token generated from your Github account. It allows you to authenticate to Github when using the API. Follow the [Github docs instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) on how to generate a personal access token.

### Step 3: Run the script
Run python script using
```
python automate_git.py
```


