# automate-git.py

**Requirements**

Tested on Linux only (Debian based distros) 

Python3 must be installed. 

You must have a Github account.

Curl must be installed. Install by running:
```
 sudo apt-get install curl
```

**How to use**

Run python script using
```
python3 automate-git.py
```


**Description of program flow**

Program does the following:

- Asks user for directory to create a local repo
- Asks user for repo name
- Init the repo
- Ask user for file name
- Create a file in the repo
- Ask user for commit message
- Commit the file
- Ask for github username
- Password prompt
- Create a github repo using same name as local repo
- Get URL for created repo
- Push local to remote repo
