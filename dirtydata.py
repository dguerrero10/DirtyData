from colorama import init
init()
from colorama import Fore, Back, Style

class DataFrameHelper:
    @classmethod
    def from_file(cls, file_name):
        missing_values = ["n/a", "na", "--"]
        df = pd.read_csv(file_name, na_values = missing_values, error_bad_lines = False)
        return cls(df)

    def __init__(self, df):
         self.df = df

    def __repr__(self):
        return repr(self.df)

    def __str__(self):
        return str(self.df)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self.df, name)

#Column Operations
    def n_percent_nulls(self):
        return self.isnull().sum() *100 / self.shape[0]

    def get_columns(self):
        for index, col in enumerate(self.columns):
            print("--------------------------------------------------------------\n")
            print(f"{index}: {col}")

    def search_columns(self):
        while True:
            try:
                col = ask_user("What column would you like to search?\n >> ")

                if col == "menu":
                    return
                else:
                    value = ask_user("What value are you searching?\n >> ")

                    try:
                        int(value)
                        print(self.loc[self.df[col] == value])
                        return

                    except ValueError:
                        pass

                    print(self.loc[self.df[col] == value])
                    return

            except KeyError as e:
                print(e)

    def melt_dataframe(self):
        while True:
            try:
                answ = ask_user("\nWould you like to keep certain columns untouched? \n[0] No \n[1] Yes\n \nEnter Option:")

                if answ == "menu":
                    return

                elif answ == '1':
                    self.get_columns()
                    num = int(ask_user("Enter the number of columns you would like to leave untouched:\n >> "))
                    if num > 1:
                        id_columns = []
                        counter = 0
                        while counter < num:
                            col = ask_user(f"Enter one {counter + 1} the {num} columns:\n >> ")
                            id_columns.append(col)
                            counter += 1

                    pd.melt(self, id_columns)
                    print(f"\n{self}")
                    return

                else:
                    pd.melt(self)
                    print(f"\n{self}")
                    return

            except KeyError as e:
                print(e)

    def display_n_column(self):
        while True:
            try:
                col = ask_user("What column do you want to display?\n >> ")

                if col == "menu":
                    return
                else:
                    print(f"\n{self.df[col].head(100)}")
                    return

            except KeyError:
                print(f"\nThere is no column named '{col}.' Please enter a valid column name.")

    def display_n_rows(self):
        while True:
            try:
                rows = int(ask_user("How many rows do you want to display?\n >> "))

                if rows == "menu":
                    return
                else:
                    pd.set_option('display.max_rows', rows)
                    print(self.df.head(rows))
                    return

            except ValueError:
                print("Please enter a number.\n >> ")

    def find_value(self):
        value = ask_user("What value are you searching for?\n >> ")
        print(self.df.loc[value])
        # print(self.df.isin([value]).any())

    def rename_column(self):
        while True:
            try:
                col = ask_user("What column do you want to rename?\n >> ")

                if col == "menu":
                    return
                else:
                    name = ask_user("what would you like to rename it to?\n >> ")
                    self = self.rename(columns={col:name}, inplace=True)
                    print(f"\nRenamed column '{col}' to '{name}'\n"
                    "--------------------------------------------------------------\n")
                    return

            except KeyError:
                print(f"There is no column named '{col}'. Please enter a valid column name.")

    def sort_column(self):
        while True:
            try:
                col = ask_user("What column would you like to sort?\n >> ")

                if col == 'menu':
                    return
                else:
                    answ = ask_user("In what order?\n [1] Ascending\n [2] Descending\n Enter option:")

                    try:
                        if answ == "1":
                            self.sort_values(col, ascending=True, inplace=True)
                            print(f"\n{self.df[col]}")
                        elif answ == "2":
                            self.sort_values(col, ascending=False, inplace=True)
                            print(f"\n{self.df[col]}")
                        return

                    except TypeError:
                        print(f"Please enter a valid option.")
            except KeyError:
                print(f"There is no column named '{col}'. Please enter a valid column name.")

    def format_column(self):
        while True:
            try:

                col = ask_user("What column would you like to format?\n >> ")

                if col == "menu":
                    return
                else:
                    answ = ask_user("How would you like to format it?\n [1] Upper Case\n [2] Lower Case\n [3] Trim Whitespace\n [4] Remove Quotes\n Enter option: ")

                    try:
                        if answ == "1":
                            self.df[col] = self.df[col].str.upper()
                        elif answ == "2":
                            self.df[col] = self.df[col].str.lower()
                        elif answ == "3":
                            self.df[col] = self.df[col].str.strip()
                        elif answ == "4":
                            self.df[col] = self.df[col].str.replace('"', '')
                        return

                    except TypeError:
                        print("Please enter a valid option.")

            except AttributeError:
                print("Cannot apply to column due to incompatibale data type.")
            except KeyError:
                print(f"There is no column named '{col}'. Please enter a valid column name.")

    def set_index(self):
        while True:
            try:
                col = ask_user("What column would you like to set as the index?\n >> ")

                if col == "menu":
                    return
                else:
                    self.df.set_index(col, inplace=True, drop=False)
                    return

            except KeyError as e:
                print(f"There is no column named '{col}'. Please enter a valid column name.")

    def drop_column(self):
        while True:
            try:
                col = ask_user("What column would you like to drop?\n")

                if col == "menu":
                    return
                else:
                    list(col)
                    self.drop(columns=col, axis=1, inplace=True)
                    return

            except KeyError:
                print(f"There is no column named '{col}'\n")

    def change_column_d_type(self):
        while True:
            try:
                print("Your Dataframe object types: \n\n")
                self.info(verbose=True)

                col = ask_user("\nWhat column would you like to change?\n")

                if col == "menu":
                    return
                else:
                    answ = ask_user("What data type would you like to change it to?\n [1] Numeric\n [2] String\n [3] Boolean\n")
                    if answ == "1":
                        if self.df[col].dtype != np.number:
                            print(f"Cannot perform operation. Column '{col}' is a string. Please try again.")
                        else:
                            self.df[col] = pd.to_numeric(self.df[col], errors="raise", inplace=True)
                    elif answ == "2":
                        self.df[col] = self.df[col].astype(dtype = str, errors="raise", inplace=True)
                    elif answ == "3":
                        t = ask_user("Enter what value you would like to associate with True:\n")
                        f = ask_user("Enter what value you would like to associate with False:\n")

                        d = {t: True, f: False}

                        self.df[col] = self.df[col].map(d)
                        return

            except ValueError:
                print("Cannot apply transformation to that column because data type is incompatibale.\n")
            except KeyError:
                print(f"There is no column named '{col}'\n")

    def fill_nan_values(self):
        self.get_columns()
        col = ask_user("What column would you like to change?\n")

        if col ==  "menu":
            return
        else:
            answ = ask_user("Choose how you would like to fill in the values:\n")

            if answ == "mean":
                self.df[col] = self.df[col].fillna((self.df[col].mean()), inplace=True)
            elif answ == "zero":
                self.df[col] = self.df[col].fillna(0, inplace=True)
            elif answ == "value":
                value = ask_user("What kind of value will this be, an int or string?\n")
                if value == "int":
                    value = int(ask_user("What value would you like to use?\n"))
                    self.df[col] = self.df[col].fillna(value=value, inplace=True)
                else:
                    v = ask_user("What value would you like to use?\n")
                    self.df[col] = self.df[col].fillna(value=value, inplace=True)

    #Math Functions
    def sum_individual_column(self):
        while True:
            try:
                col = ask_user("What column would you like to sum?\n")

                if col == "menu":
                    return
                else:
                    if self.df[col].dtype != np.number:
                        print(f"\n'Cannot perform operation.'{col}' is not of data type 'number.' Please try again.\n")
                    else:
                        print(self.df[col].sum())
                        return

            except KeyError:
                print(f"There is no column named '{col}'\n")

    def sum_two_columns(self):
        while True:
            try:
                col_1 = ask_user("What column woud you like to sum? Enter column one:\n")

                if col_1 == "menu":
                    return
                else:
                    col_2 = ask_user("What column woud you like to sum? Enter column two:\n")
                    new_column_name = ask_user("What would you like to name the resulting column?\n")

                    if self.df[col_1].dtype != np.number and self.df[col_2] != np.number:
                        print(f"\nCannot perform operation. One of or both columns '{col_1}, {col_2}' are not of data type 'number.' Please try again.\n")
                    else:
                        self.df[new_column_name] = self.df[col_1] + self.df[col_2]
                        print(self.df[new_column_name])
                        return
            except KeyError:
                print(f"Please choose valid column names.")

    def group_by_count(self):
        while True:
            try:
                num = int(ask_user("Enter the number of columns you want to group on:\n >> "))

                if num == "menu":
                    return
                else:
                    if num > 1:
                        id_columns_group = []
                        counter = 0
                        while counter < num:
                            col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                            id_columns_group.append(col)
                            counter += 1
                        num = int(ask_user("How many columns do you want to perform the aggregation on?\n >> "))
                        if num > 1:
                            id_columns_aggr = []
                            counter = 0
                            while counter < num:
                                col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                                id_columns_aggr.append(col)
                                counter += 1

                            print("\n\n")
                            print(self.groupby(id_columns_group)[id_columns_aggr].count())
                            print("\n\n")

                            return

                        elif num == 1:
                            col = ask_user("What column do you want to perform the aggregation on?\n >> ")

                            print("\n\n")
                            print(self.groupby(id_columns_group)[col].count())
                            print("\n\n")

                            return

                    if num == 1:
                        id_column_group = ask_user("What column do you want to group on?\n >> ")
                        id_column_aggr = ask_user("What column do you want to perform the aggregation on?\n >>")

                        print("\n\n")
                        print(self.groupby(id_column_group)[id_column_aggr].count())
                        print("\n\n")

                        return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")

    def group_by_mean(self):
        while True:
            try:
                num = int(ask_user("Enter the number of columns you want to group on:\n >> "))

                if num == "menu":
                    return
                else:
                    if num > 1:
                        id_columns_group = []
                        counter = 0
                        while counter < num:
                            col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                            id_columns_group.append(col)
                            counter += 1
                        num = int(ask_user("How many columns do you want to perform the operation on?\n >> "))
                        if num > 1:
                            id_columns_aggr = []
                            counter = 0
                            while counter < num:
                                col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                                id_columns_aggr.append(col)
                                counter += 1

                            print("\n\n")
                            print(self.groupby(id_columns_group)[id_columns_aggr].mean())
                            print("\n\n")

                            return
                        elif num == 1:
                            col = ask_user("What column do you want to perform the operation on?\n >> ")

                            print("\n\n")
                            print(self.groupby(id_columns_group)[col].mean())
                            print("\n\n")

                            return

                    if num == 1:
                        id_column_group = ask_user("What column do you want to group on?\n >> ")
                        id_column_aggr = ask_user("What column do you want to perform the operation on?\n >>")

                        print("\n\n")
                        print(self.groupby(id_column_group)[id_column_aggr].mean())
                        print("\n\n")

                        return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")

    def min_value(self):
        while True:
            try:
                col = ask_user("What column do you want to get the min value of?\n >> ")
                if col == "menu":
                    return
                else:
                    if self.df[col].dtype != np.number:
                        print("\nNote: You are getting the min value of a column that is of type 'object', not 'number.'")
                        print(f"\nThe min value of column '{col}' is: ")
                        print("\n")
                        print(self.df[col].min())
                        print("\n")
                        return
                    else:
                        print(f"\nThe min value of column '{col}' is: ")
                        print("\n")
                        print(self.df[col].min())
                        print("\n")
                        return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")

    def max_value(self):
        while True:
            try:
                col = ask_user("What column do you want to get the min value of?\n >> ")
                if col == "menu":
                    return
                else:
                    if self.df[col].dtype != np.number:
                        print("\nNote: You are getting the min value of a column that is of type 'object', not 'number.'")
                        print(f"\nThe min value of column '{col}' is: ")
                        print("\n")
                        print(self.df[col].min())
                        print("\n")

                        return
                    else:
                        print(f"\nThe min value of column '{col}' is: ")
                        print("\n")
                        print(self.df[col].min())
                        print("\n")

                        return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")

