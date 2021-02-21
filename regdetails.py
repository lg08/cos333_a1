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
        "courses.area," + \
        "courses.title, courses.descrip, courses.prereqs " +\
        "FROM classes " + \
        "INNER JOIN courses ON classes.courseid = courses.courseid " + \
        "WHERE classes.classid = ?"

        cursor.execute(select_string, [str(args.classid[0])])

        row = cursor.fetchone()

        course_id_string = "Course Id: {}\n\n".format(row[0])
        day_string = "Day: {}\n\n".format(row[1])
        start_string ="Start time: {}\n".format(row[2])
        end_string = "End time: {}\n".format(row[3])
        build_string ="Building: {}\n".format(row[4])
        room_string = "Room: {}\n\n".format(row[5])
        area_string = "Area: {}\n\n".format(row[6])
        title_string ="Title: {}\n\n".format(row[7])
        desc_string = "Description: {}\n\n".format(textwrap.fill(row[08], 72))
        preq_string = "Prerequisites: {}\n\n".format(textwrap.fill(row[09]))


        # dept_and_num_string = "Dept and Number: {} {}\n".format(row[6], row[7])

        # while row is not None:
        #     dept_and_num_string = dept_and_num_string + "" +\
        #     "Dept and Number: {} {}\n".format(row[6], row[7])
        #     row = cursor.fetchone()

        print(course_id_string)
        print(day_string)
        print(start_string)
        print(end_string)
        print(build_string)
        print(room_string)
        # print(dept_and_num_string)
        print(area_string)
        print(title_string)
        print(desc_string)
        print(preq_string)




        # print("Course Id: {}\n\n".format(row[0]))
        # print("Days: {}\n".format(row[1]))
        # print("Start time: {}\n".format(row[2]))
        # print("End time: {}\n".format(row[3]))
        # print("Building: {}\n".format(row[4]))
        # print("Room: {}\n\n".format(row[5]))
        # print("Dept and Number: {} {}\n \n".format(row[6], row[7]))
        # print("Area: {}\n\n".format(row[8]))
        # print("Title: {}\n\n".format(row[9]))
        # print("Description: {}\n\n".format(textwrap.fill(row[10], 72)))
        # print("Prerequisites: {}\n\n".format(textwrap.fill(row[11])))
        row = cursor.fetchone()


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
