import pandas as pd
from datetime import datetime, timedelta
from embrace import get_date_from_garmin
import os
import collections


def revise():
    path = os.path.join(os.getcwd(), 'Selina Luo_26.11.20_12.21.44.md.pm.bp_datetime.csv')
    df = pd.read_csv(path)

    for i in range(len(df.Timestamp)):
        datetime_ = datetime.strptime(df.iloc[i, 0], '%Y-%m-%d %H:%M:%S.%f')
        df.iloc[i, 0] = datetime_ + timedelta(minutes=159)

    # write_path = os.path.join(os.getcwd(), 'output.csv')
    # df.to_csv(write_path, index=False)
    return df


def datetime2minutes():
    path = os.path.join(os.getcwd(), 'output.csv')
    df = pd.read_csv(path)

    df_waves = df.iloc[:, 81:152]
    df_waves.insert(loc=0, column='Timestamp', value=df['Timestamp'])
    df_waves = df_waves.dropna()
    df_waves = df_waves.reset_index(drop=True)
    print(df_waves)

    flag = 0
    dic_eeg = dict()
    for col in df_waves.columns:
        print('col: ', col)
        datetimeOfkind, valuesOfkind = [], []
        i = 0
        if col != 'Timestamp':
            while i < len(df_waves['Timestamp']):
                sum_ = 0
                count = 0

                current_datetime = datetime.strptime(df_waves['Timestamp'][i], '%Y-%m-%d %H:%M:%S.%f')
                print('current datetime:', current_datetime)

                date_time = datetime.strptime(str(df_waves['Timestamp'][i]).split('.')[0], '%Y-%m-%d %H:%M:%S')

                # transfer 15:43:44 to 15:43:00
                date_time_00 = date_time.strftime('%Y-%m-%d %H:%M:%S')
                date_time_00 = datetime.strptime(date_time_00[0:-2] + '00', '%Y-%m-%d %H:%M:%S')

                next_time = date_time_00 + timedelta(minutes=1)
                next_time = datetime.strptime(str(next_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
                # print('next_time:', next_time)

                while current_datetime < next_time:
                    sum_ += df_waves[col][i]
                    i += 1
                    count += 1

                    if i < len(df_waves['Timestamp']):
                        current_datetime = datetime.strptime(df_waves['Timestamp'][i], '%Y-%m-%d %H:%M:%S.%f')
                    elif i >= len(df_waves['Timestamp']):
                        break
                print('col:', col, 'i:', i, 'count:', count, 'sum:', sum_)

                valuesOfkind.append(float(sum_ / count))
                datetimeOfkind.append(date_time_00)

            if flag == 0:
                dic_eeg['Timestamp'] = datetimeOfkind
                flag = 1
            dic_eeg[col] = valuesOfkind

    df_final = pd.DataFrame(dic_eeg, columns=list(dic_eeg.keys()))
    # write_path = os.path.join(os.getcwd(), '06.csv')
    # df_final.to_csv(write_path, index=False)

    return df_final


def avg_14_channels(df):
    theta, alpha, betal, betah, gamma, datetime_eeg = [], [], [], [], [], []
    dic_avg = dict()

    for row in range(len(df['Timestamp'])):
        theta_temp, alpha_temp, betal_temp, betah_temp, gamma_temp = [], [], [], [], []

        for col in df.columns:
            if col[-5:] == 'Theta':
                theta_temp.append(df[col][row])
            elif col[-5:] == 'Alpha':
                alpha_temp.append(df[col][row])
            elif col[-5:] == 'BetaL':
                betal_temp.append(df[col][row])
            elif col[-5:] == 'BetaH':
                betah_temp.append(df[col][row])
            elif col[-5:] == 'Gamma':
                gamma_temp.append(df[col][row])

        theta.append(sum(theta_temp) / len(theta_temp))
        alpha.append(sum(alpha_temp) / len(alpha_temp))
        betal.append(sum(betal_temp) / len(betal_temp))
        betah.append(sum(betah_temp) / len(betah_temp))
        gamma.append(sum(gamma_temp) / len(gamma_temp))

        datetime_eeg.append(df['Timestamp'][row])

    dic_avg['Timestamp'] = datetime_eeg
    dic_avg['Theta'] = theta
    dic_avg['Alpha'] = alpha
    dic_avg['BetaL'] = betal
    dic_avg['BetaH'] = betah
    dic_avg['Gamma'] = gamma

    df_eeg = pd.DataFrame.from_dict(dic_avg)
    write_path = os.path.join(os.getcwd(), '06_1.csv')
    df_eeg.to_csv(write_path, index=False)
    return df_eeg


def profile_each_person(personInfo, egg_df, id):

    print('egg_df:', egg_df)
    print('personInfo:', personInfo)

    for id_, datetime_ in personInfo.items():
        if id_ == id:
            person = collections.defaultdict(list)
            test_start_time, test_end_time = datetime_[0], datetime_[1]
            test_start_time = datetime.strptime(test_start_time, '%Y-%m-%d %H:%M:%S')
            test_end_time = datetime.strptime(test_end_time, '%Y-%m-%d %H:%M:%S')
            print('test_start_time:', test_start_time, 'test_end_time:', test_end_time)

            for i in range(len(egg_df['Timestamp'])):
                if test_start_time <= egg_df['Timestamp'][i] <= test_end_time:
                    person['Timestamp'].append(egg_df['Timestamp'][i])
                    person['Theta'].append(egg_df['Theta'][i])
                    person['Alpha'].append(egg_df['Alpha'][i])
                    person['BetaL'].append(egg_df['BetaL'][i])
                    person['BetaH'].append(egg_df['BetaH'][i])
                    person['Gamma'].append(egg_df['Gamma'][i])

    person_df = pd.DataFrame.from_dict(dict(person))
    print(person_df)
    write_csvfilename = id + '.csv'
    writeEEG_path = os.path.join(os.getcwd(), 'EEG', write_csvfilename)
    person_df.to_csv(writeEEG_path, index=False)


if __name__ == '__main__':
    # new_df = revise()
    df_ = datetime2minutes()
    print(df_)
    eeg_df_avg14 = avg_14_channels(df_)
    print(eeg_df_avg14)
    person_info = get_date_from_garmin()
    print(person_info)
    profile_each_person(person_info, eeg_df_avg14, '06')





