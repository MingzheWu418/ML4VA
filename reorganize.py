import pandas as pd
from main import read_name
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def extract_county(county_name):
    df = pd.read_csv("./Data/output/graduation_ver_4.csv")
    county_info = df.loc[df['division_name'] == county_name].sort_values(by=["cohort_year"])
    # print(county_info)
    if county_info.empty:
        return
    county_info = county_info.reset_index().drop(columns=["index"])
    # print(county_info)
    x = county_info["cohort_year"].to_list()
    # x = np.arange(1, county_info["cohort_year"].shape[0]+1)
    y = county_info["curr_year_teacher_salary"].to_list()
    print(x, y)
    # popt, pcov = curve_fit(func, x, y, p0=[0,0,0])
    # print(popt)
    # xx = x
    # yy = func(xx, *popt)
    # plt.scatter(x,y)
    # plt.plot(xx, yy)
    # plt.show()
    # plt.clf()


def func(x, a, c, d):
    return a*np.exp(-c*x)+d


name_list = read_name(file_name="./Data/VA_Income.xls")
new_name_list = []
for item in name_list:
    for county in item[1].split(" + "):
        new_name_list.append(county)

df = pd.dataframe()
for item in new_name_list:
    # print(item)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        extract_county(item)