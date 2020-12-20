import json
import shutil
from configparser import ConfigParser
from pathlib import Path

import git
from py._builtin import execfile


def generate_test_config():
    """
    Helper function to generate a sample config.ini file for use in the application
    """
    repo_name = 'test_repo'
    directory = '/tmp'
    try:
        shutil.rmtree(Path(directory) / repo_name)
    except FileNotFoundError:
        pass

    config = ConfigParser()
    base_config_key = 'your_settings'
    config[base_config_key] = {}
    config[base_config_key]['github_token'] = "asdasd"
    config[base_config_key]['repo_name'] = repo_name
    config[base_config_key]['commit_file'] = "touched"
    config[base_config_key]['first_commit_msg'] = "Initial commit"
    config[base_config_key]['github_name'] = "test"
    config[base_config_key]['directory'] = directory
    config[base_config_key]['cmd'] = 'touch another_file'

    config_file = 'config.ini'
    with open(config_file, 'w') as fh:
        config.write(fh)


# The config file must be generated before the application is loaded to ensure the data
# is loaded by the application
generate_test_config()
execfile('../automate_git.py')


def mock_json_loads(response_output):
    """
    Mocking function for json.loads(), returns a basic dictionary representing the data
    returned from github.

    :param str response_output: String output that is passed to json.loads(), is ignored
    in this case
    :return: Dictionary containing the bear minimum github response
    """
    return [{'name': 'test_repo', 'html_url': 'http://github.com/fake_repo'}]


def test_program_flow(monkeypatch):

    # Apply the mocking on the json.loads() method
    monkeypatch.setattr(json, 'loads', mock_json_loads)

    # Run the main application flow
    start_program_flow()

    # Get a path object for the repo defined in the config and create a git repo object
    # for further testing
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
    # head_commit = git_repo.head.commit
    # assert head_commit.message == 'Initial commit\n'
    # assert len(head_commit.parents) == 0
