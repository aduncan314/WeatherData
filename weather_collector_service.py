import requests
import sys
import json

import datetime as dt

from config_Weather import WUkey


class WeatherCollectorService:
    """
    Collects data using Wunderground API"
    """

    def __init__(self, zc, start_date):
        self.current_date = dt.datetime.strptime(start_date, '%Y/%m/%d')
        self.url = self.make_url(self.current_date)
        self.zipcode = self._check_zip(zc)
        pass

    def _change_zip(self, new_zip):
        """
        Updates zipcode
        :param new_zip: new zipcode
        :return: Does not return
        """
        self.zipcode = self._check_zip(new_zip)

    def _next_day(self):
        self.current_date = self.current_date + dt.timedelta(1)
        return self.current_date.strftime('%Y/%m/%d')

    # ****************************************************************************************************
    #   Do things
    # ****************************************************************************************************

    def make_url(self, date):
        """
        Use 'place' to build API URL
        :param date: date
        :return: <string> URL
        """

        # Define the url for this call to the API
        print('zipcode is: ' + self.zipcode)
        print('date is: ' + date)
        this_call = '/history_' + date + '/q/' + self.zipcode
        url = 'http://api.wunderground.com/api/{}{}.json'.format(WUkey, this_call)
        return url

    def get_data(self):
        """
        Make API call using self.url
        :return: Parsed JSON as Dicts and Lists
        """
        now = dt.datetime.now()
        print("[{}]  Getting weather data for {} on {}".format(now, self.zipcode, self.current_date))

        my_request = requests.get(self.url)
        response = my_request.json()

        location_name = 'Boston'  # TODO: name from zipcode later
        # dictionary of daily summary conditions
        conditions = {
            'location': location_name,
            # daily conditions
            'date': str(response['history']['dailysummary'][0]['date']['year']) + '-' + str(
                response['history']['dailysummary'][0]['date']['mon']) + '-' + str(
                response['history']['dailysummary'][0]['date']['mday']),
            'maxtemp': str(response['history']['dailysummary'][0]['maxtempm']),
            'mintemp ': str(response['history']['dailysummary'][0]['mintempm']),
            'meantemp': str(response['history']['dailysummary'][0]['meantempm']),
            'maxhum': str(response['history']['dailysummary'][0]['maxhumidity']),
            'minhum': str(response['history']['dailysummary'][0]['minhumidity']),
            'precip': str(response['history']['dailysummary'][0]['precipm'])
        }

        # Creates hourly dictionary to be added to conditions
        hourly = []
        for j in range(24):
            #		print(j)
            # TODO: check date formatting
            try:
                hourly.append(
                    {
                        'time': date[:4] + '-' + date[4:6] + '-' + date[6:8] + ' '
                                + str
                                (response['history']['observations'][j]['date']['hour']) + ':'
                                + str(response['history']['observations'][j]['date']['min']) + ':00',
                        'temp': str(response['history']['observations'][j]['tempm']),
                        'hum': str(response['history']['observations'][j]['hum']),
                        'press': str(response['history']['observations'][j]['pressurem']),
                        'hprecip': str(response['history']['observations'][j]['precipm'])
                    }
                )
            except Exception as err:
                print("[Error: {}], {}".format(err, hourly[j - 1]))
        conditions['hourly'] = hourly
        return conditions

    # ****************************************************************************************************
    #   Static
    # ****************************************************************************************************

    # TODO there is a module to actually check
    @staticmethod
    def _check_zip(zipcode):
        """
        confirm zipcode could be a real zipcode and return as 0 padded string
        :param zipcode: String or Int
        :return: String,
        """
        if type(zipcode) is not int:
            zipcode = int(zipcode)
        # Check zipcode and convert to string
        if 501 <= zipcode <= 99999:
            zipcode = '%05d' % zipcode
        else:
            raise ValueError("{} is not a valid zipcode".format(zipcode))
            # print('NOT A ZIPCODE: ' + str(zipcode) + '\n Failed before API call')  # time too?
            # sys.exit(1)
        return zipcode
