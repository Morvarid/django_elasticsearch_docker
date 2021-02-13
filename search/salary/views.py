import json
import logging
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings.local import salary_index_name

from search.salary.us_city_state import city_to_state_dict, us_states
from search.salary.es_helper import query_builder, search_in_es, parse_build_response
from search.salary.cleaning import clean_raw_file
from search.salary.import_to_es import csv_import_to_es
from search.salary.xls_to_csv import convert_xls_to_csv


logger = logging.getLogger(__name__)


@csrf_exempt
def search_salary(request):
    """ This function will be called by search API """

    logger.info("Received a salary request {}".format(request.method))

    if request.method == 'GET':
        try:
            request_json_body = json.loads(request.body)
            title = request_json_body['title']
            location = request_json_body['location']
            logger.info("The request has title {} and location {}".format(title, location))
        except:
            response_body = {'Error': 'Bad Request'}
            logger.info("Wrong parameters have been passed".format(request.body))
            return HttpResponse(status=400, content=json.dumps(response_body), content_type='application/json')

        if ',' in location:
            city, state = location.split(',')
        else:
            city = location
            try:
                state = city_to_state_dict[city.title()]
            except:
                response_body = {'Error': 'Did you spell the city name correctly? '
                                          'Could you use the closest metropolitan cityCould you add state name?'}
                logger.info("Wrong city name {} ".format(request.body))
                return HttpResponse(status=400, content=json.dumps(response_body), content_type='application/json')

        state_abbreviation = us_states[state.lower().strip()]

        query_body = query_builder(title=title, city=city, state=state_abbreviation)

        response = search_in_es(index_name=salary_index_name, query_body=query_body)

        response_body = parse_build_response(response)
        status = 200

    else:
        logger.info("WRONG METHOD for salary request {}".format(request.method))
        status = 405
        response_body = {'Error': 'Method Not Allowed'}

    return HttpResponse(status=status, content=json.dumps(response_body), content_type='application/json')


def excel_to_es_load(request):

    """ This function downloads the excel file and loads it into Elasticsearch """

    signed_link = request.GET.get('link')
    logger.info("Received a request to import excel file into Elasticsearch for link {}".format(signed_link))

    excel_file = signed_link.rsplit('/', 1)[-1]
    if signed_link is not None:
        response = requests.get(signed_link)
        try:
            open(excel_file, 'wb').write(response.content)

        except Exception as e:
            logger.error("Was NOT able to download the excel file from the signed link because {}".format(e))

    csv_file = convert_xls_to_csv(excel_file)
    clean_csv_file = clean_raw_file(csv_file)
    csv_import_to_es(clean_csv_file, salary_index_name)
    response_body = {'Message': 'Your data has been imported into Elasticsearch.'}

    return HttpResponse(status=202, content=json.dumps(response_body), content_type='application/json')



