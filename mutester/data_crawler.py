import json
import logging
import os
import subprocess
from pathlib import Path

from typing import List

from git import Repo

from mutester.execution import Execution
from mutester.mutant import Mutant


class DataCrawler:
    def __init__(self, repository_path, virtual_environment, timeout=0):
        self.repository_path = os.path.abspath(repository_path)
        self.virtual_environment = os.path.abspath(virtual_environment)
        self.timeout = timeout

    def analyze_mutant(self, mutant_id: int) -> [Mutant, List[Execution]]:
        tests_json = self.execute_test(mutant_id)
        return_value = [Mutant.from_repo(Repo(self.repository_path), mutant_id),
                        map(lambda test_json: Execution.fromJson(test_json, mutant_id, self.repository_path),
                            tests_json)
                        ]
        self.reset_folder()
        return return_value

    def checkout_mutant(self, mutant_id: int) -> bool:
        logging.info('Switching to Mutant %i', mutant_id)
        cmd_str = 'cd ' + str(Path(self.virtual_environment)) + ' &&  . bin/activate && cd ' + self.repository_path + ' && mutmut apply ' + str(
            mutant_id)
        logging.info(cmd_str)
        return_value = subprocess.call(cmd_str, shell=True)
        subprocess.call('cd ' + self.repository_path + ' && git diff', shell=True)
        if return_value != 0:
            logging.error('Nonzero exit code in checkout_mutant call')
            return False
        return True

    def execute_test(self, mutant_id: int) -> json:
        try:
            logging.info('Executing tests for Mutant %i', mutant_id)
            cmd_str = 'cd ' + self.virtual_environment + ' && . bin/activate && cd ' \
                      + self.repository_path + ' && pytest -rN --timeout=' + \
                      str(self.timeout) + ' --json=report.json > pytest_log.log'
            logging.info(cmd_str)
            subprocess.call(cmd_str, timeout=100, shell=True)
            with open(self.repository_path + '/report.json') as json_file:
                test_data = json.load(json_file)["report"]["tests"]
                return test_data
        except:  # noqa: E722
            logging.error('Executing tests for Mutant %i failed\n It will not be used in the analysis', mutant_id)
            return []

    def reset_folder(self):
        subprocess.call('cd ' + self.repository_path + ' && git checkout .' + ' && rm report.json', shell=True)
