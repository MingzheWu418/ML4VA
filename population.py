import pandas as pd


def read_population():
    """
    :return: population by county and year, population increase (from previous year) by county and year
    """
    pop_df = pd.read_excel(io="./Data/VA-Intercensal-Estimates_2000-2010.xls")
    # df_header = pop_df[2]
    # print(pop_df.columns)
    pop_df = pop_df.drop(columns="2000 Census").iloc[3:, 1:]
    pop_df2 = pd.read_excel(io="./Data/VA-Intercensal-Estimates_2010-2020_UVA-CooperCenter.xls")
    pop_df2 = pop_df2.drop(columns=[2010, "2010 Census", "Locality"]).iloc[3:, 1:]
    pop_df = pd.concat([pop_df, pop_df2], axis=1).reset_index().drop(columns="index")
    # print(pop_df[2001]/pop_df[2000])
    # print(pop_df[pop_df.index.duplicated()])
    increase_df = pop_df[["Locality"]].copy()
    for i in range(2001, 2021):
        increase_df[i] = 100*(pop_df[i]/pop_df[i-1]-1)
    pop_df = pop_df.T
    new_header = pop_df.iloc[0]
    pop_df = pop_df[1:].astype(int)
    pop_df.columns = new_header

    increase_df = increase_df.T
    inc_new_header = increase_df.iloc[0]
    increase_df = increase_df[1:]
    increase_df.columns = inc_new_header

    pop_df.to_csv(path_or_buf=("./Data/test/populationT.csv"))
    increase_df.to_csv(path_or_buf=("./Data/test/percent_inc.csv"))
    return pop_df, increase_df

if __name__ == "__main__":
    read_population()
