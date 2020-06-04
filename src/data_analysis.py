import logging
import os
from typing import List
import time
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
        self.executions = pd.DataFrame()
        self.mutants = pd.DataFrame()

    def collect_data(self, mutant_ids: List[int]):
        with tempfile.TemporaryDirectory() as temporary_directory:
            subprocess.call('cp ' + self.base_repository_path + '/. ' + temporary_directory + ' -r', shell=True)
            logging.info('Temporary directory now contains:')
            logging.info(os.listdir(temporary_directory))

            # Prepare mutmut
            exit_call = subprocess.call('. ' + self.virtual_environment_path + '/bin/activate ' + ' && cd ' + temporary_directory +
                            ' && mutmut update-cache', shell=True)
            if exit_call != 0:
                logging.warning('Nonzero exit code for mutmut run')

            logging.info(os.listdir(temporary_directory))
            data_crawler = DataCrawler(temporary_directory, 'repos/flask/env/')

            for mutant_id in mutant_ids:
                if data_crawler.checkout_mutant(mutant_id):
                    [mutant, executions] = data_crawler.analyze_mutant(mutant_id)
                    new_tests = pd.DataFrame(map(lambda execution: execution.__dict__, executions))
                    self.executions = self.executions.append(new_tests, ignore_index=True)
                    self.mutants = self.mutants.append(mutant.__dict__, ignore_index=True)
                else:
                    logging.error('Skipping mutant %i due to checkout error', mutant_id)

    def store_data_to_disk(self, filename: str):
        mutants_and_tests = self.mutants.set_index('mutant_id').join(self.executions.set_index('mutant_id')).reset_index()
        timestring = time.strftime("%Y%m%d-%H%M%S")
        mutants_and_tests.to_pickle(timestring + '_' + filename + '.pkl')



