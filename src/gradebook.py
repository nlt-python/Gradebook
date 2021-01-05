'''
Objective:  Calculate student grades

Using pandas, this script will load an .xlsx file containing student scores into
a dataframe, filter and clean the dataframe, add new columns of categorical point
totals and use a point total and weights-based system to assign letter grades.
'''

import pandas as pd


# File path for the merged xlsx file
merged_xlsx = "../data/merged_scores.xlsx"

# Load the merged xlsx file into a pandas dataframe
df = pd.read_excel(merged_xlsx, header=0, index_col=0)

# The of number homework, quiz, laboratory or discussion assignments. This will dictate
# the maximum number of points issued in the class.
num_chaps = 6

# NB: The number of exams will be different


def points_and_weights(df):
    '''Create new columns of point totals and weighted totals in a pandas dataframe

    Keyword arguments:
    df -- pandas dataframe

    This function takes a pandas dataframe of student scores and calculates the point
    total for each category of assignments in new columns.

    The categorical point totals are combined into a total point column which is used
    to calculate a final score according to the points-based grading system whereby a
    "Final Score (%)", is calculated as the ratio of the points accrued by the student
    and the total possible points, max_points, excluding the extra credit.

    The categorical point totals are also used to calculate a weights-based total. A
    dictionary, weights, is created where the weight of each category of assignments
    is calculated according to a percentage of the max_points.
    '''

    # Point distribution for each assignment type
    pts_distr = {'Qzs': 5.0, 'Labs': 5.0, 'Discs': 2.0, 'HMWKs': 5.0,
                 'MidT #1': 150.0, 'MidT #2': 150.0, 'Cumulative': 100,
                 'XCs': 2.0}

    # Calculate the maximum number of points for each category of assignments
    # The keys in this dictionary are identical to the keys in new_cols, but
    # their values are different.
    max_dict = {}
    for key, val in pts_distr.items():
        if ('MidT' in key) | (key == 'Cumulative'):
            max_dict[f'TTL {key}'] = val
        else:
            max_dict[f'TTL {key}'] = 6 * val

    # Calculate the maximum number of points a student may accrue in the class
    # minus the extra credit
    max_pts = 0
    for k, v in max_dict.items():
        if 'XCs' not in k:
            max_pts += v

    # The cumulative exam is treated separate from the midterms. Each midterm score
    # consists of a multiple choice component and a short answer component.
    new_cols = {'TTL Qzs': r'Qz', 'TTL Labs': r'Lab',
                'TTL Discs': r'Disc', 'TTL HMWKs': r'HMWK',
                'TTL MidT #1': r'MidT #1', 'TTL MidT #2': r'MidT #2',
                'TTL Cumulative': r'Cumulative',
                'TTL XCs': r'XC'}

    # Use regex to sum the student scores for each category of assignments.
    for k, v in new_cols.items():
        df[k] = df.filter(regex=v, axis=1).sum(axis=1)

    # Use regex to obtain the total points for each student
    df['TTL Points'] = df.filter(regex=r'TTL', axis=1).sum(axis=1)

    # Calculate the final score according to a points-based system
    df['Final Score (%)'] = round((df["TTL Points"] / max_pts), 4)

    # Create weights for each assignment category.
    # Weights for the exams are divided by 3 so that each exam will have the same weight
    # even though the cumulative exam is worth 50 points less than Midterms #1 and #2.
    weights = {}
    for category, points in max_dict.items():
        if ('MidT' in category) | ('Cumulative' in category):
            weights[category] = round(400 / max_pts / 3, 6)

        else:
            weights[category] = round(points / max_pts, 6)

    df['Weighted Score (%)'] = 0
    for category in new_cols:
        df['Weighted Score (%)'] += round((df[category] /
                                           max_dict[category]) * weights[category], 4)

    return df


def mapping_grades(final_percent):

    letter_dict = {0.88: "A", 0.77: "B", 0.66: "C", 0.55: "D", 0: "F"}

    for percent, letter in letter_dict.items():
        if final_percent >= percent:
            return letter

    return df


if __name__ == "__main__":

    # Uncomment these lines if using points grading scheme
    final_df = points_and_weights(df)
    final_df['Points Grade'] = final_df["Final Score (%)"].map(mapping_grades)
    final_df['Weights Grade'] = final_df["Weighted Score (%)"].map(
        mapping_grades)
    print(final_df)

    final_df.to_excel('../data/final_grades.xlsx')
