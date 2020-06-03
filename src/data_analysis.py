import logging
import os
from typing import List

import pandas as pd
import subprocess
import tempfile

from src.data_crawler import DataCrawler
from src.execution import Execution
from src.mutant import Mutant


class DataAnalysis:
    def __init__(self, base_repository_path: str, virtual_environment_path: str):
        self.base_repository_path = base_repository_path
        self.virtual_environment_path = virtual_environment_path
        self.executions = pd.DataFrame(columns=Execution.__annotations__)
        self.mutants = pd.DataFrame(columns=Mutant.__annotations__)

    def collect_data(self, mutant_ids: List[int]):
        with tempfile.TemporaryDirectory() as temporary_directory:
            subprocess.call('cp ' + self.base_repository_path + '/. ' + temporary_directory + ' -r', shell=True)
            logging.info('Temporary directory now contains:')
            logging.info(os.listdir(temporary_directory))

            # Prepare mutmut
            exit_call = subprocess.call('. ' + self.virtual_environment_path + '/bin/activate ' + ' && cd ' + temporary_directory +
                            ' && timeout 10 --signal=STOP python -m mutmut run', shell=True)
            if exit_call != 0:
                logging.warning('Nonzero exit code for mutmut run')

            logging.info(os.listdir(temporary_directory))
            data_crawler = DataCrawler(temporary_directory, 'repos/flask/env/')

            for mutant_id in mutant_ids:
                [mutant, executions] = data_crawler.analyze_mutant(mutant_id)
                new_tests = pd.DataFrame(map(lambda execution: execution.__dict__, executions))
                self.executions = self.executions.append(new_tests, ignore_index=True)
                self.mutants = self.mutants.append(mutant.__dict__, ignore_index=True)


