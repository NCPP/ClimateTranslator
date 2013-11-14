
from ncpp.util.data_scanner.query import DataQuery
from ncpp.constants import DATASETS_DB

dataQuery = DataQuery(db_path=DATASETS_DB)

dictionaries = dataQuery.get_package()
print dictionaries