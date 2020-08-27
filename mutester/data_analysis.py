import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from typing import List

import pandas as pd

from mutester.data_crawler import DataCrawler


class DataAnalysis:
    def __init__(self, base_repository_path: str, virtual_environment_path: str, timeout=0):
        self.base_repository_path = Path(base_repository_path)
        self.virtual_environment_path = Path(virtual_environment_path)
        self.executions = pd.DataFrame()
        self.mutants = pd.DataFrame()
        self.timeout = timeout

    def collect_data(self, mutant_ids: List[int]):
        with tempfile.TemporaryDirectory() as temporary_directory:
            subprocess.call('cp ' + self.base_repository_path.absolute() + ' ' + temporary_directory + ' -r',shell=True)
            subprocess.call(
                '. ' + (self.virtual_environment_path / Path('bin/activate')).absolute()  + ' && virtualenv-clone '
                + self.virtual_environment_path.absolute() + ' ' + temporary_directory + '/venv/',
                shell=True)
            logging.info('Temporary directory now contains:')
            logging.info(os.listdir(temporary_directory))

            # Prepare mutmut
            exit_call = subprocess.call(
                'cd ' + temporary_directory + '&& . '
                + (self.virtual_environment_path / Path('bin/activate')).absolute()
                + ' && pip install pytest pytest-timeout pytest-json && pip install -e . '
                + ' && mutmut update-cache', shell=True)
            if exit_call != 0:
                logging.warning('Nonzero exit code for mutmut update-cache')

            logging.info(os.listdir(temporary_directory))
            data_crawler = DataCrawler(temporary_directory, Path(temporary_directory) / Path('venv'), timeout=self.timeout)

            for mutant_id in mutant_ids:
                try:
                    if data_crawler.checkout_mutant(mutant_id):
                        [mutant, executions] = data_crawler.analyze_mutant(mutant_id)
                        new_tests = pd.DataFrame(map(lambda execution: execution.__dict__, executions))
                        self.executions = self.executions.append(new_tests, ignore_index=True)
                        self.mutants = self.mutants.append(mutant.__dict__, ignore_index=True)
                    else:
                        logging.error('Skipping mutant %i due to checkout error', mutant_id)
                except KeyboardInterrupt:
                    return
                except:  # noqa: E722
                    logging.error('Thrown error for mutant %i, resetting environment', mutant_id)
                    subprocess.call('cd ' + temporary_directory + ' && git checkout .')
                    logging.error(sys.exc_info()[0])
                    return True  # Supress the error, as we want to keep our temporary directory
