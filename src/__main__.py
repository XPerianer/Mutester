import argparse
import pandas as pd
import logging

from data_analysis import DataAnalysis
from execution import Execution
from mutant import Mutant

import os
import sys

argument_parser = argparse.ArgumentParser(
    description='Run mutation testing with record of failed test to pandas dataframe'
)

argument_parser.add_argument('repository_path',
                             help='Path to the repository to be tested')
argument_parser.add_argument('environment_path',
                             help='Path to the python environment to run the tests. Make sure the module is installed in -e mode, and that pytest, pytest-json, mutmut are available')
argument_parser.add_argument('interval_start',
                             help='Test to start with')
argument_parser.add_argument('interval_end',
                             help='Test to end with (exlusive)')
argument_parser.add_argument('-m', '--merge',
                             help='Add a path to the pickle file, the end result should be merged with. Helpful if the process was aborted, and you want to run some tests again.',
                             default='')
argument_parser.add_argument('--filename', action='store', default='dataframe')
argument_parser.add_argument('-v', '--verbose', action='store_true')

args = argument_parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.INFO)

tests = pd.DataFrame(columns=Execution.__annotations__)
mutants = pd.DataFrame(columns=Mutant.__annotations__)

data_analysis = DataAnalysis(args.repository_path, args.environment_path)

data_analysis.collect_data(list(range(int(args.interval_start), int(args.interval_end))))
data_analysis.store_data_to_disk(args.filename, args.merge)