#Charts & Plots
    def dist_plot(self):
        while True:
            try:
                col = ask_user("Enter the column you want to plot:\n >> ")
                sns.distplot(self.df[col].dropna())
                plt.show()
                return
            except KeyError as e:
                print(e)

    def print_rows(self):
        print(self.head(30))

    def print_tail(self):
        print(self.tail(30))

    def save_file(self):
        while True:
            try:
                working_directory = os.getcwd()
                print("\nNOTE: The file will be saved in your current directory and will not overwrite your original file.\n")
                file_name = ask_user("Please provide a file name without the csv extension:\n >> ")
                self.df.to_csv(working_directory+'/'+file_name+'.csv', index=None, header=True)
                print(f"Created file {file_name}\n")
                print("\nThanks for cleaning your dirty data!")
                sys.exit()

            except OSError as e:
                print(e)
            except KeyboardInterrupt:
                sys.exit()
            except ValueError as e:
                print("Please enter a valid option.")

    def EXIT(self):
        while True:
            try:
                double_check = int(ask_user("\n Are you sure you want to exit the program? NOTE: Saying 'no' will return you to option menu.\n [0] No\n [1] Yes\n \nEnter option: "))

                if double_check == 1:
                    answ = int(ask_user("Do you want to save your changes first?\n [0] No\n [1] Yes\n \nEnter Option: "))
                    if answ == 1:
                        self.save_file()
                    else:
                        print("\nThanks for cleaning your dirty data!")
                        sys.exit()
                else:
                    return

            except KeyError as e:
                print(e)
            except KeyboardInterrupt:
                sys.exit()
            except ValueError as e:
                print("Please enter either a valid option.")

