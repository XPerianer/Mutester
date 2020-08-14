# Mutester ![Tests](https://github.com/XPerianer/CRM2020/workflows/Tests/badge.svg)

Mutester is a tool to simplify the generation of mutation testing datasets, that can be used for data analysis of software projects.

The core of it is a command line tool, that can be used to generate mutation testing data sets.

For an example of how to use it, see the Dockerfile.

It shows how to clone the popular python project flask, setup up a virtual environment that can be used to run pytest, and then calls mutester.

Mutester then mutates inside the given virtual environment, and executes the test.
In the end, a pandas dataframe is created.
For an example of what you can do with such data, see my work for the [Code Repository Mining Seminar](XPerianer/CRM20_How_does_software_break)

Call with the '-h' option for more infos:
```
usage: [-h] [-m MERGE] [--filename FILENAME] [-v] [-j THREAD_COUNT] repository_path environment_path interval_start interval_end

Run mutation testing with record of failed test to pandas dataframe

positional arguments:
  repository_path       Path to the repository to be tested
  environment_path      Path to the python environment to run the tests. Make sure the module is installed in -e mode, and that pytest, pytest-json, mutmut are available
  interval_start        Test to start with
  interval_end          Test to end with (exlusive)

optional arguments:
  -h, --help            show this help message and exit
  -m MERGE, --merge MERGE
                        Add a path to the pickle file, the end result should be merged with. Helpful if the process was aborted, and you want to run some tests again.
  --filename FILENAME
  -v, --verbose
  -j THREAD_COUNT, --thread_count THREAD_COUNT
  ```
