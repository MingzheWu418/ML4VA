import pandas as pd


def read_population():
    """
    :return: the mean income per capita for each county
    """
    pop_df = pd.read_excel(io="./Data/co-est2019-cumchg-51.xlsx")
    pop_df = pop_df[5:138].iloc[:, :-4]
    pop_df = pop_df.rename(
        columns={list(pop_df)[0]: "county",
                 list(pop_df)[1]: "population_2010",
                 list(pop_df)[2]: "population_2019",
                 list(pop_df)[3]: "population_change",
                 list(pop_df)[4]: "population_percent_change"})
    pop_df = pop_df.reset_index().drop(columns=["index"])
    # print(pop_df["county"])
    for i in range(pop_df.shape[0]):
        # print(i)
        # print(pop_df["county"][i])
        pop_df["county"][i] = pop_df["county"][i].strip(".").split(", ")[0]
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(pop_df)
    return pop_df

    # pop_df =
    # df_dict = {}
    # df_columns = income_df.columns
    # for j in range(len(income_df.columns) - 1):
    #     df_dict[df_columns[j + 1]] = name_list[j][1]
    # df_renamed = income_df.rename(columns=df_dict)
    # s = df_renamed.columns.str.split('+')
    # df_splited = df_renamed.reindex(columns=df_renamed.columns.repeat(s.str.len()))
    # df_splited.columns = sum(s.tolist(), [])
    # df_splited = df_splited.rename(columns=lambda x: x.strip())
    # # df_splited = df_splited.sort_index(axis=1)
    # return df_splited


if __name__ == "__main__":
    read_population()
