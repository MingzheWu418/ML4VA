import pandas as pd
import numpy as np
from calc_salary import read_salary
import os
import glob

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

# TODO: Fill in these data
manually_input_list = [
    "2016-2017_salary_report.csv",
    "2017-2018_salary_report.csv",
    "2018-2019_salary_report.csv"
]


def read_name(file_name="./Data/VA_Income.xls"):
    """
    The xls file is managed in a format that each series has an ID, e.g. PCPI51700.
    We can only access each series via this ID.
    But since we need the county name,
    we here create a mapping between IDs and county names.
    """
    xl = pd.read_excel(io=file_name, sheet_name="README", header=None)
    # print(xl.sheet_names)

    xl = xl.dropna(how='all').reset_index().drop(columns=["index"])
    # First read in a correspondence between the county and table
    name_list = []

    # The format of the xls file changes for some reasons,
    # so we have to manually handle that

    format_change = [2200, 2400, 2530, 2600, 2680]
    i = 9
    for limit in format_change:
        while i < limit:
            county_name = xl[0][i + 2]
            county_name = county_name.split("in ")[1].split(",")
            # county_name = county_name.split("in ")[1].split(",")[0].split(" + ")
            name_list.append([xl[0][i], county_name[0]])
            # if len(county_name) > 1:
            #     name_list.append([xl[0][i], county_name[1]])
            i += 27
        i += 1

    # check name_dict
    # print(name_list)
    return name_list


# Handle income
def save_income():
    """
    :return: the mean income per capita for each county
    """
    name_list = read_name()
    income_df = pd.read_excel(io="./Data/VA_Income.xls", sheet_name="Annual")
    # print(df)
    df_dict = {}
    df_columns = income_df.columns
    for j in range(len(income_df.columns) - 1):
        df_dict[df_columns[j + 1]] = name_list[j][1]
    df_renamed = income_df.rename(columns=df_dict)
    s = df_renamed.columns.str.split('+')
    df_splited = df_renamed.reindex(columns=df_renamed.columns.repeat(s.str.len()))
    df_splited.columns = sum(s.tolist(), [])
    df_splited = df_splited.rename(columns=lambda x: x.strip())
    # df_splited = df_splited.sort_index(axis=1)
    df_splited.to_csv("./Data/income/income.csv", index=False, encoding='utf-8-sig')
    return df_splited


def read_population():
    return pd.read_csv("Data/population/populationT.csv")


def read_population_increase():
    return pd.read_csv("Data/population/percent_inc.csv")


def read_rental_price():
    return pd.read_csv("Data/housing_price/rental_price_fixed.csv")


def read_rental_increase():
    return pd.read_csv("Data/housing_price/rental_price_increase_fixed.csv")


def read_income():
    return pd.read_csv("Data/income/income_fixed.csv")


def group_by_year(dataframe):
    year_dict = {}
    # Here we only keep data between 2008 and 2019 because many statistics of 2020 and 2021 are yet to be established
    for index in range(12):
        year_dict[index + 2008] = dataframe.loc[dataframe["Cohort Year"] == (index + 2008)].sort_values(
            by=['Division']).reset_index().drop(columns="index")
    return year_dict


# print(df.loc[df["Cohort Year"] == 2008])
# print(df.groupby(["Division"]))


# print(df_splited.iloc[0].columns)
# for item in df_splited.columns:
#     print(item)
# print(list(df_splited.columns))
# counties = list(df_splited.columns)

# print(df_splited.loc[12])


def comb_dataset():
    # Save X and y into the same dataframe
    # And group by year
    df = pd.read_csv("./Data/cohort_statistics.csv")
    # For the sake of simplicity, only consider Graduation Rate and Dropout Rate for now
    df = df[["Cohort Year", "Division", "Division Name", "Students in Cohort", "Graduation Rate", "Dropout Rate"]]
    graduation_by_year = group_by_year(df)
    for index in range(12):
        cohort_year = index + 2008
        # Combining mean income
        income_df = read_income()
        pop_df = read_population()
        increase_df = read_population_increase()
        rental_df = read_rental_price()
        rental_inc_df = read_rental_increase()
        # print("-----")
        # print(income_df)
        # print(graduation_by_year)
        graduation_by_year[cohort_year]["income_per_capita"] = graduation_by_year[cohort_year]["Division Name"].map(
            income_df.loc[index + 1].to_dict())

        graduation_by_year[cohort_year]["population"] = graduation_by_year[cohort_year]["Division Name"].map(
            pop_df.loc[index + 1].to_dict())

        graduation_by_year[cohort_year]["population_increase"] = graduation_by_year[cohort_year]["Division Name"].map(
            increase_df.loc[index].to_dict())

        graduation_by_year[cohort_year]["rental_price"] = graduation_by_year[cohort_year]["Division Name"].map(
            rental_df.loc[index + 1].to_dict())

        graduation_by_year[cohort_year]["rental_increase"] = graduation_by_year[cohort_year]["Division Name"].map(
            rental_inc_df.loc[index].to_dict())

        # print(graduation_by_year)

        # Combining teacher salary
        if index <= 8:
            df = pd.merge(graduation_by_year[cohort_year], read_salary(salary_list[index]), on='Division').drop(
                columns=["Name"])
            df = df.iloc[:, :-2]
            df.to_csv(path_or_buf=("./Data/test/" + str(cohort_year) + ".csv"))

        # After data from 2016-2020 is filled in, enable this part
        else:
            df = pd.merge(graduation_by_year[cohort_year], read_salary(manually_input_list[index - 9]), on='Division')
            df = df.iloc[:, :-2]
            df.to_csv(path_or_buf=("./Data/test/" + str(cohort_year) + ".csv"))
    return df


def comb_years():
    os.chdir("./Data/test")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # combine all files in the list
    df_list = []
    for f in all_filenames:
        df = pd.read_csv(f)
        df = df.rename(
            columns={list(df)[-3]: "prev_year_teacher_salary", list(df)[-2]: "curr_year_teacher_salary",
                     list(df)[-1]: "teacher_salary_diff"})
        df_list.append(df)
        # print(pd.read_csv(f) for f in all_filenames)
    combined_csv = pd.concat(df_list)
    # export to csv

    combined_csv.to_csv("../graduation_ver_8.csv", index=False, encoding='utf-8-sig')


def num_students_to_int():
    df = pd.read_csv("Data/graduation_ver_8.csv")
    for i in range(df.shape[0]):
        try:
            df["Students in Cohort"][i] = int(df["Students in Cohort"][i].replace(",", ""))
        except:
            print(df["Students in Cohort"][i])
    df.to_csv("./Data/graduation_ver_8.csv", index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    # save_income()
    # read_name()
    # dataset = comb_dataset()
    # print(dataset)
    # comb_years()
    num_students_to_int()
