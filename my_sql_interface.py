import MySQLdb
from config_Weather import Wkey  # TODO: this should be elsewhere


class SQLInterface(object):
    thing = 'nothing'

    def __init__(self, db_name=False, raw_data=False):
        self.db = False
        self.db_name = db_name
        # self.insert_dict = False TODO use this for write_weather_data
        self.raw_data = raw_data

        # Check simple errors
        if not db_name:
            raise SyntaxError('No database name: use kwd db_name.')
        if not self.raw_data:
            print("WARNING: No data has been loaded in this SQLInterface instance")

    def collect_data(self):
        pass

    def insert_data(self):
        pass

    def info(self, level='name'):
        level = level.lower()
        if level == 'name':
            print("Database Name: {}".format(self.db_name))
            return self.db_name
        elif level == 'all':
            print("Database Name: {}\n All Data: {}".format(self.db_name, self.insert_dict))
            return self.db_name, self.insert_dict

    # TODO Hard coded for now. Perhaps abstract to config
    def write_weather_data(self):
        # locZip = '02215'
        # loc = 'Boston'

        update_conditions = getWeather(locZip, date)
        myDB = MySQLdb.connect('localhost', 'root', Wkey, 'Weather')
        cursor = myDB.cursor()

        # loop through items in the daily summary to add to DB
        cursor.execute('INSERT INTO daily_summary (location, date) VALUES (\'' + loc + '\', \'' + str(
            update_conditions['date']) + '\');')
        for key in update_conditions:
            if key != 'hourly' and key != 'location' and key != 'date':
                try:
                    cursor.execute('UPDATE  daily_summary SET ' + str(key) + ' = \'' + str(update_conditions[key])
                                   + '\' WHERE location = \'' + loc + '\' AND date = \'' + date + '\'')
                    myDB.commit()
                except:
                    # the following syntax is wrong! It will stay for now
                    print(
                        'FAILED for: ' + 'UPDATE  daily_summary SET ' + str(key) + ' = \'' + str(update_conditions[key])
                        + '\' WHERE location = \'' + loc + '\' AND date = \'' + date + '\'')
                    myDB.commit()
                    myDB.rollback()

        # load hourly
        update_hourly = update_conditions['hourly']
        for i in range(len(update_hourly)):
            cursor.execute('INSERT INTO hourly (location, time) VALUES (\'' + loc + '\', \'' + str(
                update_hourly[i]['time']) + '\');')
            for key2 in update_hourly[i]:
                if key2 != 'time':
                    try:
                        cursor.execute('UPDATE hourly SET ' + str(key2) + ' = \'' + str(update_hourly[i][key2])
                                       + '\' WHERE location = \'' + loc + '\' AND time = \'' + str(
                            update_hourly[i]['time']) + '\'')
                        myDB.commit()
                    except:
                        print('FAILED for: ' + str(key) + ':' + str(update_hourly[i][key]))
                        myDB.rollback()

        myDB.close()
