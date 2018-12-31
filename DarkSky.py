import urllib2
import json
import csv
from datetime import datetime
from collections import OrderedDict


class DarkSky(object):

    def __init__(self, latitude, longitude, data_file_csv, data_file_json):
        self.latitude = latitude
        self.longitude = longitude
        self.data_file_csv = data_file_csv
        self.data_file_json = data_file_json
        self.key = '35ff389eaa7ff07d009ec2716c7d0f5f'
        self.url = 'https://api.darksky.net/forecast/{0}/{1},{2}'.format(self.key,
                                                                         str(self.latitude),
                                                                         str(self.longitude))

    def unix_to_local_time(self, time_unix):
        return datetime.fromtimestamp(time_unix).strftime('%Y-%m-%d %H:%M:%S')

    def get_weather_data(self):

        try:  # get response from DarkSky
            response = urllib2.urlopen(self.url)
        except urllib2.URLError as e:
            print('Unable to retrieve forecast. {0}'.format(e))
        else:  # read response
            try:
                response = json.loads(response.read())
            except ValueError:
                print("Could not decode json file.")

        if response:
            return response
        else:
            return -1

    def write_data_to_file(self, response):

        # build list to write to .csv file
        current_response = [response.get('latitude', ''),
                            response.get('longitude', ''),
                            self.unix_to_local_time(response.get('currently', '').get('time', '')),
                            response.get('currently', '').get('temperature','')]

        # get list of forecasts from response
        forecast_response = response.get('daily').get('data')

        # for each day in the list, get specific data
        for day in forecast_response:
            current_response.append(self.unix_to_local_time(day.get('time', '')))
            current_response.append(day.get('temperatureHigh', ''))
            current_response.append(self.unix_to_local_time(day.get(
                'temperatureHighTime', '')))
            current_response.append(day.get('temperatureLow', ''))
            current_response.append(self.unix_to_local_time(day.get(
                        'temperatureLowTime', '')))

        # append data to .csv file
        try:
            with open(self.data_file_csv, 'ab') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(current_response)
                fp.close()
        except IOError as e:
            print("Could not write data to file. {0}".format(e))

        # append data to ordered dict for json dump
        data = OrderedDict([('date', current_response[2]),
                            ('service', 'darksky'),
                            ('latitude', current_response[0]),
                            ('longitude', current_response[1]),
                            ('temperature', current_response[3])])

        forecast = OrderedDict([])

        for day in forecast_response:
            days_data = OrderedDict([('temperatureHigh', day.get('temperatureHigh', '')),
                                    ('temperatureHighTime', self.unix_to_local_time(day.get('temperatureHighTime', ''))),
                                    ('temperatureLow', day.get('temperatureLow', '')),
                                    ('temperatureLowTime', self.unix_to_local_time(day.get('temperatureLowTime', '')))])
            forecast[self.unix_to_local_time(day.get('time', ''))] = days_data

        data['forecast'] = forecast

        try:
            with open(self.data_file_json, 'ab') as fp:
                fp.write(json.dumps(data))
                fp.close()
        except IOError as e:
            print("Could not write data to data file. {0}".format(e))









