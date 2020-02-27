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


#Data Cleaning Suggestions
    def clean_data(self):
        try:
            #Removing white space from column labels (start and end) and replacing space in betweenw with underscore
            print("\nRemoving any white space from column labels and replacing with underscore...\n")
            self.columns = self.columns.str.strip()
            self.columns = self.columns.str.replace(' ','_')
            print(self.columns)

            columns = self.columns
            column_length = len(columns)

            col_position = 0
            for i in range(1, column_length):
                series = self.df.iloc[:, col_position]
                try:
                    #Checking if any string objects should be converted into number data type
                    col_str_numeric = 100 * series.str.isnumeric().sum() / len(series)
                    col_name = self.df.columns[col_position]

                    if col_str_numeric > 0.01:
                        drop_column = ask_user(f"Column '{col_name}' appears to have numbers as a string. Would you like to change the data type to numeric?\n [0] No\n [1] Yes\n \nEnter Option: ")
                        if drop_column == '1':
                            self.df[col_position] = pd.to_numeric(col_position, errors='ignore')

                    #Checking to see if column row has only white space and removing it
                    print(f"\nChecking rows in '{col_name}' for white space and removing items...")
                    col_space = series.str.isspace()

                    for index, value in col_space.items():
                        if value == True:
                            col_space.drop(col_space.index[index])

                except AttributeError as e:
                    pass

                col_position += 1

            print("\nChecking for percentage of null values...\n")

            for col in self.columns:
                null_values = 100 * self.columns.isnull().sum() / len(self.columns)
                if null_values > .30:
                    drop_col = ask_user(f"Column '{col}' has more than 30% null values, would you like to drop it?\n [0] No\n [1] Yes\n [2] Skip All\n \nEnter Option: ")
                    if drop_col == "0" or drop_col == 'no':
                        continue
                    if drop_col == '1' or drop_col == 'yes':
                        list(col)
                        self.drop(columns=col, axis=1, inplace=True)
                        print(f"Dropping {col}...")
                    if drop_col == '2' or drop_col == 'Skip All':
                        return

            if null_values < .30:
                print("\nThere are no columns that have more than 30% null values.\n")

        except KeyboardInterrupt:
            print("Aborting...")
            return

