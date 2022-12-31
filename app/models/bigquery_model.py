import os
import pandas
from pathlib import Path
from datetime import datetime
from google.cloud import bigquery
from typing import List, Set, Dict, Tuple, TypeVar, Callable

class BigQueryClient():

    def __init__(self, parameter: Dict[str, str]) -> None:
        self.project = parameter['project']
        self.dataset = parameter['dataset']
        self.table = parameter['table']
        self.if_exists = parameter['if_exists']

    def write(self, dataframe: pandas.core.frame.DataFrame) -> None:
        dataframe.to_gbq(f'{self.dataset}.{self.table}', project_id=self.project, if_exists=self.if_exists)