# Step1 : Delete all .DS_store iteratively for each subfolder: https://jonbellah.com/articles/recursively-remove-ds-store/
# Command line: find . -name '.DS_Store' -type f -delete
# Execute FitSDK: java -jar ./java/FitCSVTool.jar 74185739562_WELLNESS.fit

# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import fitparse
import datetime
import sys
import pytz
import csv
import pandas as pd

folders = ['01-09-TR1', '10-20-TR2', '21-30-TR3']
person = dict()

# LA Time Zone
OUTPUT_TIMEZONE = pytz.timezone('US/Pacific')
INPUT_TIMEZONE = pytz.UTC

allowed_fields = ['timestamp_16', 'heart_rate', 'stress_level_time', 'stress_level_value']
required_fields = ['timestamp_16', 'heart_rate', 'stress_level_time', 'stress_level_value']


def main():
    for folder in folders:
        # returns a list containing the names of the entries in the directory given by path
        path = os.path.join(os.getcwd(), 'Data Collection', folder)
        person_dirs = os.listdir(path)                                    # dirs --> ['04-112520-245pm-JJ Kim']

        for psdir in person_dirs:
            person = dict()
            person[psdir.split('-')[-1]] = psdir.split('-')[0:3]          # person --> {'Hannah Flynn': ['08', '112720', '124pm']}

            # Obtain .fit files
            garmincon_path = os.path.join(path, psdir, "Garmin Connect")  # garmincon_path --> ./Garmin Connect
            dirs = os.listdir(garmincon_path)                             # dirs_temp --> ['2020-11-27-124pm']
            garmin_folder_path = os.path.join(garmincon_path, dirs[0])    # only one dir in dirs --> dirs[0]
            fitfiles = os.listdir(garmin_folder_path)
            fitfiles_wellness = [file for file in fitfiles if file[-13:].lower() == '_wellness.fit']

            for file in fitfiles_wellness:
                csv_filename = file[:-4] + '.csv'
                if os.path.exists(csv_filename):
                    continue
                fitfile_path = os.path.join(garmin_folder_path, file)
                fitfile = fitparse.FitFile(fitfile_path, data_processor=fitparse.StandardUnitsDataProcessor())
                print('converting %s' % fitfile_path)
                write_fitfile_to_csv(fitfile, garmin_folder_path, csv_filename)
            print('finished conversions')

            collect_person(person, garmin_folder_path)


