from microserviceutil.services.google_api_service import GoogleApiService


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

if __name__ == '__main__':
    values = GoogleApiService().get_range(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))