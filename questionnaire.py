import pandas as pd
from pandas import DataFrame
import os

csv_path = os.path.join(os.getcwd(), 'MBS Thesis Experiment (Responses).xlsx')
data = pd.read_excel(csv_path)
data_750 = data.iloc[:, 22:]
data_750_list = data_750.values.tolist()   # the length of new_data_list is 30
temp, questions_of_building = [], []

# two-dim list, for each row represents each person who answers questions about 50 buildings
# total person_idx: 30
for person_idx in range(len(data_750_list)):

    questions_of_each_building = list()
    # total build_idx: 50
    for build_idx in range(len(data_750_list[person_idx])):

        # interval for every 15 questions
        if (build_idx + 1) % 15 == 0:
            temp.append(data_750_list[person_idx][build_idx])
            questions_of_each_building.append(temp)
            temp = list()
        else:
            temp.append(data_750_list[person_idx][build_idx])

    # write csv file for each person
    person_df = DataFrame(questions_of_each_building, columns=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15'])
    # print(person_df)
    write_filename = str("%02d" % (person_idx+1)) + '.csv'
    print(write_filename)
    write_path = os.path.join(os.getcwd(), 'questionnaire', write_filename)
    person_df.to_csv(write_path, index=False)
