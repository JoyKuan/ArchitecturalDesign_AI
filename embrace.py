# Check first: name of Embrace folder has space which should be deleted by hand
# temp_df.time = temp_df.time.map(lambda ts: pytz.timezone(originalTimeZone).localize(datetime.utcfromtimestamp(ts / 1000)).astimezone(pytz.timezone(targetTimeZone)))
import os
import pandas as pd
from datetime import datetime, timedelta

# LA Time Zone
# originalTimeZone = "UTC"
# targetTimeZone = "America/Los_Angeles"


def main():
    embrace_path = os.path.join(os.getcwd(), 'Data Collection', 'Embrace')
    embrace_dirs = os.listdir(embrace_path)
    embrace_csv_paths = list()

    # There are three embrace folders
    for emdir in embrace_dirs:
        print("Folder:", emdir)

        # Read 'UPLOAD_STATUS.txt' to get its 3-level hierarchy relationships (also are different names of each level of folder)
        status_path = os.path.join(embrace_path, emdir, 'UPLOAD_STATUS.txt')

        # Replace ', ' to ',' in 'UPLOAD_STATUS.txt' and overwrite it
        lines = open(status_path).readlines()
        fp = open(status_path, 'w')
        for s in lines:
            fp.write(s.replace(', ', ','))
        fp.close()

        df = pd.read_csv(status_path)

        # get whole complete paths based on its hierarchy from 'UPLOAD_STATUS.txt'
        # %03d : 01 --> 010
        if len(list(df['STUDY'])) == 1:
            csv_path = os.path.join(embrace_path, emdir, str('%03d' % int(df.loc[0, 'STUDY'])),
                                    str('%03d' % int(df.loc[0, 'SITE'])), str(df.loc[0, 'SUBJECT']),
                                    str(df.loc[0, 'DEVICE']))
            embrace_csv_paths.append(csv_path)

        elif len(list(df['STUDY'])) > 1:
            for i in range(len(list(df['STUDY']))):
                csv_path = os.path.join(embrace_path, emdir, str('%03d' % int(df.loc[i, 'STUDY'])),
                                        str('%03d' % int(df.loc[i, 'SITE'])), str(df.loc[i, 'SUBJECT']),
                                        str(df.loc[i, 'DEVICE']))
                if os.path.exists(csv_path):
                    embrace_csv_paths.append(csv_path)  # collect all of csv paths
        else:
            print("There is no record in the folder %s", emdir)

    # print(embrace_csv_paths)
    # combine all of temp and all of eda
    person_info_dict = get_date_from_garmin()
    temp_all, eda_all = timestamp2datetime(embrace_csv_paths)
    collect_each_person(person_info_dict, temp_all, 'temp')
    collect_each_person(person_info_dict, eda_all, 'eda')


def timestamp2datetime(paths):
    temp_df = pd.DataFrame(columns=['time', 'temp'])
    eda_df = pd.DataFrame(columns=['time', 'eda'])

    for path in paths:
        csvfiles = os.listdir(path)

        for f in csvfiles:
            if f == 'temp.csv':
                temp_path = os.path.join(path, f)
                df = pd.read_csv(temp_path)
                # change column names
                df.columns = ['time', 'temp']
                # UTC timestamp -> formatted LA time
                df.time = df.time.map(lambda ts: datetime.fromtimestamp(ts * 1e-3))
                temp_df = temp_df.append(df, ignore_index=True)

            elif f == 'eda.csv':
                eda_path = os.path.join(path, f)
                df = pd.read_csv(eda_path)
                # change column names
                df.columns = ['time', 'eda']
                # UTC timestamp -> formatted LA time
                df.time = df.time.map(lambda ts: datetime.fromtimestamp(ts * 1e-3))
                eda_df = eda_df.append(df, ignore_index=True)

    temp_df = temp_df.sort_values('time', ignore_index=True)
    eda_df = eda_df.sort_values('time', ignore_index=True)
    return temp_df, eda_df


