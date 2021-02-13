import time
import logging
import pandas as pd


logger = logging.getLogger(__name__)


# this function didn't improve the speed so I didn't use it
def convert_xls_to_csv_in_chunks(excel_file, nrows):
    """ Covert excel file to csv in chunks"""
    chunks = []
    i_chunk = 0
    csv_file_name = excel_file+'.csv'

    # The first row is the header. We have already read it, so we skip it.
    skiprows = 1
    df_header = pd.read_excel(excel_file, nrows=1)

    logger.info(" *** Start converting Excel file {} to CSV ***".format(excel_file))

    while True:
        df_chunk = pd.read_excel(excel_file, nrows=nrows, skiprows=skiprows, header=None)
        skiprows += nrows

        # When there is no data, we know we can break out of the loop.
        if not df_chunk.shape[0]:
            break
        else:
            logger.info(" ** Reading chunk number {0} with {1} Rows".format(i_chunk, df_chunk.shape[0]))
            chunks.append(df_chunk)
            i_chunk += 1

        df_chunks = pd.concat(chunks)
        # Rename the columns to concatenate the chunks with the header.
        columns = {i: col for i, col in enumerate(df_header.columns.tolist())}
        df_chunks.rename(columns=columns, inplace=True)
        df = pd.concat([df_header, df_chunks])

    logger.info(" *** Reading is Completed in chunks...")

    return csv_file_name


def convert_xls_to_csv(excel_file):
    """ Covert excel file to csv """
    logger.info("Started converting Excel file {} to CSV".format(excel_file))
    csv_file_name = excel_file.replace('.xlsx', '.csv')

    start = time.time()

    read_file = pd.read_excel(excel_file)

    read_file.to_csv(csv_file_name, index=None, header=True)

    end = time.time()

    logger.info("CSV file  {0} has been created. Total time : {1} minutes".format(csv_file_name, (end-start)//60))

    return csv_file_name

