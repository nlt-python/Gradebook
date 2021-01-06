'''
Objective:  Extrapolate student grades

Using pandas, this script will load an .xlsx file containing student scores into
a dataframe, add new columns of categorical point totals and use a point total-
based scheme to estimate the likelihood a student can obtain a particular letter 
grade based upon the remaining points in the class. Student grades can only be 
extrapolate for a points-based grading scheme.
'''

import pandas as pd
from datetime import datetime


# File path for the merged xlsx file. Included the three scenarios in which
# students are most interested in their standing in the class.
wk2 = "../data/merged_scores_wk2.xlsx"
wk4 = "../data/merged_scores_wk4.xlsx"
wk6 = '../data/merged_scores_wk6.xlsx'

# Load the merged xlsx file into a pandas dataframe
# df = pd.read_excel(wk2, header=0, index_col=0)
# df = pd.read_excel(wk4, header=0, index_col=0)
df = pd.read_excel(wk6, header=0, index_col=0)

# Based on the number of assignments and exams, the total number of possible points
# in the class is known, max_pts. This hypotheical class is 6-weeks long.
max_pts = 502.0
max_weeks = 6

# The number of points the students can accrue up to this point is predicated on
# the number of weeks that have passed, num_weeks
# num_weeks = 2
# num_weeks = 4

# Sixth week but before taking the finals
num_weeks = 6


def predict_grades(df):
    '''Create new columns of needed points and percentages for grades in a pandas dataframe

    Keyword arguments:
    df -- pandas dataframe

    This function takes a pandas dataframe of student scores and calculates the point
    total for each category of assignments in new columns.

    The categorical point totals are combined into a current point total column which is 
    used to calculate a current score according to the points-based grading system whereby
    "Current Score (%)" is calculated as the ratio of the points accrued by the student
    and the total possible points now, pts_now.

    The amount of points each student needs to obtain a specific letter grade as the 
    course progresses is also calculated. The "Pts Needed (for a letter grade)" is calculated 
    according to a scale of 90% = A, 80% = B, 70% = C, and 60% = D. These points are also
    converted to a percentage.
    '''

    # Point distribution for each assignment type
    pts_distr = {'Qzs': 5.0, 'Labs': 5.0, 'Discs': 2.0, 'HMWKs': 5.0,
                 'MidT #1': 150.0, 'MidT #2': 150.0, 'Cumulative': 100,
                 'XCs': 2.0}

    # Calculate the maximum number of points for each category of assignments up to
    # this moment in the class, now_dict. Also, calculate the remaining points for each
    # category of assignments in the class, remaining_dict.
    # Initialize the dictionaries.
    now_dict = {}
    remaining_dict = {}

    for key, val in pts_distr.items():

        #  Add key, value pairs where keys are assignment names and values are either
        # points completed or remaining. After 2 weeks in the course, students will have
        # completed 2 weeks worth of assignments and 1 midterm.
        if num_weeks == 2:
            if key == 'MidT #1':
                now_dict[f'TTL {key}'] = val

            elif (key == 'MidT #2') | (key == 'Cumulative'):
                remaining_dict[f'TTL {key}'] = val

            else:
                now_dict[f'TTL {key}'] = num_weeks * val
                remaining_dict[f'TTL {key}'] = (max_weeks - num_weeks) * val

        # After 4 weeks, students will have completed 4 weeks worth of assignments
        # and 2 midterms. After 6 weeks, students will have completed 6 weeks worth
        # of assignments and 2 midterms.
        else:
            if (key == 'MidT #1') | (key == 'MidT #2'):
                now_dict[f'TTL {key}'] = val

            elif key == 'Cumulative':
                remaining_dict[f'TTL {key}'] = val

            else:
                now_dict[f'TTL {key}'] = num_weeks * val
                remaining_dict[f'TTL {key}'] = (max_weeks - num_weeks) * val

    # Calculate the maximum number of points a student may accrue up to this point
    # in the class and the number of points remaining, excluding the extra credit.
    # Initialize the number of points.
    pts_now, pts_remaining = 0, 0

    for k, v in now_dict.items():
        if k != 'TTL XCs':
            pts_now += v

    for k, v in remaining_dict.items():
        if k != 'TTL XCs':
            pts_remaining += v

    # Calculate the number of points each student has accrued up to this point in the
    # class. The keys in this dictionary contain unique keys found in both now_dict and
    # remaining_dict.
    student_dict = {'TTL Qzs': r'Qz', 'TTL Labs': r'Lab',
                    'TTL Discs': r'Disc', 'TTL HMWKs': r'HMWK',
                    'TTL MidT #1': r'MidT #1', 'TTL MidT #2': r'MidT #2',
                    'TTL Cumulative': r'Cumulative',
                    'TTL XCs': r'XC'}

    # Use regex to sum the student scores for each category of assignments that have
    # passed; those assignments are in now_dict.
    for k, v in student_dict.items():
        if k in now_dict:
            df[k] = df.filter(regex=v, axis=1).sum(axis=1)

    # Use regex to obtain the current points and score for each student
    df['Current Pts'] = df.filter(regex=r'TTL', axis=1).sum(axis=1)
    df['Current Score'] = round(df['Current Pts'] / pts_now, 4)

    # Keep track of the maximum number of points completed and remaining in the class
    # by adding these columns to the dataframe.
    df['Completed Pts'] = pts_now
    df['Remaining Pts'] = pts_remaining

    # Scale for the letter grades A through D in the class.
    letter_dict = {"A": 0.90, "B": 0.80, "C": 0.70, "D": 0.60}

    # Calculate the number of points (and its resepective percentage) a student will
    # need at this point in the semester to obtain a specific letter grade.
    for lett in letter_dict:
        df[f'Pts Needed ({lett})'] = (letter_dict[lett]
                                      * max_pts) - df['Current Pts']
        df[f'% Needed ({lett})'] = round(
            df[f'Pts Needed ({lett})'] / df['Remaining Pts'], 4)

        # If the number of points the students need exceeds the number of points
        # remaining or the percentage needed is greater than 1, add a placeholder '-',
        # to indicate the letter grade is not attainable.
        df[f'Pts Needed ({lett})'] = df[f'Pts Needed ({lett})'].apply(
            lambda x: x if x <= pts_remaining else '-')
        df[f'% Needed ({lett})'] = df[f'% Needed ({lett})'].apply(
            lambda x: x if x <= 1.0 else '-')

    return df


if __name__ == "__main__":

    # Execute the function to obtain current scores and projected scores
    current_df = predict_grades(df)
    print(current_df)

    # Save the completed forecasting gradebook to an .xlsx spreadsheet
    current_df.to_excel(
        f'../data/scores_{datetime.now().strftime("%Y-%m-%d_%I-%M-%p")}.xlsx')
