#-----------------------------------------------------------------------
# reg.py
# Author: Lucas Gen, Yusuf Kocaman
#-----------------------------------------------------------------------
from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
import argparse
import textwrap


def main(argv):
    DATABASE_NAME = 'reg.sqlite'
    parser = argparse.ArgumentParser(
        description='Registrar application: show details about a class',
        allow_abbrev=False)

    parser.add_argument('classid', nargs=1, default='%',
        help='the id of the class whose details should be shown')
    args = parser.parse_args()

    if not path.isfile(DATABASE_NAME):
        print('database reg.sqlite not found', file=stderr)
        exit(1)

    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()

        select_string = "" + \
        "SELECT classes.courseid, classes.days, classes.starttime, " + \
        "classes.endtime, classes.bldg, classes.roomnum, " + \
        "crosslistings.dept, crosslistings.coursenum, courses.area," + \
        "courses.title, courses.descrip, courses.prereqs, profs.profname " +\
        "FROM classes " + \
        "INNER JOIN crosslistings ON crosslistings.courseid = classes.courseid " + \
        "INNER JOIN courses ON classes.courseid = courses.courseid " + \
        "INNER JOIN coursesprofs ON courseprofs.courseid = " + \
        "classes.courseid " + \
        "WHERE classes.classid = ?" + \


        cursor.execute(select_string, [str(args.d[0])])

        row = cursor.fetchone()

        print(row[0])

        # while row is not None:
        #     print_string = ""
        #     i = 0
        #     while i < (5 - len(str(row[0]))):
        #         print_string = print_string + " "
        #         i += 1
        #     print_string = print_string + str(row[0]) + "  "

        #     print_string = print_string + row[1] + "   "

        #     i = 0
        #     while i < (4 - len(row[2])):
        #         print_string = print_string + " "
        #         i += 1
        #     print_string = print_string + row[2] + "  "

        #     i = 0
        #     while i < (3 - len(row[3])):
        #         print_string = print_string + " "
        #         i += 1
        #     print_string = print_string + row[3] + " "

        #     print_string = print_string + row[4]

        #     print_string = textwrap.fill(print_string, 72, initial_indent='',
        #      subsequent_indent='                       ')

        #     print(print_string)

        #     # print("{} {} {} {} {}".format(
        #     #     row[0], row[1], row[2], row[3],
        #     #     textwrap.fill(row[4]), 72))
        #     row = cursor.fetchone()


        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)




if __name__ == '__main__':
    main(argv)
