import csv
import logging

logger = logging.getLogger(__name__)


def get_year_wage(wage, wage_unit):
    """ Calculate a yearly wage """
    old_wage = int(float(wage))
    try:
        wage_unit = wage_unit.lower()
        if wage_unit == 'hour':
            cleaned_wage = old_wage * 40 * 52
        elif wage_unit == 'month':
            cleaned_wage = old_wage * 12
        elif wage_unit == 'week':
            cleaned_wage = old_wage * 52
        elif wage_unit == 'bi-weekly':
            cleaned_wage = old_wage * 26
        else:
            cleaned_wage = old_wage
    except Exception as e:
        cleaned_wage = old_wage
        logger.info("While cleaning wage for {0} error happened: {1}".format(wage, e))

    return cleaned_wage


def clean_raw_file(file_name):
    """ From the raw CSV file, create a clean CSV file """
    # You many need to clean or normalize some of your date in your CSV file before you import it to Elasticsearch
    # Wage field is just an example. All wage data should be yearly

    logger.info("Start cleaning csv file {}".format(clean_raw_file))

    clean_file = file_name.replace('.csv', '_clean_file.csv')

    with open(file_name) as raw_file, open(clean_file, mode='w') as output_file:

        csv_reader = csv.DictReader(raw_file)

        # write the headers in the output/clean file first
        writer = csv.writer(output_file)
        writer.writerow(csv_reader.fieldnames)

        csvwriter = csv.DictWriter(output_file, fieldnames=csv_reader.fieldnames)

        for row in csv_reader:
            print(row)

            if row['WAGE_RATE']:
                wage = get_year_wage(row['WAGE_RATE'], row['WAGE_UNIT'])
                row['WAGE_RATE'] = wage

            # You can clean more fields here
            #

            # Cleaned/modified row is being written in the clean file
            csvwriter.writerow(row)
        logger.info("Finished cleaning csv file {}".format(clean_raw_file))

    return clean_file





