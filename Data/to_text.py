#This is going ot convert the csv files into 'insert into' files

import csv
filename = "insert_commands"
lists = ['users','publications','venues','Published','Published_or_Presented_at','attended_by','known_contributors','User_cites','Publication_cites']
result = ""
for table in lists:
    file_to_open = table + ".csv"
    file = open(file_to_open)
    file_reader = csv.reader(file)

    for row in file_reader:
        result = result + "insert into " + table + " values ("
        for el in row:
            try:
                b = int(el)
            except:
                if el != "NULL":
                    el = "'" + el + "'"

            result += el + ","
        result = result[0:-1] + ");\n"
    result += "\n\n"

text_file = open(filename, "w")
text_file.write(result)
text_file.close()
