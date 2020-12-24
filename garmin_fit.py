# Step1 : Delete all .DS_store iteratively for each subfolder: https://jonbellah.com/articles/recursively-remove-ds-store/
# find . -name '.DS_Store' -type f -delete
# FitSDK: e

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import fitparse
import datetime
import sys
import pytz
import csv
import pandas as pd

folders = ['01-09-TR1', '10-20-TR2', '21-30-TR3']
# folders = ['01-09-TR1']
person = dict()

OUTPUT_TIMEZONE = pytz.timezone('US/Pacific')
INPUT_TIMEZONE = pytz.UTC

allowed_fields = ['timestamp_16', 'heart_rate']
required_fields = ['timestamp_16','heart_rate']

def main():

    for folder in folders:
        # returns a list containing the names of the entries in the directory given by path
        path = os.path.join(os.getcwd(), 'Data Collection', folder)
        person_dirs = os.listdir(path)                                     # dirs --> ['04-112520-245pm-JJ Kim']

        for psdir in person_dirs:
            person = dict()
            person[psdir.split('-')[-1]] = psdir.split('-')[0:3]           # print person --> {'Hannah Flynn': ['08', '112720', '124pm']}

            # Obtain .fit files
            garmincon_path = os.path.join(path, psdir, "Garmin Connect")   # garmincon_path --> ./Garmin Connect
            dirs = os.listdir(garmincon_path)                              # print dirs_temp --> ['2020-11-27-124pm']
            garmin_folder_path = os.path.join(garmincon_path, dirs[0])     # only one dir in dirs --> dirs[0]
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

            integrate_to_person(person, garmin_folder_path)



def write_fitfile_to_csv(fitfile, output_folder, output_file):
    messages = fitfile.messages

    #messages[0].fields[1] --> time_created: 2020-11-27 08:00:00
    if messages[0].fields[1].name != 'time_created':
        print('wrong input')
        sys.exit(1)
    else:
        timestamp = (messages[0].fields[1].value - datetime.datetime(1989, 12, 31, 0, 0)).total_seconds()

    data = []
    for m in messages:
        count = 0
        skip = True

        if not hasattr(m, 'fields'):
            continue
        fields = m.fields
        mdata = dict()

        # e.g. [<FieldData: timestamp_16: 30584 [s], def num: 26, type: uint16 (uint16), raw value: 30584>, <FieldData: heart_rate: 0 [bpm], def num: 27, type: uint8 (uint8), raw value: 0>]
        # make sure fields only two elements(count=2): timestamp_16 and heart_rate
        for f in fields:
            if f.name == 'timestamp_16':
                count+=1
            if f.name == 'heart_rate':
                count+=1

        if count == 2:
            for field in fields:
                if field.name in allowed_fields:
                    if field.name == 'timestamp_16':
                        last_timestamp_16 = field.value

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


def integrate_to_person(personRecord, csvdirName):
    li = []
    if not os.path.exists(csvdirName):
        print('Error: Cannot find %s' % csvdirName)
    else:
        ts16 = list()
        heart = list()
        dic = dict()

        files = os.listdir(csvdirName)
        for file in files:
            if file[-4:].lower() == '.csv':
                df = pd.read_csv(csvdirName + '/' + file)
                li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.sort_values('timestamp_16', inplace=True, ignore_index=True)
        values = list(personRecord.values())

        time = values[0][2][0:2] + ':' + values[0][2][2:] + ':00'

        for i in range(len(frame['timestamp_16'])):
            if frame['timestamp_16'][i].split(' ')[1] >= time:
                ts16.append(frame['timestamp_16'][i])
                heart.append(frame['heart_rate'][i])

        dic['timestamp_16'] = ts16
        dic['heart_rate'] = heart

        person_df = pd.DataFrame.from_dict(dic)
        print(person_df)

        writeGarmin_name = values[0][0] + '.csv'
        writeGarmin_dir = os.path.join(os.getcwd(), 'garmin')      # need to create "garmin" folder before running the code

        writeGarmin_path = os.path.join(writeGarmin_dir, writeGarmin_name)
        person_df.to_csv(writeGarmin_path, index=False)


if __name__=='__main__':
    main()

