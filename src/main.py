import pandas as pd
import logging

from src.data_analysis import DataAnalysis
from src.execution import Execution
from src.mutant import Mutant

logging.basicConfig(level=logging.INFO)
tests = pd.DataFrame(columns=Execution.__annotations__)
mutants = pd.DataFrame(columns=Mutant.__annotations__)

data_analysis = DataAnalysis('repos/flask', 'repos/flask/env')

data_analysis.collect_data([1, 2, 3, 1234, 2000])
data_analysis.store_data_to_disk('joined_data')

print(data_analysis.executions)
