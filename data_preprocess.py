# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Description:  Data Preprocessor
#      if heart_rate == 0 OR heart_rate < 50 -----> 75
#      if stress level < 0 -----> 1
# -------------------------------------------------------------------------------

import os
import pandas as pd


'''
# convert multiple excel sheets to csv

excel_file = 'final.xlsx'
df = pd.read_excel(excel_file, sheet_name=None)
for key, value in df.items():
    csvfilename = key.split('_')[0]
    df[key].to_csv('final/person/%s.csv' %csvfilename, index=False)
'''


for person_id in range(1, 31):
    path = os.path.join(os.getcwd(), 'final', 'person')
    file_path = os.path.join(path, '%.2d.csv' % person_id)
    print(file_path)
    df = pd.read_csv(file_path)
    df['heart_rate'] = df['heart_rate'].apply(lambda x: 75 if x == 0 or x < 50 else x)
    df['stress_level_value'] = df['stress_level_value'].apply(lambda x: 1 if x < 0 else x)
    df.to_csv('final/preprocessor_person/%.2d.csv' % person_id, index=False)


# pre-process combine.csv
path = os.path.join(os.getcwd(), 'final', 'person', 'combine.csv')
df_combine = pd.read_csv(path)
df_combine['heart_rate'] = df_combine['heart_rate'].apply(lambda y: 75 if y == 0 or y < 50 else y)
df_combine['stress_level_value'] = df_combine['stress_level_value'].apply(lambda y: 1 if y < 0 else y)
df_combine.to_csv('final/preprocessor_person/combine.csv', index=False)