def write_fitfile_to_csv(fitfile, output_folder, output_file):
    messages = fitfile.messages

    # messages[0].fields[1] --> time_created: 2020-11-27 08:00:00
    if messages[0].fields[1].name != 'time_created':
        print('wrong input')
        sys.exit(1)
    else:
        timestamp = (messages[0].fields[1].value - datetime.datetime(1989, 12, 31, 0, 0)).total_seconds()  # 1989/12/31 is the special date of garmin

    data = []
    for m in messages:
        count = 0
        skip = True

        if not hasattr(m, 'fields'):
            continue
        fields = m.fields
        mdata = dict()

        '''
        one message:
        [<DataMessage: file_id (#0) -- local mesg: #0,
        fields: [serial_number: 3953386591, time_created: 2020-11-24 00:10:00, manufacturer: garmin, garmin_product: 2622, number: 168, unknown_6: None, type: monitoring_b]>, 

        m.fields:
        fields: [serial_number: 3953386591, time_created: 2020-11-24 00:10:00, manufacturer: garmin, garmin_product: 2622, number: 168, unknown_6: None, type: monitoring_b]>
        
        it is not enough to use "f.name == 'timestamp_16'" because you will meet:
        <DataMessage: monitoring (#55) -- local mesg: #6, fields: [cycles: 0.0, active_time: 60.0, active_calories: 1, timestamp_16: 64752, activity_type: generic, intensity: 2, current_activity_type_intensity: (64,)]>,
        this message also has 'timestamp_16'. But we don't need this timestamp_16
        Hence, make sure fields only two elements(count=2): timestamp_16 and heart_rate
        '''

        for f in fields:
            if f.name == 'timestamp_16':
                count += 1
            if f.name == 'heart_rate':
                count += 1
            if f.name == 'stress_level_time':
                timestamp_stress = (f.value - datetime.datetime(1989, 12, 31, 0, 0)).total_seconds()
                t_utc_stress = datetime.datetime.fromtimestamp(631065600 + timestamp_stress)
                mdata[f.name] = t_utc_stress
            if f.name == 'stress_level_value':
                mdata[f.name] = f.value

        # handle with heart rate data
        if count == 2:
            for field in fields:
                if field.name in allowed_fields:
                    if field.name == 'timestamp_16':
                        last_timestamp_16 = field.value

                        # convert timestamp_16 to datetime format
                        timestamp_16 = ((int(timestamp) & 0xffff0000) | last_timestamp_16)
                        if timestamp_16 < (int(timestamp)):
                            timestamp_16 += 0x10000

                        t_utc = datetime.datetime.fromtimestamp(631065600 + timestamp_16)
                        mdata[field.name] = t_utc
                    elif field.name == 'heart_rate':
                        mdata[field.name] = field.value

        for rf in required_fields:
            if rf in mdata:
                skip = False
                break
        if not skip:
            data.append(mdata)

    # write to csv
    writeFile = os.path.join(output_folder, output_file)
    with open(writeFile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(allowed_fields)
        for entry in data:
            writer.writerow([str(entry.get(k, '')) for k in allowed_fields])


def collect_person(personRecord, csvdirName):
    li = []
    if not os.path.exists(csvdirName):
        print('Error: Cannot find %s' % csvdirName)
    else:
        ts16, stress_ts16, heart, stress = [], [], [], []
        dic_heart, dic_stress = {}, {}

        files = os.listdir(csvdirName)
        for file in files:
            if file[-4:].lower() == '.csv':
                df = pd.read_csv(csvdirName + '/' + file)
                li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)

        heartrate_df = pd.DataFrame(frame, columns=["timestamp_16", "heart_rate"])
        stress_df = pd.DataFrame(frame, columns=["stress_level_time", "stress_level_value"])

        heartrate_df.sort_values('timestamp_16', inplace=True, ignore_index=True)
        stress_df.sort_values('stress_level_time', inplace=True, ignore_index=True)

        heartrate_df = heartrate_df.dropna(axis=0, how='any')
        stress_df = stress_df.dropna(axis=0, how='any')

        values = list(personRecord.values())
        time = values[0][2][0:2] + ':' + values[0][2][2:] + ':00'

        for i in range(len(heartrate_df['timestamp_16'])):
            if heartrate_df['timestamp_16'][i].split(' ')[1] >= time:
                ts16.append(heartrate_df['timestamp_16'][i])
                heart.append(heartrate_df['heart_rate'][i])

        for j in range(len(stress_df['stress_level_time'])):
            if stress_df['stress_level_time'][j].split(' ')[1] >= time:
                stress_ts16.append(stress_df['stress_level_time'][j])
                stress.append(stress_df['stress_level_value'][j])

        dic_heart['timestamp_16'] = ts16
        dic_heart['heart_rate'] = heart
        dic_stress['stress_level_time'] = stress_ts16
        dic_stress['stress_level_value'] = stress

        heart_person_df = pd.DataFrame.from_dict(dic_heart)
        stress_person_df = pd.DataFrame.from_dict(dic_stress)

        writeGarmin_name = values[0][0] + '.csv'

        writeGarmin_dir = os.path.join(os.getcwd(), 'garmin', 'heart_rate')  # need to create "garmin" folder before running the code
        writeGarmin_stress_dir = os.path.join(os.getcwd(), 'garmin', 'stress')

        writeGarmin_path = os.path.join(writeGarmin_dir, writeGarmin_name)
        writeGarmin_stress_path = os.path.join(writeGarmin_stress_dir, writeGarmin_name)

        heart_person_df.to_csv(writeGarmin_path, index=False)
        stress_person_df.to_csv(writeGarmin_stress_path, index=False)


if __name__ == '__main__':
    main()
