'''
Objective:  Calculate student grades

Using pandas, this script will load three .csv files into three separate
dataframes, remove unnecessary columns in the individual dataframes, prepare
the dataframes so that they can be merged into a single dataframe where
calculations can be performed to create the final gradebook.

The .csv files are located in /data and consist of
    * roster
    * homework and extra credit grades from Cengage
    * quiz, exam, discussion, lab, Zoom and group project grades from Canvas
'''

import pandas as pd


# File path for the merged xlsx file
merged_xlsx = "data/merged_scores.xlsx"

# Load the merged xlsx file into a pandas dataframe
df = pd.read_excel(merged_xlsx, header=0, index_col=0)

# The number homework, quiz, laboratory or discussion assignment. This will dictate the
# maximum number of points issued in the class.
num_chaps = 6


def calculate_grades(df):
    '''This function takes an xlsx spread of student scores and calculates the point
    total for each category of assignments in new columns.

    The categorical point totals are combined into a total point column which is used
    to calculate a letter grade according to the points-based grading system whereby
    a "Final Score (%)", is calculated as the ratio of the points accrued by the student
    and the total possible points, max_points, excluding the extra credit.
    '''

    # Point distribution for each assignment type
    pts_distr = {'quiz': 5.0, 'lab': 5.0, 'disc': 2.0, 'hmwk': 5.0,
                 'midt1': 150.0, 'midt2': 150.0, 'cumulative': 150,
                 'xc': 2.0}

    # Use regex to sum the scores for each category of assignments
    new_cols = {'TTL Qzs': r'Qz', 'TTL Labs': r'Lab', 'TTL Discs': r'Disc',
                'TTL HMWKs': r'HMWK', 'TTL MidT #1': r'MidT #1',
                'TTL MidT #2': r'MidT #2', 'TTL Cumulative': r'Cumulative',
                'TTL XCs': r'XC', }

    for k, v in new_cols.items():
        df[k] = df.filter(regex=v, axis=1).sum(axis=1)

    # Use regex to obtain the total points for each student
    df['TTL Points'] = df.filter(regex=r'TTL', axis=1).sum(axis=1)

    # Calculate the maximum number of points a student may accrue minus the
    # extra credit
    max_points = pts_distr['midt1'] + pts_distr['midt2'] + \
        pts_distr['cumulative'] + \
        6 * (pts_distr['quiz'] + pts_distr['lab'] +
             pts_distr['disc'] + pts_distr['hmwk'])

    df['Final Score (%)'] = round((df["TTL Points"] / max_points), 4)

    return df


def weighted_grades(df):
    '''This function takes an xlsx spreadsheet of student scores and calculates the
    point total for each category of assignments in new columns.

    The categorical point totals are combined into a total point column which is used
    to calculate a letter grade according to a pseudo-weights-based grading system.

    A dictionary, weights, is created where the weight of each category of assignments
    is calculated according to a percentage of the max_points.
    '''

    # Use regex to sum the scores for each category of assignments with the exception
    # of the exams. The exams will be summed individually. Currently, the short answer
    # and multiple choice portions of each exam are listed separately.
    df['TTL Zoom'] = df.filter(regex=r'Zoom', axis=1).sum(axis=1)
    df['TTL GP'] = df.filter(regex=r'GP', axis=1).sum(axis=1)
    df['TTL Disc'] = df.filter(regex=r'Disc', axis=1).sum(axis=1)
    df['TTL Labs'] = df.filter(regex=r'At-Home', axis=1).sum(
        axis=1) + df.filter(regex=r'In-Class', axis=1).sum(axis=1)

    df['TTL HMWK'] = df.filter(regex=r'HMWK', axis=1).sum(axis=1)
    df['TTL QZ'] = df.filter(regex=r'Qz', axis=1).sum(axis=1)
    df['TTL XC'] = df.filter(regex=r'XC', axis=1).sum(axis=1)

    # Sum the exams individually
    num_exams = 3
    for n in range(1, num_exams + 1):
        df[f'TTL Exam #{n}'] = df[f'Exam #{n}: SAQs'] + df[f'Exam #{n}: MCQs']

    # Sum all the points in the class as a check; compare with point total from calculated
    # grades
    df['TTL Points'] = df.filter(
        regex=r'TTL', axis=1).sum(axis=1) + df['SLO Exam']

    # Create weights for each assignment category.
    # Weights for the exams are divided by 4 so that each exam will have the same weight
    # even though the SLO exam is worth 50 points less than Exams #1 - #3.
    max_points = 837
    category_dict = {'TTL Zoom': 15, 'TTL GP': 20, 'TTL Disc': 32,
                     'TTL Labs': 60, 'TTL HMWK': 65, 'TTL QZ': 95,
                     'TTL Exam #1': 150, 'TTL Exam #2': 150,
                     'TTL Exam #3': 150, 'SLO Exam': 100,
                     'TTL XC': 35}

    weights = {}
    for category, points in category_dict.items():
        if 'Exam' in category:
            weights[category] = round(550 / 837 / 4, 6)
        else:
            weights[category] = round(points / max_points, 6)

    # Use the weights to create the final, weighted score column
    category_lst = ['TTL Zoom', 'TTL GP', 'TTL Disc', 'TTL Labs',
                    'TTL HMWK', 'TTL QZ', 'TTL Exam #1', 'TTL Exam #2',
                    'TTL Exam #3', 'SLO Exam', 'TTL XC']

    df['Weighted Score (%)'] = 0
    for category in category_lst:
        df['Weighted Score (%)'] += round((df[category] /
                                           category_dict[category]) * weights[category], 4)

    return df


def mapping_grades(final_percent):

    letter_dict = {0.89: "A", 0.78: "B", 0.67: "C", 0.56: "D", 0: "F"}

    for percent, letter in letter_dict.items():
        if final_percent >= percent:
            return letter

    return df


if __name__ == "__main__":

    # Uncomment these lines if using points grading scheme
    final_df = calculate_grades(df)
    final_df['Grade'] = final_df["Final Score (%)"].map(mapping_grades)
    print(final_df)
    print()

    # Uncomment these lines if using weighted exams grading scheme
    # weighted_df = weighted_grades(merged_df)
    # weighted_df['Grade'] = weighted_df['Weighted Score (%)'].map(
    #     mapping_grades)
    # print(weighted_df[['Student', 'TTL Zoom', 'TTL GP', 'TTL Disc', 'TTL Labs', 'TTL HMWK',
    #                    'TTL QZ', 'TTL XC', 'TTL Exam #1', 'TTL Exam #2', 'TTL Exam #3',
    #                    'SLO Exam', 'TTL Points', 'Weighted Score (%)', 'Grade']])

    # print()
    # print()

    # weighted_df.to_excel('data/weighted_grades.xlsx')
