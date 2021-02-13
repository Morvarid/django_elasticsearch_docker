import csv
import time
import logging

from elasticsearch import helpers
from search.salary import es_helper

logger = logging.getLogger(__name__)


def csv_import_to_es(file_name, index_name):
    """ CSV file will be imported into the given index"""

    # For my sample file I had to define the schema/mapping for the field "wage" so I could do aggregate function on it
    # You may need to have more elaborate mapping

    mapping = """{
                    "properties": {
                        "WAGE_RATE": {
                            "type": "integer"
                            }
                        }
                    }
                }"""

    # Make a connection to Elasticsearch
    elastic_client = es_helper.es_connect()
    elastic_client.indices.create(index=index_name, ignore=400)
    elastic_client.indices.put_mapping(index=index_name, body=mapping)
    start = time.time()

    # Open the given CSV file and bulk load it into Elasticsearch
    with open(file_name, 'r') as outfile:
        reader = csv.DictReader(outfile)
        # https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.bulk
        try:
            helpers.bulk(elastic_client, reader, index=index_name, request_timeout=1500)
        except Exception as e:
            logger.error("The import to Elasticseach has been UNSUCCESSFUL due to {}".format(e))

    end = time.time()
    logger.info("File {0} has been fully imported into Elasticsearch {1} total time: {2} minute "
                .format(file_name, index_name, (end - start)//60))




