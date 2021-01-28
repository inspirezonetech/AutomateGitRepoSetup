# Contributing to AutomateGitRepoSetup

All inputs are welcome!

## This repo is part of the [inspirezone.tech](https://inspirezone.tech) portfolio of projects located on our [Github page](https://github.com/inspirezonetech)

Inspirezone is an online tech blog and community that focuses on encouraging developers of all levels of experience to improve their skills through online collaboration.

Consider [joining the inspirezone community here!](https://community.inspirezone.tech/)
You don't have to join to contribute to this project. However, joining will give you a number of advantages such as:
- You can join our Github community page
- Have discussions with other members of our community
- Be part of an accountability group that will encourage you to code more
- Potentially become a project maintainer
- Get notified of other projects and activities within our community
- It's fun to improve your skills by working with others!

## Please make sure you are assigned to an [Issue](https://github.com/inspirezonetech/AutomateGitRepoSetup/issues) before submitting a pull request

Go to the [issue](https://github.com/inspirezonetech/AutomateGitRepoSetup/issues) page and either
- Request to be assigned to an existing issue
- Create your own issue and use one of the templates provided. Wait for approval and to be assigned the issue before submitting a pull request

**Note:** You can only be assigned to one issue at a time. Please clear your assigned issue before requesting to be assigned to another.

## Contributions you can make to this project

- Add a new feature
- Report a bug
- Submit a bug fix
- Help with documentation
- Discuss current state of code
- Make any suggestion for improvement

## Guidelines for adding a new feature to the script

- Please make sure you've made your intention known first in the [issues](https://github.com/inspirezonetech/AutomateGitRepoSetup/issues) section
- Outline in the relevant issue how you may go about adding this feature
- New features should be added as a separate function if possible

## Use [flake8]((https://flake8.pycqa.org/en/latest/)) linting to ensure format of code is consistent with repo

Run flake8 on your python file before submitting.

The following flake8 errors can be excluded:
- `line too long (x > x characters) flake8(E501)`

How to run flake8 lint check on your code using command line:
```
python -m pip install flake8

# runs flake8 and ignores the 3 errors
flake8 path/to/code/to/check.py --ignore E501
```

## How to submit your code - step by step guide

Please use pull requests. See the [Github docs](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests) for details on how pull requests work.

Steps to make your contribution:

### 1. Fork this repo

### 2. Clone it locally

### 3. Add this repo as the remote upstream and keep it synced by pulling from upstream
```
git remote add upstream https://github.com/inspirezonetech/AutomateGitRepoSetup.git

git pull upstream main
```

### 4. Create a new branch and checkout to the branch
```
 git checkout -b your-branch
```

### 5. Make your changes and test it works

### 6. Commit your changes
```
git commit -m "commit message describing change" 
```

### 7. Push to your Fork 
```
git push origin your-branch
```

### 8. Go to your Fork on Github and create a pull request to this repo on Github. Fill in the PR submission form.

### 9. If needed, respond to code review comments and feedback 

### 10. If all goes well, your changes will be merged. Congrats! 

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
