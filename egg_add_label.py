from datetime import datetime, timedelta, date
import pandas as pd
import os
import collections


# check the last time whether or not it is the same on garmin and embrace files
def get_last_datetime():
    id_last_datetime = collections.defaultdict(list)
    file_path_embrace = os.path.join(os.getcwd(), 'embrace')
    files_embrace = os.listdir(file_path_embrace)

    for file in files_embrace:
        read_path = os.path.join(file_path_embrace, file)
        id = file.split('_')[0]

        # ======== Embrace ========
        # read either eda or temp because they have the same last datetime
        if file.split('_')[1] == 'eda.csv':
            print('file:', file)
            df_embrace = pd.read_csv(read_path)
            # get last time from embrace
            last_datetime_embrace = datetime.strptime(df_embrace.iloc[-1]['time'], '%Y-%m-%d %H:%M:%S')

            # ======== Garmin ========
            garmin_filename = id + '.csv'
            read_path_garmin = os.path.join(os.getcwd(), 'garmin', 'heart_rate', garmin_filename)
            df_garmin = pd.read_csv(read_path_garmin)
            # get last time from garmin
            last_datetime_garmin = datetime.strptime(df_garmin.iloc[-1]['timestamp_16'], '%Y-%m-%d %H:%M:%S')

            if last_datetime_embrace == last_datetime_garmin:
                id_last_datetime[id].append(last_datetime_garmin)
    return id_last_datetime


def fill_lost_time(dic_id_datetime):

    # only 28.csv has not lost any time

    for id_, datetime_ in dic_id_datetime.items():
        if id_ == '06':
            filename = id_ + '.csv'
            print('file:', filename)
            file_path_eeg = os.path.join(os.getcwd(), 'EEG', filename)
            eeg = pd.read_csv(file_path_eeg)

            # trans string to datetime
            last_datetime_eeg = datetime.strptime(eeg.iloc[-1]['Timestamp'], '%Y-%m-%d %H:%M:%S')

            print('eda last datetime:', datetime_[0])
            print('eeg last datetime:', last_datetime_eeg)

            if datetime_[0] > last_datetime_eeg:
                delta = datetime_[0] - last_datetime_eeg
                print('delta:', delta)

            expect_end_datetime_eeg = last_datetime_eeg + delta
            print('expect end datetime of eeg:', expect_end_datetime_eeg)

            # Iterating through a range of time returns every datetime
            lost_datetime_list = list()
            while last_datetime_eeg < expect_end_datetime_eeg:
                last_datetime_eeg += timedelta(minutes=1)
                lost_datetime_list.append(last_datetime_eeg)
            print(lost_datetime_list, len(lost_datetime_list))    # store a few lost time

            # get losing wave values from eeg
            row = 0
            lost_wave_values = list()
            while row < len(lost_datetime_list):
                lost_wave_values.append(list(eeg.iloc[row, 1:6]))
                row += 1

            # append datetime to beginning of list
            if len(lost_datetime_list) == len(lost_wave_values):
                for i in range(len(lost_wave_values)):
                    lost_wave_values[i].insert(0, lost_datetime_list[i])
                print(lost_wave_values)

            # append more rows to current eeg dataframe
            for idx in range(len(lost_wave_values)):
                eeg.loc[len(eeg['Timestamp'])+idx+1] = lost_wave_values[idx]

            write_path = os.path.join(os.getcwd(), 'EEG_lost_fill', filename)
            eeg.to_csv(write_path, index=False)


def eeg_add_label(eeg_df, laps_data_df, begin_time, current_date):
    combine = list()
    count = 0

    for i in range(len(laps_data_df)-1, -1, -1):

        # total building is 50
        if count == 50:
            break

        lap_num = laps_data_df.iloc[i]['laps'].split(' ')[1]
        using_time = datetime.strptime(laps_data_df.iloc[i]['using_time'], '%H:%M:%S.%f').time()
        print("using time: ", using_time)
        print("begin time: ", begin_time)
        current_time = (datetime.combine(current_date, using_time) + begin_time).time()
        print("currt time: ", current_time)

        for idx in range(len(eeg_df)):
            data_datetime = datetime.strptime(eeg_df.iloc[idx, 0], '%Y-%m-%d %H:%M:%S')
            current_datetime = datetime.combine(current_date, current_time)

            if data_datetime > current_datetime:
                print('data_datetime, index, label = ', data_datetime, idx, lap_num)
                temp = list(eeg_df.iloc[idx-1, 1:6])
                temp.append(lap_num)
                combine.append(temp)
                delta_current_time = datetime.combine(date.min, current_time) - datetime.min
                begin_time = delta_current_time
                break
        count += 1

    person_df = pd.DataFrame(combine, columns=['Theta', 'Alpha', 'BetaL', 'BetaH', 'Gamma', 'label'])
    return person_df


if __name__ == '__main__':
    # first step: fill lost time
    last_datetime_dic = get_last_datetime()
    print(last_datetime_dic)
    fill_lost_time(last_datetime_dic)

    # second step: add label
    file_path = os.path.join(os.getcwd(), 'EEG_complete')
    files = os.listdir(file_path)

    for file in files:
        readfile_path = os.path.join(file_path, file)
        df = pd.read_csv(readfile_path)

        # get the last time and date from files in EEG_complete folder
        last_time = df.iloc[len(df) - 1, 0].split(' ')[1]
        date_ = datetime.strptime(df.iloc[len(df) - 1, 0].split(' ')[0], '%Y-%m-%d').date()
        print('file:', file, 'last time:', last_time, 'date:', date_)

        # Start to handle with Time Laps data
        laps_folder = os.path.join(os.getcwd(), 'Time Laps')
        laps_file = file.split('.')[0] + '.txt'
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

        eeg_person_df = eeg_add_label(df, laps_df, start_time, date_)

        write_path = os.path.join(os.getcwd(), 'final', 'eeg_label')
        write_filename = write_path + '/' + file
        eeg_person_df.to_csv(write_filename, index=False)




