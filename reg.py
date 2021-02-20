#-----------------------------------------------------------------------
# reg.py
# Author: Yusuf Kocaman, Lucas Gen
#-----------------------------------------------------------------------
from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
import argparse
import textwrap


def main(argv):
    DATABASE_NAME = 'reg.sqlite'
    parser = argparse.ArgumentParser(
        description='Registrar application: show overviews of classes',
        allow_abbrev=False)

    parser.add_argument('-d', nargs=1, metavar='dept', default='%',
        help='show only those classes whose department contains dept')
    parser.add_argument('-n', nargs=1, metavar='num', default='%',
        help='show only those classes whose course number contains num')
    parser.add_argument('-a', nargs=1, metavar='area', default='%',
        help='show only those classes whose distrib area contains area')
    parser.add_argument('-t', nargs=1, metavar='title', default='%',
        help='show only those classes whose course title contains title')
    args = parser.parse_args()

    print(args.d[0])
    print(vars(args)['d'][0])

    print(args)

    if not path.isfile(DATABASE_NAME):
        print('database reg.sqlite not found', file=stderr)
        exit(1)

    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()

        select_string = "" + \
        "SELECT classes.classid, crosslistings.dept, crosslistings.coursenum, courses.area, courses.title " + \
        "FROM courses " + \
        "INNER JOIN crosslistings ON crosslistings.courseid = courses.courseid " + \
        "INNER JOIN classes ON classes.courseid = courses.courseid " + \
        "WHERE crosslistings.dept LIKE ? " + \
        "AND crosslistings.coursenum LIKE ? " + \
        "AND courses.area LIKE ? " + \
        "AND courses.title LIKE ? "


        cursor.execute(select_string, [str("%" + args.d[0] + "%"),
                                       str("%" + args.n[0] + "%"),
                                       str("%" + args.a[0] + "%"),
                                       str("%" + args.t[0] + "%")])
        # cursor.execute(select_string)
        row = cursor.fetchone()
        while row is not None:
            print("{} {} {} {} {}".format(
                row[0], row[1], row[2], row[3],
                textwrap.fill(row[4]), 72))
            row = cursor.fetchone()
        connection.commit()
        print("transaction commited")
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)




if __name__ == '__main__':
    main(argv)
