# Note: Embrace folder name has space which be deleted by hand

import os
import pandas as pd
from datetime import datetime

originalTimeZone = "UTC"
targetTimeZone = "America/Los_Angeles"

temp_all = pd.DataFrame(columns=['time', 'skin_temp'])
eda_all = pd.DataFrame(columns=['time', 'eda'])


def main():
    global temp_all
    global eda_all

    embrace_path = os.path.join(os.getcwd(), 'Data Collection', 'Embrace')
    embrace_dirs = os.listdir(embrace_path)
    embrace_csv_paths = list()

    for emdir in embrace_dirs:
        print("Folder:", emdir)
        status_path = os.path.join(embrace_path, emdir, 'UPLOAD_STATUS.txt')

        # Replace ', ' to ',' in the txt file and overwrite it
        lines = open(status_path).readlines()
        fp = open(status_path, 'w')
        for s in lines:
            fp.write(s.replace(', ', ','))
        fp.close()

        df = pd.read_csv(status_path)

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
                    embrace_csv_paths.append(csv_path)      # collect all of csv paths
        else:
            print("There is no record in the folder %s", emdir)

    # print(embrace_csv_paths)
    # combine all of temp and all of eda
    temp_all, eda_all = timestamp2datetime(embrace_csv_paths)
    collect_each_person()


def timestamp2datetime(paths):
    temp_df = pd.DataFrame(columns=['time', 'skin_temp'])
    eda_df = pd.DataFrame(columns=['time', 'eda'])

    for path in paths:
        csvfiles = os.listdir(path)

        for f in csvfiles:
            if f == 'temp.csv':
                temp_path = os.path.join(path, f)
                df = pd.read_csv(temp_path)
                # change column names
                df.columns = ['time', 'skin_temp']
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
    path = os.path.join(os.getcwd(), 'garmin')
    garmin_csv = os.listdir(path)

    # person_info includes person id and its start date and end date of garmin records
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


def collect_each_person():
    pass
    # get timestamp_16 time

    # compare garmin and embrace


if __name__ == '__main__':
    main()
    get_date_from_garmin()
