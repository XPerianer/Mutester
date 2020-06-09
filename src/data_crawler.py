import json
import logging
import subprocess
from typing import List

from git import Repo

from execution import Execution
from mutant import Mutant


class DataCrawler:
    def __init__(self, repository_path, virtual_environment):
        self.repository_path = repository_path
        self.virtual_environment = virtual_environment

    def analyze_mutant(self, mutant_id: int) -> [Mutant, List[Execution]]:
        tests_json = self.execute_test(mutant_id)
        return_value = [Mutant.from_repo(Repo(self.repository_path), mutant_id),
                        map(lambda test_json: Execution.fromJson(test_json, mutant_id), tests_json)
                        ]
        self.reset_folder()
        return return_value

    def checkout_mutant(self, mutant_id: int) -> bool:
        logging.info('Switching to Mutant %i', mutant_id)
        cmd_str = '. ' + self.virtual_environment + '/bin/activate && cd ' + self.repository_path + ' && mutmut apply ' + str(mutant_id)
        print(cmd_str)
        return_value = subprocess.call(cmd_str, shell=True)
        if return_value != 0:
            logging.error('Nonzero exit code in checkout_mutant call')
            return False
        return True

    def execute_test(self, mutant_id: int) -> json:
        logging.info('Executing tests for Mutant %i', mutant_id)
        cmd_str = '. ' + self.virtual_environment + '/bin/activate && cd ' + self.repository_path + ' && pytest -rN --timeout=60 --json=report.json'
        subprocess.call(cmd_str, shell=True)
        with open(self.repository_path + '/report.json') as json_file:
            test_data = json.load(json_file)["report"]["tests"]
            return test_data

    def reset_folder(self):
        subprocess.call('cd ' + self.repository_path + ' && git checkout .' + ' && rm report.json', shell=True)
