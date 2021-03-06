#-----------------------------------------------------------------------
# reg.py
# Author: Lucas Gen, Yusuf Kocaman
#-----------------------------------------------------------------------
import argparse
import textwrap
from os import path
from sqlite3 import connect
from sys import argv, exit, stderr


def main(argv):
    DATABASE_NAME = 'reg.sqlite'
    parser = argparse.ArgumentParser(
        description='Registrar application: show details about a class',
        allow_abbrev=False)

    parser.add_argument('classid', nargs=1, default='%', type=int,
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

        course_id_string = "Course Id: {}\n".format(row[0])
        day_string = "Days: {}".format(row[1])
        start_string ="Start time: {}".format(row[2])
        end_string = "End time: {}".format(row[3])
        build_string ="Building: {}".format(row[4])
        room_string = "Room: {}\n".format(row[5])
        area_string = "Area: {}\n".format(row[6])
        title_string ="Title: {}\n".format(row[7])
        desc_string = "Description: {}\n".format(row[8], 72)
        preq_string = "Prerequisites: {}".format(row[9])

        cursor.close()

        dept_and_num_string = []

        cursor = connection.cursor()
        select_string = "" + \
        "SELECT crosslistings.coursenum, crosslistings.dept " + \
        "FROM classes " + \
        "INNER JOIN crosslistings ON classes.courseid = crosslistings.courseid " + \
        "WHERE classes.classid = ? " + \
        "ORDER BY crosslistings.dept ASC, " + \
        "crosslistings.coursenum ASC"

        cursor.execute(select_string, [str(args.classid[0])])

        row = cursor.fetchone()
        while row is not None:
            dept_and_num_string.append("Dept and Number: {} {}".format(
                row[1], row[0]
            ))
            row = cursor.fetchone()

        cursor.close()

        # new cursor to grab professors
        cursor = connection.cursor()

        select_string = "" + \
            "SELECT profs.profname " + \
            "FROM classes " + \
            "INNER JOIN coursesprofs ON classes.courseid = " +\
            "coursesprofs.courseid " + \
            "INNER JOIN profs ON profs.profid = coursesprofs.profid " + \
            "WHERE classes.classid = ? " + \
            "ORDER BY profs.profname ASC"

        cursor.execute(select_string, [str(args.classid[0])])
        profs_string = []

        row = cursor.fetchone()
        while row is not None:
            profs_string.append(
                "Professor: {}".format(row[0])
            )
            row = cursor.fetchone()


        print(textwrap.fill(course_id_string, 72,
                            replace_whitespace=False,
                            break_long_words=True, drop_whitespace=False))

        print(textwrap.fill(day_string, 72, replace_whitespace=False, break_long_words=True, drop_whitespace=False))
        print(textwrap.fill(start_string, 72,
                            replace_whitespace=False, break_long_words=True, drop_whitespace=False))
        print(textwrap.fill(end_string, 72, replace_whitespace=False, break_long_words=True, drop_whitespace=False))
        print(textwrap.fill(build_string, 72, replace_whitespace=False, break_long_words=True, drop_whitespace=False))
        print(textwrap.fill(room_string, 72, replace_whitespace=False, break_long_words=True, drop_whitespace=False))

        for line in dept_and_num_string:
            print(textwrap.fill(line, 72,
                                replace_whitespace=False,
                                break_long_words=True, drop_whitespace=False))
        print()
        print(textwrap.fill(area_string, 72, replace_whitespace=False, break_long_words=True, drop_whitespace=False))
        print(textwrap.fill(title_string, 72,
                            replace_whitespace=False, break_long_words=True))
        print()
        print(textwrap.fill(desc_string, 72, replace_whitespace=False,
                            break_long_words=True))
        print()
        print(textwrap.fill(preq_string, 72, replace_whitespace=False,
                            break_long_words=True))
        print()
        for line in profs_string:
            print(textwrap.fill(line, 72,
                                replace_whitespace=False, break_long_words=True, drop_whitespace=False))

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)




if __name__ == '__main__':
    main(argv)
