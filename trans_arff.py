import os
import pandas as pd


def trans_scales():

    def trans_three_scales(x):
        if x == -1 or x == -2:
            return -1
        elif x == 1 or x == 2:
            return 1
        else:
            return 0

    def trans_three_categories(x):
        if x == -1 or x == -2:
            return 'dislike'
        elif x == 1 or x == 2:
            return 'like'
        else:
            return 'neutral'

    def trans_five_categories(value):
        if value == -2:
            return 'strongly_dislike'
        elif value == -1:
            return 'dislike'
        elif value == 0:
            return 'neutral'
        elif value == 1:
            return 'like'
        elif value == 2:
            return 'strongly_like'

    path = os.path.join(os.getcwd(), "final/preprocessor_person")
    files = os.listdir(path)

    for file in files:
        csv_file_path = os.path.join(path, file)
        df = pd.read_csv(csv_file_path)

        # 5 numerical scales and 5 categorical scales
        fea9_scale5 = df[['heart_rate', 'stress_level_value', 'eda', 'temp', 'Theta', 'Alpha', 'BetaL', 'BetaH', 'Gamma', 'Q15']]
        fea9_categ5 = fea9_scale5.iloc[:, 0:10]
        fea9_categ5['Q15'] = fea9_categ5['Q15'].apply(trans_five_categories)

        # 3 numerical scales and 3 categorical scales
        fea9_scale3 = fea9_scale5.iloc[:, 0:10]
        fea9_scale3['Q15'] = fea9_scale3['Q15'].apply(trans_three_scales)
        fea9_categ3 = fea9_scale5.iloc[:, 0:10]
        fea9_categ3['Q15'] = fea9_categ3['Q15'].apply(trans_three_categories)

        if file == 'combine.csv':
            write_path = os.path.join(os.getcwd(), 'ML', 'input_dataset', 'general')

            # write numerical date with 5 scales and 3 scales
            scale5_write_path = os.path.join(write_path, 'numeric_5', 'combine_5.csv')
            scale3_write_path = os.path.join(write_path, 'numeric_3', 'combine_3.csv')
            fea9_scale5.to_csv(scale5_write_path, index=False)
            fea9_scale3.to_csv(scale3_write_path, index=False)

            # write categorical date with 5 scales and 3 scales
            categ5_write_path = os.path.join(write_path, 'category_5', 'combine_5.csv')
            categ3_write_path = os.path.join(write_path, 'category_3', 'combine_3.csv')
            fea9_categ5.to_csv(categ5_write_path, index=False)
            fea9_categ3.to_csv(categ3_write_path, index=False)

            # create .arff files for Weka
            create_arff(fea9_scale5, write_path, 'numeric_5', file)
            create_arff(fea9_scale3, write_path, 'numeric_3', file)
            create_arff(fea9_categ5, write_path, 'category_5', file)
            create_arff(fea9_categ3, write_path, 'category_3', file)

        else:
            write_path = os.path.join(os.getcwd(), 'ML', 'input_dataset', 'individual')

            # write numerical date with 5 scales and 3 scales
            scale5_write_path = os.path.join(write_path, 'numeric_5', '%s' % file)
            scale3_write_path = os.path.join(write_path, 'numeric_3', '%s' % file)
            fea9_scale5.to_csv(scale5_write_path, index=False)
            fea9_scale3.to_csv(scale3_write_path, index=False)

            # write categorical date with 5 scales and 3 scales
            categ5_write_path = os.path.join(write_path, 'category_5', '%s' % file)
            categ3_write_path = os.path.join(write_path, 'category_3', '%s' % file)
            fea9_categ5.to_csv(categ5_write_path, index=False)
            fea9_categ3.to_csv(categ3_write_path, index=False)

            # create .arff files for Weka
            create_arff(fea9_scale5, write_path, 'numeric_5', file)
            create_arff(fea9_scale3, write_path, 'numeric_3', file)
            create_arff(fea9_categ5, write_path, 'category_5', file)
            create_arff(fea9_categ3, write_path, 'category_3', file)


def create_arff(df, writepath, scale_type, filename):
    scale_folder = scale_type + '_arff'
    filename = filename.split('.')[0] + '.arff'
    output_filename = os.path.join(writepath, scale_folder, filename)
    print(output_filename)

    if scale_type == 'category_3':
        with open(output_filename, "w") as fp:
            fp.write('''@RELATION signals\n\n@ATTRIBUTE heart_rate NUMERIC\n@ATTRIBUTE stress_level_value NUMERIC\n@ATTRIBUTE eda NUMERIC\n@ATTRIBUTE temp NUMERIC\n@ATTRIBUTE Theta NUMERIC\n@ATTRIBUTE Alpha NUMERIC\n@ATTRIBUTE BetaL NUMERIC\n@ATTRIBUTE BetaH NUMERIC\n@ATTRIBUTE Gamma NUMERIC\n@ATTRIBUTE Q15 {dislike,neutral,like}\n\n@DATA\n''')
            df.to_csv(fp, header=None, index=None)
    elif scale_type == 'category_5':
        with open(output_filename, "w") as fp:
            fp.write('''@RELATION signals\n\n@ATTRIBUTE heart_rate NUMERIC\n@ATTRIBUTE stress_level_value NUMERIC\n@ATTRIBUTE eda NUMERIC\n@ATTRIBUTE temp NUMERIC\n@ATTRIBUTE Theta NUMERIC\n@ATTRIBUTE Alpha NUMERIC\n@ATTRIBUTE BetaL NUMERIC\n@ATTRIBUTE BetaH NUMERIC\n@ATTRIBUTE Gamma NUMERIC\n@ATTRIBUTE Q15 {strongly_dislike,dislike,neutral,like,strongly_like}\n\n@DATA\n''')
            df.to_csv(fp, header=None, index=None)
    else:
        with open(output_filename, "w") as fp:
            fp.write('''@RELATION signals\n\n@ATTRIBUTE heart_rate NUMERIC\n@ATTRIBUTE stress_level_value NUMERIC\n@ATTRIBUTE eda NUMERIC\n@ATTRIBUTE temp NUMERIC\n@ATTRIBUTE Theta NUMERIC\n@ATTRIBUTE Alpha NUMERIC\n@ATTRIBUTE BetaL NUMERIC\n@ATTRIBUTE BetaH NUMERIC\n@ATTRIBUTE Gamma NUMERIC\n@ATTRIBUTE Q15 NUMERIC\n\n@DATA\n''')
            df.to_csv(fp, header=None, index=None)


if __name__ == '__main__':
    trans_scales()



