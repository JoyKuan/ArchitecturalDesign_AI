from datetime import datetime, date
import pandas as pd
import os

file_path = os.path.join(os.getcwd(), 'embrace')
files = os.listdir(file_path)


def add_label(data_df, laps_data_df, begin_time, current_date, fea):
    combine = list()
    count = 0

    for i in range(len(laps_data_df)-1, -1, -1):

        # total is 50
        if count == 50:
            break

        lap_num = laps_data_df.iloc[i]['laps'].split(' ')[1]
        using_time = datetime.strptime(laps_data_df.iloc[i]['using_time'], '%H:%M:%S.%f').time()
        print("using time: ", using_time)
        print("begin time: ", begin_time)
        current_time = (datetime.combine(current_date, using_time) + begin_time).time()
        print("currt time: ", current_time)

        for idx in range(len(data_df)):
            data_datetime = datetime.strptime(data_df.iloc[idx, 0], '%Y-%m-%d %H:%M:%S')
            print('data_datetime: ', data_datetime)
            current_datetime = datetime.combine(current_date, current_time)

            if data_datetime > current_datetime:
                print('=======:', data_datetime, idx, lap_num)
                combine.append([data_df.iloc[idx-1, 1], lap_num])
                delta_current_time = datetime.combine(date.min, current_time) - datetime.min
                begin_time = delta_current_time
                break
        count += 1

    person_df = pd.DataFrame(combine, columns=[fea, 'label'])
    return person_df


for file in files:
    print('file name: ', file)
    temp_ = file.split('_')
    col_name = temp_[1].split('.')[0]

    readfile_path = os.path.join(file_path, file)
    df = pd.read_csv(readfile_path)

    # get the last time where the value is not 0 and the date from embrace file
    for index in range(len(df) - 1, -1, -1):
        if df.iloc[index, 1] != 0:
            last_time = df.iloc[index, 0].split(' ')[1]
            date_ = datetime.strptime(df.iloc[index, 0].split(' ')[0], '%Y-%m-%d').date()
            break

    # Start to handle with Time Laps data
    laps_folder = os.path.join(os.getcwd(), 'Time Laps')
    laps_file = file[0:2] + '.txt'
    laps_file_path = os.path.join(laps_folder, laps_file)

    # get total time from Time Laps
    laps_df = pd.read_csv(laps_file_path, sep='\t', names=["laps", "using_time", "total_time"])
    res_df = laps_df.loc[laps_df['laps'] == 'Lap 50']
    total_time = res_df['total_time'].to_string(index=False)
    total_time = total_time[1:]  # handle with ' 00:40:09.130000'

    # transfer string to datetime and get start time
    last_time = datetime.strptime(last_time, '%H:%M:%S').time()
    total_time = datetime.strptime(total_time, '%H:%M:%S.%f').time()
    start_time = datetime.combine(date_, last_time) - datetime.combine(date_, total_time)

    print('last time: ', last_time)
    print('start time:', start_time)
    print('total using time:', total_time)

    garmin_person_df = add_label(df, laps_df, start_time, date_, col_name)

    write_path = os.path.join(os.getcwd(), 'final', 'embrace_label')
    write_filename = write_path + '/' + file
    garmin_person_df.to_csv(write_filename, index=False)
