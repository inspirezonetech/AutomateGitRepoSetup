import json
import shutil
from configparser import ConfigParser
from pathlib import Path

import git
from py._builtin import execfile

CONFIG_FILE = 'config.ini'
BASE_CONFIG_KEY = 'your_settings'


def generate_test_config():
    repo_name = 'test_repo'
    directory = '/tmp'
    try:
        shutil.rmtree(Path(directory) / repo_name)
    except FileNotFoundError:
        pass

    config = ConfigParser()
    config[BASE_CONFIG_KEY] = {}
    config[BASE_CONFIG_KEY]['github_token'] = "asdasd"
    config[BASE_CONFIG_KEY]['repo_name'] = repo_name
    config[BASE_CONFIG_KEY]['commit_file'] = "touched"
    config[BASE_CONFIG_KEY]['first_commit_msg'] = "Initial commit"
    config[BASE_CONFIG_KEY]['github_name'] = "test"
    config[BASE_CONFIG_KEY]['directory'] = directory
    config[BASE_CONFIG_KEY]['cmd'] = 'touch another_file'
    with open(CONFIG_FILE, 'w') as fh:
        config.write(fh)
    return config


generate_test_config()

execfile('../automate-git.py')


def mock_json_loads(response_output):
    return [{'name': 'test_repo', 'html_url': 'http://github.com/fake_repo'}]


def test_program_flow(monkeypatch):
    monkeypatch.setattr(json, 'loads', mock_json_loads)
    start_program_flow()
    repo = Path('/tmp/test_repo')
    git_repo = git.Repo(repo)

    # Check the local repo folder exists
    assert repo.exists()

    # Check the file specified exists
    commited_file = repo / 'touched'
    assert commited_file.exists()

    # Check the command specified ran
    another_file = repo / 'another_file'
    assert another_file.exists()

    # Check the repo folder is a git repo
    assert Path(git_repo.git_dir).stem == ".git"

    # Get the commit and check it is the first commit with the message specified
    head_commit = git_repo.head.commit
    assert head_commit.message == 'Initial commit\n'
    assert len(head_commit.parents) == 0
