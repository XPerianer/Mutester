import argparse
import logging
import math
import time
from threading import Thread
from typing import List

import pandas as pd

from Mutester.mutester.data_analysis import DataAnalysis
from Mutester.mutester.data_crawler import DataCrawler


def analysis_thread(repository_path, environment_path, mutant_ids: List[int], results: List[DataAnalysis], timeout):
    data_analysis = DataAnalysis(repository_path, environment_path, timeout)
    data_analysis.collect_data(mutant_ids)
    results.append(data_analysis)
    # data_analysis.store_data_to_disk(args.filename, args.merge)


def store_data_to_disk(filename: str, merge: str, datas: List[DataAnalysis]):
    mutants_and_tests = pd.DataFrame()
    if merge != '':
        mutants_and_tests = pd.read_pickle(merge)
        print('Read in {} executions to merge from {}'.format(len(mutants_and_tests), merge))
    for data_analysis in datas:
        mutants_and_tests = mutants_and_tests.append(
            data_analysis.mutants.set_index('mutant_id').join(data_analysis.executions.set_index('mutant_id'),
                                                              lsuffix='_mutant', rsuffix='_execution').reset_index(),
            ignore_index=True,
        )

    timestring = time.strftime("%Y%m%d-%H%M%S")
    pickle_name = timestring + '_' + filename + '.pkl'
    mutants_and_tests.to_pickle(pickle_name)
    print("Wrote: {}\n".format(pickle_name))
    total_tests = len(mutants_and_tests)
    print(mutants_and_tests)
    total_failed_tests = len(mutants_and_tests[mutants_and_tests["outcome"] is False])
    print('Total number of tests: {}\n Total failed number of tests: {}'.format(total_tests, total_failed_tests))
    return pickle_name


def main():
    argument_parser = argparse.ArgumentParser(
        description='Run mutation testing with record of failed test to pandas dataframe'
    )

    argument_parser.add_argument('repository_path',
                                 help='Path to the repository to be tested')
    argument_parser.add_argument('environment_path',
                                 help='Path to the python environment to run the tests. Make sure the module is '
                                      'installed in -e mode, and that pytest, pytest-json, mutmut are available')
    argument_parser.add_argument('interval_start',
                                 help='Test to start with')
    argument_parser.add_argument('interval_end',
                                 help='Test to end with (exlusive)')
    argument_parser.add_argument('-m', '--merge',
                                 help='Add a path to the pickle file, the end result should be merged with.'
                                      'Helpful if the process was aborted, and you want to run some tests again.',
                                 default='')
    argument_parser.add_argument('--filename', action='store', default='dataframe')
    argument_parser.add_argument('-v', '--verbose', action='store_true')
    argument_parser.add_argument('-j', '--thread_count', action='store', default=1)

    args = argument_parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    timed_run_count = 3
    timed_crawler = DataCrawler(args.repository_path, args.environment_path)

    # TODO: Baseline rund only if pytest-json and pytest-timeout have been installed, which happens later
    start_time = time.time()
    for _ in range(timed_run_count):
        timed_crawler.execute_test(-1)
    test_baseline_time = math.ceil((time.time() - start_time) / timed_run_count)
    logging.info('Measured %i seconds of runtime\n Test with higher than 10 times the baseline will be killed',
                 test_baseline_time)

    thread_count = int(args.thread_count)
    threads = []
    interval_start = int(args.interval_start)
    interval_end = int(args.interval_end)
    interval_length = int((interval_end - interval_start) / thread_count)

    results = []

    for thread_number in range(thread_count - 1):
        thread_interval_start = interval_start + thread_number * interval_length
        mutant_ids = list(range(thread_interval_start, thread_interval_start + interval_length))
        threads.append(Thread(target=analysis_thread,
                              args=(args.repository_path, args.environment_path, mutant_ids, results,
                                    test_baseline_time * 10)))

    threads.append(Thread(target=analysis_thread,
                          args=(args.repository_path, args.environment_path,
                                list(range(interval_start + (thread_count - 1) * interval_length, interval_end)),
                                results, test_baseline_time * 10)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    store_data_to_disk(args.filename, args.merge, results)

    return 0


if __name__ == "__main__":
    exit(main())
