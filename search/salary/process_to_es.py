import sys
# have to set the path
# sys.path.append("/path/to/the/code")

from config.settings.local import salary_index_name
from search.salary.cleaning import clean_raw_file
from search.salary.import_to_es import csv_import_to_es
from search.salary.xls_to_csv import convert_xls_to_csv


excel_file = sys.argv[1]
csv_file = convert_xls_to_csv(excel_file)
clean_csv_file = clean_raw_file(csv_file)
csv_import_to_es(clean_csv_file, salary_index_name)