def ask_user(message, type_=str, validator=lambda x: True, invalid="Not valid"):
    while True:
        try:
            x = type_(input(message))
            if validator(x):
                return x
            else:
                print(invalid)
        except ValueError:
            print("Please pass a(n)", type_)

def csv_files():
    csv_files = []
    csv_file_index = []

    for file in os.listdir():
        if file.endswith(".csv"):
            csv_files.append(file)

    if len(csv_files) != 0:
        for index, file in enumerate(csv_files):
            csv_file_index.append(index)

        return csv_files

def clear_screen():
    OS = os.name

    if OS == "nt":
        os.system("cls")
    else:
        os.system("clear")

import os
import sys
import pyreadline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from art import *

def main():
    try:
        dirty_data_signature = text2art("DirtyData", font='block')
        print(Fore.GREEN, Style.BRIGHT + dirty_data_signature)
        comment = text2art(">>  A  data  cleaning  tool")
        print(Fore.WHITE, Style.BRIGHT + comment)
        print(Fore.CYAN, Style.BRIGHT+">> Created by Dave Guerrero. Email me at daveabdouguerrero@gmail.com for any questions or feedback.\n\n")

        rows_to_display = 30

        print(Fore.WHITE + "\nHere are the files in your current directory you can use: "
        "{}\n".format(csv_files()))

        file_name = ask_user("\nPlease enter the name of the .csv file you want to process. NOTE: If the .csv file is not in the same directory as this program, please provide relative path:\n >>",
                             validator=os.path.isfile,
                             invalid="\nFile path does not exist. Please enter valid path.\nThese are the files in your current directory you can use {}".format(csv_files()))

        display_all_columns = ask_user("\nDo you want to display all the columns in your dataset? NOTE: If your dataset is very wide (has many columns) it may result in a less readable format."
                                       "\n[0] No\n[1] Yes.\n\nEnter Option:")

        if display_all_columns == '1':
            pd.set_option('display.max_columns', None)

        df = DataFrameHelper.from_file(file_name)
        print(f"\nReading in {file_name}...\n")
        file_name = file_name.strip(".csv")
        print(f"Dataframe {file_name} Info\n"
        "----------------------------------------------------------------------------------------------------------------------------------\n")
        df.info(verbose=True)
        df.n_percent_nulls()
        print(f"\nDataframe {file_name} First 30 Rows\n"
        "----------------------------------------------------------------------------------------------------------------------------------\n")
        print(df.head(30))

        while True:
            option = ask_user("\nNOTE: Type 'menu' at any point to return to option menu, 'print' to display first 50 rows, 'tail' to display last 50 rows, 'clear' to clear the screen, and 'exit' to terminate the program. \n\nColumn Operations\n"
            "----------------------------------------------------------------------------------------------------------------------------------\n"
                              " [0] Display Columns\n [1] Rename Column\n [2] Format Column\n [3] Melt Dataframe\n [4] Set Column as Index\n"
                              " [5] Drop Column\n [6] Change Column Data Type\n [7] Fill NaN values\n [8] Display One Column\n [9] Sort Column\n [10] Display Variable Amnt. of Rows\n [11] Find Value in Column\n"
                               "\nMath Operations\n"
                              "----------------------------------------------------------------------------------------------------------------------------------\n"
                              " [12] Sum Individual Column\n [13] Sum Two Columns\n [14] Group By Count\n [15] Group By Mean\n [16] Get Min Value Of Column\n [17] Get Max Value Of Column\n"
                                "\nPlots & Charts\n"
                               "----------------------------------------------------------------------------------------------------------------------------------\n"
                               "[18] Distribution Plot\n"
                              " \nEnter Option:")
            if option == "0":
                df.get_columns()
            if option == '1':
                df.rename_column()
            if option == '2':
                df.format_column()
            if option == '3':
                df.melt_dataframe()
            if option == '4':
                df.set_index()
            if option == '5':
                df.drop_column()
            if option == '6':
                df.change_column_d_type()
            if option == '7':
                df.fill_nan_values()
            if option == "8":
                df.display_n_column()
            if option == "9":
                df.sort_column()
            if option == "10":
                df.display_n_rows()
            if option == "11":
                df.find_value()
            if option == "12":
                df.sum_individual_column()
            if option == "13":
                df.sum_two_columns()
            if option == "14":
                df.group_by_count()
            if option == "15":
                df.group_by_mean()
            if option == "16":
                df.min_value()
            if option == "17":
                df.max_value()
            if option == "18":
                df.dist_plot()
            if option == "test":
                df.search_columns()
            if option == "print":
                df.print_rows()
            if option == "tail":
                df.print_tail()
            if option == "clear":
                clear_screen()
            if option == 'exit':
                df.EXIT()

    except KeyboardInterrupt:
        df.EXIT()

if __name__ == "__main__":
    main()