#Column Operations
    def n_percent_nulls(self):
        return self.isnull().sum() *100 / self.shape[0]

    def get_missing_values(self):
        print("\n\n")
        zero_val = (self.df == 0.00).astype(int).sum(axis=0)
        missing_val = self.df.isnull().sum()
        missing_val_percent = 100 * self.df.isnull().sum() / len(self.df)
        table = pd.concat([zero_val, missing_val, missing_val_percent], axis=1)
        table = table.rename(
        columns = {0 : 'Zero Values', 1 : 'Missing Values', 2 : '% of Total Values'})
        table['Total Zero Missing Values'] = table['Zero Values'] + table['Missing Values']
        table['% Total Zero Missing Values'] = 100 * table['Total Zero Missing Values'] / len(self.df)
        table['Data Type'] = self.df.dtypes
        table = table[
        table.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(self.df.shape[1]) + " columns and " + str(self.df.shape[0]) + " Rows.\n"
            "There are " + str(table.shape[0]) +
              " columns that have missing values.\n")
        print(table)
        print("\n\n")

    def display_all_columns(self):
        for index, col in enumerate(self.df.columns):
            print("--------------------------------------------------------------\n")
            print(f"{index}: {col}")

    def display_subset_columns(self):
        while True:
            try:
                slice_method = ask_user("\nDo you want to slice columns by index or column names?\n [0] names\n [1] index\n \nEnter Option: ")

                if slice_method == '0':
                    col_1 = ask_user("Enter the first column name\n >> ")
                    col_2 = ask_user("Enter the second column name\n >> ")

                    print(self.df.loc[:, col_1:col_2].head(50))
                    return

                if slice_method == '1':

                    col_1 = int(ask_user("Enter the first index\n >> "))
                    col_2 = int(ask_user("Enter the second index\n >> "))

                    print(self.df.iloc[:, col_1:col_2].head(50))
                    return

            except KeyError as e:
                print(f"There is no column named {e}")
            except ValueError:
                print("Please pass an integer\n")

    def drop_null_values(self):
        try:
            col = ask_user("\nWhat column do you want to target\n >> ")
            self.dropna(subset=[col], inplace=True)
            print(self.df[col])
            return
        except ValueError as e:
            print(e)

    def search_columns(self):
        while True:
            try:
                print(self.head(25))
                print("[0] Equal to value\n [1] Not Equal to value\n [2] Greater than value\n [3] Less than value\n")
                query_kind = ask_user("What kind of query do you want to perform?\n >> ")

                if query_kind == '0':
                    col = ask_user("What column do you want to query?\n >> ")
                    value = ask_user("What value do you want to look for?\n >> ")

                    result = self.df[self.df[col] == value]

                    if result.empty == True:
                        print(f"\nThere are no {result.shape[0]} rows with '{col} == '{value}'.\n")
                        return

                    print(result.head(10))
                    print(result.tail(10))
                    print(f"\nThere are {result.shape[0]} rows with '{col}' == '{value}'.\n")

                    return

                elif query_kind == '1':
                    col = ask_user("What column do you want to query?\n >> ")
                    value = ask_user("What value do you want to look for?\n >> ")

                    result = self.df[self.df[col] != value]

                    if result.empty == True:
                        print(f"\nThere are no {result.shape[0]} rows with '{col} != '{value}'.\n")
                        return

                    print(result.head(10))
                    print(result.tail(10))
                    print(f"\nThere are {result.shape[0]} rows with '{col}' != '{value}'.\n")

                    return


                elif query_kind == '2':
                    col = ask_user("What column do you want to query?\n >> ")
                    value = ask_user("What value do you to compare it to?\n >> ")

                    result = self.df[self.df[col] > value]

                    if result.empty == True:
                        print(f"\nThere are no {result.shape[0]} rows with '{col} > '{value}'.\n")
                        return

                    print(result.head(10))
                    print(result.tail(10))
                    print(f"\nThere are {result.shape[0]} rows with '{col}' > '{value}'.\n")

                    return

                elif query_kind == '3':
                    col = ask_user("What column do you want to query?\n >> ")
                    value = ask_user("What value do you to compare it to?\n >> ")

                    result = self.df[self.df[col] < value]

                    if result.empty == True:
                        print(f"\nThere are no {result.shape[0]} rows with '{col} < '{value}'.\n")
                        return

                    print(result.head(10))
                    print(result.tail(10))
                    print(f"\nThere are {result.shape[0]} rows with '{col}' < '{value}'.\n")

                    return

            except KeyError as e:
                print(e)

    def slice_df(self):
        while True:
            try:
                row_1 = int(ask_user("What row do you want to start slicing at?\n >> "))
                row_2 =  int(ask_user("What row do you want to end at?\n >> "))

                result = self.df.iloc[row_1:row_2]
                print(result)
                return

            except ValueError:
                print("Please pass an integer.")


    def melt_dataframe(self):
        while True:
            try:
                answ = ask_user("\nWould you like to keep certain columns untouched? \n[0] No \n[1] Yes\n \n >> ")

                if answ == "menu":
                    return

                elif answ == '1':
                    self.display_all_columns()
                    num = int(ask_user("Enter the number of columns you would like to leave untouched:\n >> "))
                    if num > 1:
                        id_columns = []
                        counter = 0
                        while counter < num:
                            col = ask_user(f"Enter one {counter + 1} the {num} columns:\n >> ")
                            id_columns.append(col)
                            counter += 1

                    pd.melt(self, id_columns)
                    print(f"\n{self.head()}")
                    return

                else:
                    pd.melt(self)
                    print(f"\n{self.head()}")
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
                    print(f"\n{self.df[col].head(25)}")
                    print(f"\n{self.df[col].tail(25)}")
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
                    answ = ask_user("In what order?\n [0] Ascending\n [1] Descending\n \n >>")

                    try:
                        if answ == "0":
                            self.sort_values(col, ascending=True, inplace=True)
                            print(f"'\n Sorted '{col}' in ascending order"
                            "\n--------------------------------------------------------------\n")
                            print(f"{self.df[col].head(25)}")
                            print(f"{self.df[col].tail(25)}")
                        elif answ == "1":
                            self.sort_values(col, ascending=False, inplace=True)
                            print(f"'\n Sorted '{col}' in descending order"
                            "\n--------------------------------------------------------------\n")
                            print(f"{self.df[col].head(25)}")
                            print(f"{self.df[col].tail(25)}")
                        return

                    except TypeError:
                        print(f"Please enter a valid option.")
            except KeyError:
                print(f"There is no column named '{col}'. Please enter a valid column name.")

    def format_column(self):
        while True:
            try:

                col = ask_user("\nWhat column would you like to format?\n >> ")

                if col == "menu":
                    return
                else:
                    answ = ask_user("How would you like to format it?\n [1] Upper Case\n [2] Lower Case\n [3] Trim Whitespace\n [4] Remove Quotes\n >> ")

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
                col = ask_user("What column would you like to drop?\n >> ")

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
                            if col == "menu":
                                return
                            else:
                                id_columns_group.append(col)
                                counter += 1
                        num = int(ask_user("How many columns do you want to perform the aggregation on?\n >> "))
                        if num > 1:
                            id_columns_aggr = []
                            counter = 0
                            while counter < num:
                                col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                                if col == "menu":
                                    return
                                else:
                                    id_columns_aggr.append(col)
                                    counter += 1

                                    print("\n\n")
                                    print(self.groupby(id_columns_group)[id_columns_aggr].count())
                                    print("\n\n")

                                    return

                        elif num == 1:
                            col = ask_user("What column do you want to perform the aggregation on?\n >> ")
                            if col == "menu":
                                return
                            else:
                                print("\n\n")
                                print(self.groupby(id_columns_group)[col].count())
                                print("\n\n")

                                return

                    if num == 1:
                        id_column_group = ask_user("What column do you want to group on?\n >> ")
                        id_column_aggr = ask_user("What column do you want to perform the aggregation on?\n >>")

                        if id_column_group == "menu" or id_column_aggr == "menu":
                            return
                        else:
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
                            if col == "menu":
                                return
                            else:
                                id_columns_group.append(col)
                                counter += 1
                        num = int(ask_user("How many columns do you want to perform the operation on?\n >> "))
                        if num > 1:
                            id_columns_aggr = []
                            counter = 0
                            while counter < num:
                                col = ask_user(f"Enter {counter + 1} of the {num} columns:\n >> ")
                                if col == "menu":
                                    return
                                else:
                                    id_columns_aggr.append(col)
                                    counter += 1

                                    print("\n\n")
                                    print(self.groupby(id_columns_group)[id_columns_aggr].mean())
                                    print("\n\n")

                                    return
                        elif num == 1:
                            col = ask_user("What column do you want to perform the operation on?\n >> ")

                            if col == "menu":
                                return
                            else:
                                print("\n\n")
                                print(self.groupby(id_columns_group)[col].mean())
                                print("\n\n")

                                return

                    if num == 1:
                        id_column_group = ask_user("What column do you want to group on?\n >> ")
                        id_column_aggr = ask_user("What column do you want to perform the operation on?\n >>")

                        if id_column_group == "menu" or id_column_aggr == "menu":
                            return
                        else:
                            print("\n\n")
                            print(self.groupby(id_column_group)[id_column_aggr].mean())
                            print("\n\n")

                            return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")

    def max_min_value(self):
        while True:
            try:
                col = ask_user("What column do you want to get the max and min value of?\n >> ")

                if (self.df[col].dtype != np.int64 and self.df[col].dtype != np.int32 and self.df[col].dtype
                    != np.int8 and self.df[col].dtype != np.float32 and self.df[col].dtype != np.float64):
                    print("\nNote: You are getting the max and min value of a column that is of type 'object', not 'number.'")
                    print(f"\nThe max value of column '{col}' is: ")
                    print(self.df[col].max())
                    print(f"\nThe min value of column '{col}' is: ")
                    print(self.df[col].min())

                    return

                else:
                    print(f"\nThe max value of column '{col}' is: ")
                    print(self.df[col].max())
                    print(f"\nThe min value of column '{col}' is: ")
                    print(self.df[col].min())

                    return

            except KeyError as e:
                print(e)
            except ValueError:
                print("Please pass a number.")
            except TypeError as e:
                print(e)

