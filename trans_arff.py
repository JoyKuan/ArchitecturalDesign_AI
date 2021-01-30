import os
import pandas as pd


def trans_scales():

    def parse_values(x):
        if x == -1 or x == -2:
            return 'dislike'
        elif x == 1 or x == 2:
            return 'like'
        else:
            return 'neutral'

    path = os.path.join(os.getcwd(), "final/preprocessor_person")
    files = os.listdir(path)

    for file in files:
        csv_file_path = os.path.join(path, file)
        df = pd.read_csv(csv_file_path)
        new_df_fea9_scale5 = df[['heart_rate', 'stress_level_value', 'eda', 'temp', 'Theta', 'Alpha', 'BetaL', 'BetaH', 'Gamma', 'Q15']]
        new_df_fea9_scale3 = new_df_fea9_scale5.iloc[:, 0:10]
        new_df_fea9_scale3['Q15'] = new_df_fea9_scale3['Q15'].apply(parse_values)

        if file == 'combine.csv':
            write_path = os.path.join(os.getcwd(), 'ML', 'input_dataset', 'general')
            scale5_write_path = os.path.join(write_path, 'scales_5', 'combine_5.csv')
            scale3_write_path = os.path.join(write_path, 'scales_3', 'combine_3.csv')
            new_df_fea9_scale5.to_csv(scale5_write_path, index=False)
            new_df_fea9_scale3.to_csv(scale3_write_path, index=False)
            create_arff(new_df_fea9_scale5, write_path, 'scales_5', file)
            create_arff(new_df_fea9_scale3, write_path, 'scales_3', file)

        else:
            write_path = os.path.join(os.getcwd(), 'ML', 'input_dataset', 'individual')
            scale5_write_path = os.path.join(write_path, 'scales_5', '%s' % file)
            scale3_write_path = os.path.join(write_path, 'scales_3', '%s' % file)
            new_df_fea9_scale5.to_csv(scale5_write_path, index=False)
            new_df_fea9_scale3.to_csv(scale3_write_path, index=False)
            create_arff(new_df_fea9_scale5, write_path, 'scales_5', file)
            create_arff(new_df_fea9_scale3, write_path, 'scales_3', file)


def create_arff(df, writepath, scale_type, filename):
    scale_folder = scale_type + '_arff'
    filename = filename.split('.')[0] + '.arff'
    output_filename = os.path.join(writepath, scale_folder, filename)
    print(output_filename)

    if scale_type == 'scales_3':
        with open(output_filename, "w") as fp:
            fp.write('''@RELATION signals\n\n@ATTRIBUTE heart_rate NUMERIC\n@ATTRIBUTE stress_level_value NUMERIC\n@ATTRIBUTE eda NUMERIC\n@ATTRIBUTE temp NUMERIC\n@ATTRIBUTE Theta NUMERIC\n@ATTRIBUTE Alpha NUMERIC\n@ATTRIBUTE BetaL NUMERIC\n@ATTRIBUTE BetaH NUMERIC\n@ATTRIBUTE Gamma NUMERIC\n@ATTRIBUTE Q15 {dislike,neutral,like}\n\n@DATA\n''')
            df.to_csv(fp, header=None, index=None)
    else:
        with open(output_filename, "w") as fp:
            fp.write('''@RELATION signals\n\n@ATTRIBUTE heart_rate NUMERIC\n@ATTRIBUTE stress_level_value NUMERIC\n@ATTRIBUTE eda NUMERIC\n@ATTRIBUTE temp NUMERIC\n@ATTRIBUTE Theta NUMERIC\n@ATTRIBUTE Alpha NUMERIC\n@ATTRIBUTE BetaL NUMERIC\n@ATTRIBUTE BetaH NUMERIC\n@ATTRIBUTE Gamma NUMERIC\n@ATTRIBUTE Q15 NUMERIC\n\n@DATA\n''')
            df.to_csv(fp, header=None, index=None)


if __name__ == '__main__':
    trans_scales()