def get_date_from_garmin():
    # get date of each person from garmin files
    path = os.path.join(os.getcwd(), 'garmin', 'heart_rate')
    garmin_csv = os.listdir(path)

    # person_info includes person id and its date and start time and end time of garmin records
    # e.g. person_info = {'23': ['2020-12-12 14:04:00', '2020-12-12 14:50:00'], '22': ['2020-12-12 13:16:00', '2020-12-12 13:58:00']...}
    person_info = dict()
    for file in garmin_csv:
        date = list()
        # get number in the file name as key
        person_id = file.split('.')[0]
        # get start and end date of each person as values
        df = pd.read_csv(os.path.join(path, file))
        date.append(df.loc[0, 'timestamp_16'])
        date.append(df.loc[len(df.timestamp_16) - 1, 'timestamp_16'])
        person_info[person_id] = date
    return person_info


def collect_each_person(personInfo, embrace_df, kind):
    # already obtained temp and eda dataframes and date/time of each person
    for id, dati in personInfo.items():

        time, skin_values = [], []
        person = dict()
        date, test_start_time = dati[0].split(' ')[0], dati[0].split(' ')[1]

        # convert string "end of date/time" to datetime format (in order to add one minute to end time)
        end_date_time_obj = datetime.strptime(dati[1], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=1)

        # convert datetime format to string "end of date/time"
        test_end_time = str(end_date_time_obj).split(' ')[1]

        # Compare date and time between embrace and garmin
        # < test_end_time : per second to be unit of record, so about 14:10 (garmin), we get data (less than 14:11)
        for i in range(len(embrace_df['time'])):
            if str(embrace_df['time'][i]).split(' ')[0] == date:
                if test_start_time <= str(embrace_df['time'][i]).split(' ')[1] < test_end_time:
                    time.append(embrace_df['time'][i])
                    skin_values.append(embrace_df[kind][i])
        person['time'] = time
        person[kind] = skin_values
        person_df = pd.DataFrame.from_dict(person)

        writeEmbrace_dir = os.path.join(os.getcwd(), 'embrace_temp')  # need to create "garmin" folder before running the code
        # write temp and eda csv files
        if kind == 'temp':
            writeEmbrace_name = id + '_temp.csv'
            writeEmbrace_path = os.path.join(writeEmbrace_dir, writeEmbrace_name)
            person_df.to_csv(writeEmbrace_path, index=False)
            print("Finish %s person" % writeEmbrace_name)
        elif kind == 'eda':
            writeEmbrace_name = id + '_eda.csv'
            writeEmbrace_path = os.path.join(writeEmbrace_dir, writeEmbrace_name)
            person_df.to_csv(writeEmbrace_path, index=False)
            print("Finish %s person" % writeEmbrace_name)


def second2minute():
    csv_path = os.path.join(os.getcwd(), 'embrace_temp')
    csv_files = os.listdir(csv_path)

    for file in csv_files:
        dic = dict()
        datetimeOfkind, valuesOfkind = [], []
        i = 0
        kind = file.split('_')[1].split('.')[0]       # kind: eda or temp
        df = pd.read_csv(os.path.join(csv_path, file))

        while i < len(df['time']):
            sum_ = 0
            count = 0
            time = datetime.strptime(str(df['time'][i]).split('.')[0], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.strptime(df['time'][i], '%Y-%m-%d %H:%M:%S.%f')
            next_time = current_time + timedelta(minutes=1)
            next_time = datetime.strptime(str(next_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
            while current_time < next_time:
                sum_ += df[kind][i]
                i += 1
                count += 1

                if i < len(df['time']):
                    current_time = datetime.strptime(df['time'][i], '%Y-%m-%d %H:%M:%S.%f')
                elif i >= len(df['time']):
                    break
            # print('file:', file, 'i:', i, 'count:', count, 'sum:', sum)
            valuesOfkind.append(float(sum_ / count))
            datetimeOfkind.append(time)

        dic['time'] = datetimeOfkind
        dic[kind] = valuesOfkind
        dic_df = pd.DataFrame.from_dict(dic)
        print(dic_df)
        write_path = os.path.join(os.getcwd(), 'embrace', file)
        dic_df.to_csv(write_path, index=False)
        print("Finish %s convert to minutes" % file)


if __name__ == '__main__':
    main()
    second2minute()
