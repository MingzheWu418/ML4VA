import numpy as np
import pandas as pd

salary_list = [
    "2007-2008_salary_report.csv",
    "2008-2009_salary_report.csv",
    "2009-2010_salary_report.csv",
    "2010-2011_salary_report.csv",
    "2011-2012_salary_report.csv",
    "2012-2013_salary_report.csv",
    "2013-2014_salary_report.csv",
    "2014-2015_salary_report.csv",
    "2015-2016_salary_report.csv"]


# Previously written because 2015-2016 has different format,
# But that can be manually fixed, so this function becomes irrelevant

# def read_2015():
#     xl = pd.read_csv("./Data/TeacherSalary/csv_original/2015-2016_salary_report.csv", header=None)
#     xl = xl.dropna(axis=1, how='all')
#     new_header = xl.loc[4]
#     xl = xl[5:143].dropna()
#     xl.columns = new_header
#     xl = xl[[  'Division',
#               'Name',
#               'FY 2014 \nActual Average Teacher Salary',
#               'FY 2015 \nActual Average Teacher Salary',
#               'FY 2014 to FY 2015 Percent Increase/ (Decrease)',
#               'FY 2016 \nBudgeted Average Teacher Salary',
#               'FY 2015 to FY 2016 Percent Increase/ (Decrease)',]]
#     return xl

def convert_salary(filename):
    salary = pd.read_csv("./Data/TeacherSalary/csv_original/" + filename, header=None)
    salary = salary.dropna(axis=1, how='all')
    # print(xl[5:10])
    new_header = salary.loc[4]
    salary = salary[5:143].dropna()
    salary.columns = new_header
    # print(salary.columns)
    salary = salary.reset_index().drop(columns=["index"])
    # print(xl.shape)
    for i in range(salary.shape[0]):
        for item in salary.columns:
            if salary[item][i].find("%") != -1:
                if salary[item][i].find("(") != -1:
                    # print(xl[item][i])
                    salary[item][i] = -float(salary[item][i].strip("()%"))
                else:
                    salary[item][i] = float(salary[item][i].strip(" %"))
                # print(xl[item][i])
            elif salary[item][i].find(",") != -1:
                salary[item][i] = float(salary[item][i].replace(",", ""))
    return salary


def read_salary(filename):
    salary = pd.read_csv("./Data/TeacherSalary/csv_transformed/" + filename)
    return salary.drop(columns=["Unnamed: 0"])


if __name__ == "__main__":
    # pass
    for item in salary_list:
        dataframe = convert_salary(item)
        dataframe.to_csv(path_or_buf=("./Data/TeacherSalary/csv_transformed/" + item))