#Charts & Plots
    def dist_plot(self):
        while True:
            try:
                col = ask_user("Enter the column you want to plot:\n >> ")
                sns.distplot(self.df[col].dropna())
                plt.show()
                return
            except TypeError as e:
                print(e)

    def scatter_plot(self):
        while True:
            try:
                x = ask_user("What column do you want to use for the 'x' axis?\n >> ")

                if x == "menu":
                    return
                else:
                    y = ask_user("What column do you want to use for the 'y' axis?\n >> ")
                    print("Add options to your chart:\n [0] hue\n [1] style\n [2] finished\n")

                    options_dict = {0:'hue', 1:'style', 3:'finished'}
                    options_list = []

                    while True:
                        try:
                            parameter = int(ask_user("What option would you like to apply to your chart?.\n >> "))
                        except ValueError:
                            print("Please pass either: '0', '1', '2'\n")
                        try:
                            if parameter == 0 and options_dict[0] != None:
                                hue = ask_user("What column would you like to set as your hue?\n >> ")
                                options_list.append(options_dict[0])
                                options_dict.pop(0)
                                print(f"Chosen options: {options_list}")
                        except KeyError:
                            print("This option is already applied.")

                        try:
                            if parameter == 1 and options_dict[1] != None:
                                style = ask_user("What column would you like to set for style?\n >> ")
                                options_list.append(options_dict[1])
                                options_dict.pop(1)
                                print(f"Chosen options: {options_list}")
                        except KeyError:
                            print("This option is already applied.")

                        if len(options_list) == 2:
                            sns.relplot(x=x, y=y, kind='scatter', hue=hue, style=style, data=self.df)
                            print("Building your chart...")
                            plt.show()
                            return

                        if parameter == 2 and len(options_list) == 0:
                            sns.relplot(x=x, y=y, kind="scatter", data=self.df)
                            print("Building your chart...")
                            plt.show()
                            return

                        if parameter == 2 and len(options_list) >= 1:
                            for i in options_list:
                                if i == 'hue' and len(options_list) == 1:
                                    sns.relplot(x=x, y=y, kind="scatter", hue=hue, data=self.df)
                                    print("Building your chart...")
                                    plt.show()
                                    return
                                elif i == 'style' and len(options_list) == 1:
                                    sns.relplot(x=x, y=y, kind="scatter", style=style, data=self.df)
                                    print("Building your chart...")
                                    plt.show()
                                    return
                                elif len(option_list) == 2:
                                    sns.relplot(x=x, y=y, kind="scatter", hue=hue, stlye=style, data=self.df)
                                    print("Building your chart...")
                                    plt.show()
                                    return
            except TypeError as e:
                print(f"{e}\n")
            except ValueError as e:
                print(f"There is no such column: '{e}'.\n")
            except DataError as e:
                print(f"{e}\n")


    def line_plot(self):
        while True:
            try:
                x = ask_user("What column do you want to use for the 'x' axis?\n >> ")

                if x == "menu":
                    return
                else:
                    y = ask_user("What column do you want to use for the 'y' axis?\n >> ")
                    print("Add options to your chart:\n [0] hue\n [1] style\n [2] finished\n")

                    options_dict = { 0:'hue', 1:'style', 3:'finished' }
                    options_list = []

                    while True:
                        try:
                            parameter = int(ask_user("What option would you like to apply to your chart?.\n >> "))
                        except ValueError:
                            print("Please pass either: '0', '1', '2'\n")
                        try:
                            if parameter == 0 and options_dict[0] != None:
                                hue = ask_user("What column would you like to set as your hue?\n >> ")
                                options_list.append(options_dict[0])
                                options_dict.pop(0)
                                print(f"Chosen options: {options_list}")
                        except KeyError:
                            print("This option is already applied.")

                        try:
                            if parameter == 1 and options_dict[1] != None:
                                style = ask_user("What column would you like to set for style?\n >> ")
                                options_list.append(options_dict[1])
                                options_dict.pop(1)
                                print(f"Chosen options: {options_list}")
                        except KeyError:
                            print("This option is already applied.")

                        if len(options_list) == 2:
                            sort = ask_user("Do you want to set 'sort' to 'False'?]\n [0] No\n [1] Yes\n \nEnter Option:")
                            if sort == '1':
                                sns.relplot(x=x, y=y, kind='line', hue=hue, style=style, data=self.df, sort=True)
                                print("Building your chart...")
                                plt.show()
                                return
                            else:
                                sns.relplot(x=x, y=y, kind='line', hue=hue, style=style, data=self.df, sort=False)
                                print("Building your chart...")
                                plt.show()
                                return
                        if parameter == 2 and len(options_list) == 0:
                            sort = ask_user("Do you want to set 'sort' to 'False'?\n [0] No\n [1] Yes\n \nEnter Option:")
                            if sort == '1':
                                sns.relplot(x=x, y=y, kind="line", data=self.df, sort=False)
                                print("Building your chart...")
                                plt.show()
                                return
                            else:
                                sns.relplot(x=x, y=y, kind="line", data=self.df, sort=True)
                                print("Building your chart...")
                                plt.show()
                                return
                        if parameter == 2 and len(options_list) >= 1:
                            sort = ask_user("Do you want to set 'sort' to 'False'?\n [0] No\n [1] Yes\n \nEnter Option:")
                            if sort == '1':
                                for i in options_list:
                                    if i == 'hue' and len(options_list) == 1:
                                        sns.relplot(x=x, y=y, kind="line", hue=hue, data=self.df, sort=True)
                                        print("Building your chart...")
                                        plt.show()
                                        return
                                    elif i == 'style' and len(options_list) == 1:
                                        sns.relplot(x=x, y=y, kind="line", style=style, data=self.df, sort=True)
                                        print("Building your chart...")
                                        plt.show()
                                        return
                                    elif len(option_list) == 2:
                                        sns.relplot(x=x, y=y, kind="line", hue=hue, stlye=style, data=self.df, sort=True)
                                        print("Building your chart...")
                                        plt.show()
                                        return
                            else:
                                for i in options_list:
                                    if i == 'hue' and len(options_list) == 1:
                                        sns.relplot(x=x, y=y, kind="line", hue=hue, data=self.df, sort=False)
                                        print("Building your chart...")
                                        plt.show()
                                        return
                                    elif i == 'style' and len(options_list) == 1:
                                        sns.relplot(x=x, y=y, kind="line", style=style, data=self.df, sort=False)
                                        print("Building your chart...")
                                        plt.show()
                                        return
                                    elif len(options_list) == 2:
                                        sns.relplot(x=x, y=y, kind="line", hue=hue, stlye=style, data=self.df, sort=False)
                                        print("Building your chart...")
                                        plt.show()
                                        return
            except TypeError as e:
                print(f"{e}\n")
            except ValueError as e:
                print(f"There is no such column: '{e}'.\n")
            except DataError as e:
                print(f"{e}\n")


    def concat_dataframe(self):
        while True:
            try:
                print(Fore.WHITE + "\nHere are the files in your current directory you can use: "
                "{}\n".format(csv_files()))
                file_name_2 = ask_user("\nPlease enter the name of the .csv file you want to concat. NOTE: If the .csv file is not in the same directory as this program, please provide relative path:\n >> ",
                                     validator=os.path.isfile,
                                     invalid="\nFile path does not exist. Please enter valid path.\nThese are the files in your current directory you can use {}".format(csv_files()))
                missing_values = ["n/a", "na", "--"]
                df_2 = pd.read_csv(file_name_2, na_values = missing_values, error_bad_lines = False)

                concat_direction = ask_user("Do you want to concat the dataset horizontally or vertically?\n [0] horizontally\n [1] vertically\n \nEnter Option: ")
                if concat_direction == "0":
                    self.df = pd.concat([self.df, df_2], axis=0)
                    return
                if concat_direction == "1":
                    self = pd.concat([self.df, df_2], axis=1)
                    return

            except ValueError as e:
                print(e)

    def split_df(self):
         self = np.split(self, [2,3], axis=1)
         print(self[0])
         print(self[1])
         print(self[2])

    def print_rows(self):
        print(self.head(15))

    def print_tail(self):
        print(self.tail(15))

    def save_file(self):
        while True:
            try:
                working_directory = os.getcwd()
                print("\nNOTE: The file will be saved in your current directory and will not overwrite your original file.\n")
                file_name = ask_user("Please provide a file name without the 'csv' extension:\n >> ")
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
                double_check = ask_user("\n Are you sure you want to exit the program? NOTE: Saying 'no' will return you to option menu.\n [0] No\n [1] Yes\n \nEnter option: ")

                if double_check == '1':
                    answ = ask_user("Do you want to save your changes first?\n [0] No\n [1] Yes\n \nEnter Option: ")
                    if answ == '1':
                        self.save_file()
                    else:
                        print("\nThanks for cleaning your dirty data!")
                        sys.exit()

                if double_check == '0':
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
            x = x.strip()
            if x == "clear":
                clear_screen()
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

