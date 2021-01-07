# Gradebook
<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_A-LetterGrade.PNG" width="500">
  </p>
&nbsp  


## Objective:

Using Python, develop a more efficient method to calculate student grades from multiple sources and extrapolate current student scores to predict grades throughout the course of the semester.
<p></p>
&nbsp  


## Background:

I have been teaching chemistry for several years and have been using a combination of Microsoft Excel, our school's Learning Management System (LMS) and a third-party program where homework assignments are administered to keep track of student grades. Every week, I take about 30 to 45 minutes to export homework grades as well as grades from our LMS in CSV form to compile into an Excel spreadsheet. I compile my own master spreadsheet to:

* ensure updated access to student grades in case the LMS is down.
* maintain an accurate record of student grades in the semester; on an almost weekly basis, the LMS fails to update some aspect of student scores from the third-party program.
* maintain a local copy of student grades from previous semesters. Our LMS maintains student records for only a few semesters.
* track students that drop the class and when. Once a student drops, their grades are erased from the LMS. I would like to retain this data for use in a future research project to identify topics early on in the semester that students tend to struggle with.

Another spreadsheet is created that extrapolate students’ current scores to give them an idea of how they need to perform as the semester progresses to obtain their desired letter grade. This spreadsheet is used to proactively identify and reach out to students on the border between two letter grades (eg., A/B, B/C or C/D). 
</p></p>
&nbsp  


## Data:

Due to the confidential nature of student information and grades, I created three sets of CSV files to reflect information obtained from:
* our school roster – **‘generated_roster.csv’**
* homework and extra credit assignment scores from a third-party program – **‘generated_hmwk_scores.csv’**
* other assignments and their scores administered through our LMS – **‘generated_other_scores.csv’**

Although the names, assignments and grades are fake, the nuances in each type of CSV file is preserved to demonstrate some of the data cleaning aspects of this project. All assignment scores are randomly generated with lower and upper limits using numpy’s *np.random.normal()*. The Python script to generate these CSV files is located in ***generate_csvs.py***. For example,

* Student names may be different in different data sources. The school roster contains student names as “Last Name, First Name” and middle initial, where applicable, whereas the LMS omits the middle initial. Students provide their own names for the third-party publisher that hosts the homework and may sometimes use their married name or revert to their birth name; this discrepancy is not addressed in this project.
* Some of the columns in the LMS CSV file may have different headers compared to the ones in the homework file, but they contain the same or similar data. Also, both the LMS and homework CSV files refer to student names as “Name” whereas the roster file uses “Student Name”.
* Rows or columns in the tables may have missing data for incomplete assignments or assignments that are not graded.
* The homework file lists an assignment’s maximum point value in the column header instead of in a different column or row (see image below). In contrast, the LMS file does not contain any information on an assignment’s maximum point.

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_HMWKscores.PNG">
  </p>
&nbsp  

### Load, Clean and Merge the Data:

The Python script to load, clean and merge the three CSV files is located in ***merge_csvs.py***. This file loads the roster, homework scores and scores from the LMS into three separate pandas dataframes. The individual dataframes were cleaned as follows before merging:

* Using *str.lower()*, string data in all files was changed to lower case for ease of comparison between the files
* Using *str.extract()*, only student first and last names were retained
* Using *.dropna()*, only graded assignments were retained. Columns containing only NaNs were dropped
* Using *str.replace()*, wordy or lengthy column headers were replaced with more succinct headers

A code snippet illustrating the first and last two bullet points is included below:

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_merge_snippet.PNG">
  </p>
&nbsp  

The dataframes were indexed on student IDs and student names and merged using pandas' *pd.merge()*. The merged dataframe was saved to an .xlsx file, **'merged_scores.xlsx'**.
<p></p>
&nbsp  


## Gradebook:

The gradebook was created from the **'merged_scores.xlsx'** spreadsheet. The final format of the gradebook data table contains all the data for a single student in a row. The columns represent each assignment score. In this project, they are quizzes, labs, discussions, homework, extra credit, midterms and a final. There is also information about each student’s name, student identification number, course section number, e-mail address and declared academic program. Calculations for categorical point totals, an overall point total and final letter grades are stored in separate columns. Categorical point totals and overall point totals and scores were calculated using a combination of the pandas filter function *.filter()* and regular expressions.

Letter grades were mapped onto the numerical scores from both a points-based and weights-based system according to the scale 

* greater than or equal to 0.90 = A
* greater than or equal to 0.80 = B
* greater than or equal to 0.70 = C
* greater than or equal to 0.60 = D

The Python script to calculate scores and map letter grades is located in ***gradebook.py***.

In a points-based system, each individual assignment has a pre-determined value to the final grade. The overall grade is determined by the ratio of the student’s total points to the total possible points offered in the course. This method is easier for students to understand but is not readily amenable to adding or removing assignments during the semester since it affects the total points possible offered in the course. In a weights-based system, each category of assignments is assigned a percentage or weight to determine its impact on the students’ final grade. The overall grade is determined by the ratio of the student’s total points for a category to the total possible points for that category times its weight and the results for each category are summed.

In this project, the weights-based system was used sparingly in that the difference between these two systems lie solely on the exams. The midterm and final exams were weighted equally even though their point distribution was different. This was done to account for students that struggle at the beginning of the semester but finish strong. In a points-based system, the midterms have a greater impact on the students’ overall grade. Since the difference between the two grading systems was subtle, only one student was affected (“B” versus a “C” letter grade in **'final_grades.xlsx'** below). In the end, students are issued the higher grade of the two systems.

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_gradebook.PNG">
  </p>
&nbsp  


Although weights were only changed for the midterms and exams in this example (code snippet shown below), the code can be easily modified by deleting lines 92 – 97 and manually entering the category header and weight value in the weights dictionary for greater effect. Note, the weights for each category should sum to 1.

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_weights.PNG">
  </p>
&nbsp  


## Extrapolate:

Throughout the semester, I track my students’ progress by estimating the likelihood they can obtain a particular letter grade based upon their current performance and the maximum number of points left in class. I use this spreadsheet to proactively identify and reach out to students on the border between two letter grades. This helps me build a strong rapport with my students since I am initiating the conversation about their performance.

Although I track my students’ progress on an almost weekly basis, this exercise will focus on the times during the semester when students are most interested in their progress: 

* after the first midterm – **'merged_scores_wk2.xlsx'**
* after the second midterm – **'merged_scores_wk4.xlsx'**
* right before the final – **'merged_scores_wk6.xlsx'**

The current score is calculated by taking the ratio of the points accrued by each student at some time in the semester to the total points possible at that time in the semester. The points needed for some letter grade is calculated by subtracting the current number of points accrued by the student from the product of the percent for that letter grade and the maximum points offered in the semester (lines 145 – 146 in the code snippet below). The percentage needed is calculated by taking the ratio of the points needed to the remaining points (lines 147 – 148).

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_extrapolate_II.PNG">
  </p>
&nbsp  

When the number of points needed exceeds the number of points remaining, it is no longer possible for students to obtain that letter grade. This points needed value is then replaced by the string ‘-‘ for easier viewing. The image below captures the students’ current score and points and percentages needed for various letter grades after two weeks into the semester, after the first midterm, of this example class (**'scores_2021-01-06_08-32-AM.xlsx'**).

<p align="center">
  <img src="https://github.com/nlt-python/Gradebook/blob/main/imgs/img_extrapolate.PNG">
  </p>
&nbsp  

The resulting data for extrapolating student grades after the second midterm and before the final exam are in files **'scores_2021-01-06_08-33-AM.xlsx'** and **'scores_2021-01-06_08-34-AM.xlsx'**.
<p></p>
&nbsp  

## Takeaways:
* This project has helped me more accurately and efficiently calculate student grades from multiple sources. 
* Using Python to create my extrapolation table has saved me at least 30-minutes every week.
* I am more adept at using the map and zip functions, pandas filter function with regex and numpy’s random functions.



