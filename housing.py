import pandas as pd

rental_list = ["2007.xlsx",
                "2008.xlsx",
                "2009.xlsx",
                "2010.xlsx",
                "2011.xlsx",
                "2012.xlsx",
                "2013.xlsx",
                "2014.xlsx",
                "2015.xlsx",
                "2016.xlsx",
                "2017.xlsx",
                "2018.xlsx",
                "2019.xlsx",]


def read_rental_price():
    rent_df_list = []

    # print(rent_df)
    for ele in rental_list:
        if ele == "2007.xlsx":
            rent_df = pd.read_excel(io="./Data/housing_price/2007.xlsx")
            rent_df = rent_df.iloc[:,[0,5]]
            df_header = rent_df.iloc[0]
            for i in range(1, len(df_header)):
                df_header[i] = 2007
            rent_df = rent_df[1:]
            rent_df.columns = df_header
            rent_df_list.append(rent_df)
        else:
            rent_df = pd.read_excel(io="./Data/housing_price/" + ele)
            df_header = rent_df.iloc[0]
            for i in range(len(df_header)):
                df_header[i] = int(ele[:4])
            rent_df = rent_df[1:]
            rent_df.columns = df_header
            rent_df = rent_df.iloc[:,5]

            rent_df_list.append(rent_df)
        # print(rent_df)
    rent_df_all = pd.concat(rent_df_list, axis=1)
    rent_df_all["County"] = rent_df_all["County"].str.replace("Metro", "")

    increase_df = rent_df_all[["County"]].copy()
    for i in range(2008, 2021):
        increase_df[i] = 100*(rent_df_all[i]/rent_df_all[i-1]-1)
    # print(increase_df)

    rent_df_all = rent_df_all.T
    new_header = rent_df_all.iloc[0]
    rent_df_all = rent_df_all[1:].astype(int)
    rent_df_all.columns = new_header

    increase_df = increase_df.T
    inc_new_header = increase_df.iloc[0]
    increase_df = increase_df[1:]
    increase_df.columns = inc_new_header

    rent_df_all.to_csv(path_or_buf="Data/housing_price/rental_price_fixed.csv")
    increase_df.to_csv(path_or_buf="./Data/housing_price/rental_price_increase.csv")

    return rent_df_all, increase_df


if __name__ == "__main__":
    read_rental_price()
