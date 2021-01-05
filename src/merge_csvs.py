'''
Objective:  Clean, load and combine student data from multiple sources.

Using pandas, this script will load three .csv files into three separate
dataframes, remove unnecessary columns in the individual dataframes, merge
them into a single dataframe and export the dataframe as an .xlsx file.

The .csv files are located in ../data and consist of
    * roster
    * homework and extra credit grades hosted by a third-party provider, publisher
    * quiz, lab, discussion and exam grades from a learning management system (LMS)
'''

import pandas as pd


###  Load the data in three separate dataframes  ###

# Global variables of file paths for the roster, homework scores and LMS assignment scores
roster_csv = "../data/generated_roster.csv"
hmwk_xc_scores = "../data/generated_hmwk_scores.csv"
lms_scores = "../data/generated_other_scores.csv"


def load_roster(roster_filename):
    '''Load the roster, a csv file, into a dataframe

    Keyword arguments:
    roster_filename -- string. Contains file path and name for the roster file.

    This function loads the roster information for the gradebook into a dataframe.
    It retains the student ID number, name, their academic program and e-mail
    address for posterity. For easier matching of naming schemes in the LMS and
    homework grading csv files, the names are lower-cased and only the last and first
    names are retained; middle initials and suffixes are removed.
    '''

    # Load the roster and keep all columns
    roster_df = pd.read_csv(
        roster_filename,

        # changes all strings to lowercase for simpler string comparisons later on
        converters={"Student ID": str.lower,
                    "Student Name": str.lower,
                    "Academic Program": str.lower,
                    "Preferred Email": str.lower},

        # Indexed on SID for easier merging of data frames later.
        index_col="Student ID"
    )

    # Only retain the Last Name, First Name in the student name. Omits middle
    # initials and suffixes. This is also for simpler string comparison later on.
    roster_df['Student Name'] = roster_df['Student Name'].str.extract(
        r'([a-z]+, [a-z]+)')

    return roster_df


def load_hmwk(hmwk_filename):
    '''Load the homework, a csv file, into a dataframe

    Keyword arguments:
    hmwk_filename -- string. Contains file path and name for the hmwk file.

    This function loads the grades from the homework and extra credit assignments
    administered through a third-party provider into a dataframe. Student names, 
    all lower-cased, the homework and their extra credit (XC) assignments scores
    are retained.

    The maximum points for each assignment are not designated in a separate row.
    Instead, they are listed in the title of the assignment.
    '''

    # Load the homework and extra credit assignment grades
    hmwk_df = pd.read_csv(
        hmwk_filename,

        # change student names to lowercase for simpler string comparisons later on
        converters={"Name": str.lower},

        # use only the columns listed as NOT 'E-BOOK' since no points are attributed to
        # the reading
        usecols=lambda x: "E-BOOK" not in x,

        # Indexed on student name for easier merging of dataframes later
        index_col="Name"
    )

    # Drop all columns only containing NaNs (reading assignment columns)
    hmwk_df.dropna(axis=1, how="all", inplace=True)

    # Remove extraneous wording in column headers to create more succinct headers
    hmwk_df.columns = hmwk_df.columns.str.replace(r'( \([0-9].[0-9]\))', "")
    hmwk_df.columns = hmwk_df.columns.str.replace("Chapter", "CH")
    hmwk_df.columns = hmwk_df.columns.str.replace(": Extra Credit", " XC")
    hmwk_df.columns = hmwk_df.columns.str.replace(": Required", " HMWK")

    return hmwk_df


def load_lms(lms_filename):
    '''Load the lms assignment scores, a csv file, into a dataframe

    Keyword arguments:
    lms_filename -- string. Contains file path and name for the lms file.

    This function loads the grades for all non-homework related assignments into a
    dataframe. These assignments are administered through an LMS.

    This function retains student names, all lower-cased, student ID numbers, class
    section number, exams, quizzes, labs and discussions. Homework or extra credit
    assignments are not included in this dataframe since the third-party hosting the homework
    keeps a better record of these assignment types. This dataframe only retains a record of
    the students currently enrolled in the class.
    '''

    # Load the exam, quiz, lab and discussion assignment grades
    lms_df = pd.read_csv(
        lms_filename,
        # change strings in student name and userid to lowercase for simpler string
        # comparison later on
        converters={"Name": str.lower, "Student ID Number": str.lower},

        # Indexed on student ID for easier merging of dataframes later.
        index_col="Student ID Number"
    )

    # Housecleaning of column titles.
    lms_df.columns = lms_df.columns.str.replace("Canvas Quiz", "Qz")
    lms_df.columns = lms_df.columns.str.replace("Chapter", "CH")
    lms_df.columns = lms_df.columns.str.replace("Laboratory", "Lab")

    lms_df.columns = lms_df.columns.str.replace("Midterm", "MidT")
    lms_df.columns = lms_df.columns.str.replace("Short Answer", "SAQs")
    lms_df.columns = lms_df.columns.str.replace("Multiple Choice", "MCQs")

    lms_df.columns = lms_df.columns.str.replace("Discussion Week ", "Disc #")

    return lms_df


def merge_grades(roster, exams_qzzes, hmwk):
    '''This function merges three dataframes: roster, exams scores and homework scores.

    The merged dataframe is saved as an .xlsx spreadsheet.

    Keyword arguments:
    roster      -- pandas dataframe. Contains generated roster information
    exams_qzzes -- pandas dataframe. Contains generated assignment scores
    hmwk        -- pandas dataframe. Contains generated homework & extra credit scores
    '''

    # NB: Student Name and Student both appear as columns and both contain student names.
    final = pd.merge(roster, exams_qzzes, left_index=True, right_index=True)
    final = pd.merge(final, hmwk, left_on="Student Name", right_index=True)

    # Fill any missing assignment scores, NaN with 0
    final = final.fillna(0)

    # Drop the duplicate Name column
    final.drop("Name", inplace=True, axis=1)

    final.to_excel("../data/merged_scores.xlsx", sheet_name='Sheet1')

    return final


if __name__ == "__main__":

    roster = load_roster(roster_csv)
    hmwk_xc = load_hmwk(hmwk_xc_scores)
    exams_quizzes = load_lms(lms_scores)
    merged_df = merge_grades(roster, exams_quizzes, hmwk_xc)

    # print("---------- ROSTER ----------")
    # print(roster)
    # print()
    # print("---------- HOMEWORK SCORES ----------")
    # print(hmwk_xc)
    # print()
    # print("---------- LMS SCORES ----------")
    # print(exams_quizzes)
    # print()
    # print("---------- MERGED DATAFRAME ----------")
    # print(merged_df)
