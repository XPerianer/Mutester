# The tests in here are used to not only test the reproduciblity of the results, but also show how mutester is supposed
# to work

import subprocess
import tempfile

import mutester


def test_full_flask_run():
    with tempfile.TemporaryDirectory() as temporary_directory:
        # Prepare everything to run the tool
        cmd_str = "cd " + temporary_directory + "&& "
        # Clone flask
        cmd_str += "git clone https://github.com/pallets/flask.git . &&"
        # TODO: Check out a specific commit
        # Prepare a virtual environment we will use
        cmd_str += "python -m venv venv && . venv/bin/activate &&"
        cmd_str += "python -m pip install -e ."
        subprocess.call(cmd_str, shell=True)

        mutester.main([temporary_directory, temporary_directory + 'venv/', 1, 10, '-j 1', '-v'])