#Settings
def settings():
    while True:
        try:
            option = ask_user("\nWhat setting do you want to change?\n [0] Max Column Width\n [1] Max Rows Displayed\n [2] Max Columns Displayed\n [3] Help\n [4] Return to Main Menu\n\nEnter Option: ")

            if option == '0' or option.lower() == 'Max Column Width':
                max_column_width =  int(ask_user("What would you like to set the max width to?\n >> "))
                pd.set_option('max_colwidth', max_column_width)
            elif option == '1' or option.lower() == 'Max Rows Displayed':
                max_rows =  int(ask_user("What would you like to set the max rows displayed to?\n >> "))
                pd.set_option('display.max_rows', max_rows)
            elif option == '2' or option.lower() == 'Max Columns Displayed':
                max_columns =  int(ask_user("What would you like to set the max columns displayed to?\n >> "))
                pd.set_option('display.max_columns', max_columns)
            elif option == '3' or option.lower() == 'Help':
                print("Official panda documentation for settings:")
                print("https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html")
            elif option == '4' or option.lower() == 'Return to Main Menu':
                return

        except ValueError:
            print("Please pass a valid option.")

import os
import sys
import time
import pandas as pd
from pandas.core.groupby.groupby import DataError
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sys
from art import *

def main():
    try:
        dirty_data_signature = text2art("DirtyData", font='block')
        print(Fore.GREEN, Style.BRIGHT + dirty_data_signature)
        comment = text2art(">>  A  data  cleaning  tool")
        print(Fore.WHITE, Style.BRIGHT + comment)
        print(Fore.CYAN, Style.BRIGHT+">> Written by Dave Guerrero. Email me at daveabdouguerrero@gmail.com for any questions or feedback.\n")

        rows_to_display = 15
        sns.set(style = "darkgrid")

        print(Fore.WHITE + "\nHere are the files in your current directory you can use: "
        "{}\n".format(csv_files()))

        file_name = ask_user("\nPlease enter the name of the .csv file you want to process. NOTE: If the .csv file is not in the same directory as this program, please provide relative path:\n >> ",
                             validator=os.path.isfile,
                             invalid="\nFile path does not exist. Please enter valid path.\nThese are the files in your current directory you can use {}".format(csv_files()))

        data_dict = ask_user("\nIs this a data dictionary? NOTE: Data dictionaries will have a longer column-width in the terminal to accomodate longer strings.\n [0] No\n [1] Yes\n \nEnter Option: ")

        if data_dict == "1" or data_dict == "yes":
            pd.set_option('max_colwidth', 500)

        display_all_columns = ask_user("\nDo you want to display all the columns in your dataset? NOTE: If your dataset is very wide (has many columns) it may result in a less readable format."
                                       "\n[0] No\n[1] Yes.\n\nEnter Option:")
        if display_all_columns == "1":
            pd.set_option('display.max_columns', None)

        pd.set_option('display.max_rows', 500)
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

        clean_data = ask_user("\nWould you like DirtyData to tidy up your data?\n [0] No\n [1] Yes\n \nEnter Option: ")

        if clean_data.lower() == '1' or clean_data == 'yes':
            df.clean_data()

        while True:
            option = ask_user("\nNOTE: Type 'menu' at any point to return to option menu, 'print' to display first 50 rows,"
                              " 'tail' to display last 50 rows, 'info' to get dataset information,\n'concat' to concatenate a dataframe or series,"
                              " 'clear' to clear the screen, 'settings' to set display options, "
                              "and 'exit' to terminate the program. \n\nColumn & Row Operations (Enter number or type keyword)\n"
                              "----------------------------------------------------------------------------------------------------------------------------------\n"
                              " [0] Display All Column Names || 'display_columns'\n [1] Rename Column || 'rename'\n [2] Format Column || 'format'\n [3] Melt Dataframe || 'melt'\n [4] Set Column as Index || 'set_index'\n"
                              " [5] Drop Column || 'drop_column'\n [6] Search Column || 'search_column'\n [7] Change Column Data Type || 'change_d-type'\n [8] Fill NaN values || 'fill_null'\n [9] Display One Column || 'one_column'\n"
                              " [10] Sort Column || 'sort'\n [11] Display Subset of DataFrame by columns || 'slice_col'\n [12] Display Subset of DataFrame by rows || 'slice_rows'\n [13] Display Variable Amnt. of Rows || 'var_rows'\n"
                               "\nMath Operations\n"
                              "----------------------------------------------------------------------------------------------------------------------------------\n"
                              " [14] Sum Individual Column || 'sum_one'\n [15] Sum Two Columns || 'sum_two'\n [16] Group By Count || 'group_count'\n [17] Group By Mean || 'group_mean'\n"
                              " [16] Get Max and Min Value Of Column || 'limit'\n"
                                "\nPlots & Charts\n"
                              "----------------------------------------------------------------------------------------------------------------------------------\n"
                              " [19] Distribution Plot || 'dist_plot'\n [20] Scatter Plot || 'scatter_plot'\n [21] Line Plot || 'line_plot'\n"
                              " \nEnter Option:")

            if option == "0" or option.lower() == "all_columns":
                df.display_all_columns()

            if option == '1' or option.lower() == "rename":
                df.rename_column()

            if option == '2' or option.lower() == "format":
                df.format_column()

            if option == '3' or option.lower() == "melt":
                df.melt_dataframe()

            if option == '4' or option.lower() == "set_index":
                df.set_index()

            if option == '5' or option.lower() == "drop_column":
                df.drop_column()

            if option == "6" or option.lower() == "search_column":
                df.search_columns()

            if option == '7' or option.lower() == "change_d-type":
                df.change_column_d_type()

            if option == '8' or option.lower() == "fill_null":
                df.fill_nan_values()

            if option == "9" or option.lower() == "one_column":
                df.display_n_column()

            if option == "10" or option.lower() == "sort":
                df.sort_column()

            if option == "11" or option.lower() == "slice_col":
                df.display_subset_columns()

            if option == "12" or option.lower() == "slice_rows":
                df.slice_df()

            if option == "13" or option.lower() == "var_rows":
                df.display_n_rows()

            if option == "14" or option.lower() == "sum_one":
                df.sum_individual_column()

            if option == "15" or option.lower() == "sum_two":
                df.sum_two_columns()

            if option == "16" or option.lower() == "group_count":
                df.group_by_count()

            if option == "17" or option.lower() == "group_mean":
                df.group_by_mean()

            if option == "18" or option.lower() == "limit":
                df.max_min_value()

            if option == "19" or option.lower() == "dist_plot":
                df.dist_plot()

            if option == "20" or option.lower() == "scatter_plot":
                df.scatter_plot()

            if option == "21" or option.lower() == "line_plot":
                df.line_plot()

            if option == "concat":
                df.concat_dataframe()

            if option == "print":
                df.print_rows()

            if option == "tail":
                df.print_tail()

            if option == "info":
                df.info(verbose=True)

            if option == "settings":
                settings()

            if option == "clear":
                clear_screen()

            if option == 'exit':
                df.EXIT()

    except KeyboardInterrupt:
        df.EXIT()

if __name__ == "__main__":
    main()
