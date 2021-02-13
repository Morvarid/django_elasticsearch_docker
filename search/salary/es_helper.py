# -*- coding: utf-8 -*-
import json
import logging

from elasticsearch import Elasticsearch
from config.settings.local import ES_HOST, ES_PORT

logger = logging.getLogger(__name__)


def es_connect():
    """ Connect to Elasticsearch """
    _es = None
    _es = Elasticsearch(host=ES_HOST, port=ES_PORT)
    if _es.ping():

        logger.info("Attempt to connect to Ellasticsearch SUCCESSFUL")
    else:
        logger.info("Attempt to connect to Ellasticsearch UNSUCCESSFUL")
    return _es


def query_builder(title, city, state):
    """This function will be called from view to build the search query """

    # TODO the query body has to be in a separate json file in utils and not hard coded here
    # Also if you dont want to check city name against a full list of all cities you can use Fuzzy feature
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html#fuzzy-query-ex-request

    body = {
            "size": 0,
            "aggs": {
                "some_filter": {
                    "filter":
                        {
                            "bool": {
                                "must": [
                                    {
                                        "match": {
                                            "JOB_TITLE": {
                                                "query": title,
                                                "operator": "AND"
                                            }
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "EMPLOYER_CITY": city
                                        }
                                    },
                                 {
                                    "match_phrase": {
                                        "EMPLOYER_STATE": state
                                    }
                                }
                                ]
                            }
                        }
                    ,
                    "aggs": {
                        "percentiles_aggs": {
                            "percentiles": {
                                "field": "WAGE_RATE",
                                "percents": [
                                    25,
                                    50,
                                    75
                                ]
                            }
                        },
                        "avg_value": {
                            "avg": {
                                "field": "WAGE_RATE"
                            }
                        }
                    }
                }
            }
        }
    logger.info("The query body : {}".format(body))
    return json.dumps(body)


def search_in_es(index_name, query_body):
    """ Searching in Elasticsearch with the given query and inside the given index"""
    elastic_client = es_connect()
    try:
        res = elastic_client.search(index=index_name, body=query_body)
        return json.dumps(res)
    except Exception as e:
        logger.info("Search in index {0} for query {1} failed due to: {2}".format(index_name, query_body, e))


def parse_build_response(es_response):
    """ Parsing Elasticsearch response for the fields we need"""
    es_response = json.loads(es_response)
    logger.info("Elasticsearch returned this {}".format(es_response))

    count = es_response["aggregations"]['some_filter']['doc_count']
    mean = es_response["aggregations"]['some_filter']['avg_value']['value']
    median = es_response["aggregations"]['some_filter']['percentiles_aggs']['values']['50.0']
    percentile_25 = es_response["aggregations"]['some_filter']['percentiles_aggs']['values']['25.0']
    percentile_75 = es_response["aggregations"]['some_filter']['percentiles_aggs']['values']['75.0']

    return {
                "number of datapoints": count,
                "mean salary": round(mean, 1),
                "median salary": median,
                "25% percentile salary": percentile_25,
                "75% percentile salary": percentile_75
            }



