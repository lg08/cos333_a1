import os
from os import system
from sqlite3 import connect

connection = connect('reg.sqlite')
cursor = connection.cursor()

cursor.execute("SELECT crosslistings.dept " + \
    "FROM crosslistings")

courseid = cursor.fetchall()
cursor.close()


cursor = connection.cursor()

cursor.execute("SELECT classes.classid " + \
    "FROM classes")

classid = cursor.fetchall()
cursor.close()


connection.close()

print("there are {} many crosslistings".format(len(courseid)))


# # checks the different departments
for count, area in enumerate(courseid):
    for item in ['-d']:
        ourProg = 'python reg.py {} "{}"'.format(item, area[0] + "%")
        refProg = 'python ref_reg.pyc {} "{}"'.format(item, area[0] + "%")
        system(ourProg + ' &> ourFile')
        system("echo $? >> ourFile")
        system(refProg + ' &> refFile')
        system("echo $? >> refFile")
        system('diff ourFile refFile >> result____')
        system('rm -f ourFile refFile')
        # if os.stat("result____").st_size == 0:
        #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     print(ourProg + "caused the problem")
        #     exit(1)
    print(count)
    # if (count == 100):
    #     break

test_string = [
    "python reg.py",
    "python reg.py -d COS",
    "python reg.py -n 333",
    "python reg.py -n b",
    "python reg.py -a Qr",
    "python reg.py -t intro",
    "python reg.py -t science",
    "python reg.py -t C_S",
    "python reg.py -t c%S",
    "python reg.py -d cos -n 3",
    "python reg.py -d cos -a qr -n 2 -t intro",
    "python reg.py -t 'Independent Study'",
    "python reg.py -t 'Independent Study '",
    "python reg.py -t 'Independent Study  '",
    "python reg.py -t ' Independent Study'",
    "python reg.py -t '  Independent Study'",
    "python reg.py -t=-c",
]


ref_string = [
    "python ref_reg.pyc",
    "python ref_reg.pyc -d COS",
    "python ref_reg.pyc -n 333",
    "python ref_reg.pyc -n b",
    "python ref_reg.pyc -a Qr",
    "python ref_reg.pyc -t intro",
    "python ref_reg.pyc -t science",
    "python ref_reg.pyc -t C_S",
    "python ref_reg.pyc -t c%S",
    "python ref_reg.pyc -d cos -n 3",
    "python ref_reg.pyc -d cos -a qr -n 2 -t intro",
    "python ref_reg.pyc -t 'Independent Study'",
    "python ref_reg.pyc -t 'Independent Study '",
    "python ref_reg.pyc -t 'Independent Study  '",
    "python ref_reg.pyc -t ' Independent Study'",
    "python ref_reg.pyc -t '  Independent Study'",
    "python ref_reg.pyc -t=-c",
]

for index, line in enumerate(test_string):
    print(str(index) + "*")
    system(line + ' &> ourFile')
    system("echo $? >> ourFile")
    system(ref_string[index] + ' &> refFile')
    system("echo $? >> refFile")
    system('diff ourFile refFile >> result____')
    system('rm -f ourFile refFile')
    # if os.stat("result____").st_size == 0:
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     print(line + "caused the problem")
    #     exit(1)


for count,id in enumerate(classid):
    ourProg = 'python regdetails.py {}'.format(id[0])
    refProg = 'python ref_regdetails.pyc {}'.format(id[0])
    system(ourProg + ' &> ourFile')
    system("echo $? >> ourFile")
    system(refProg + ' &> refFile')
    system("echo $? >> refFile")
    system('diff ourFile refFile >> result____')
    # if os.stat("result____").st_size == 0:
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     print(ourProg + "caused the problem")
    #     exit(1)
    system('rm -f ourFile refFile')
    print("-" + str(count))
    # if (count == 100):
    #     break

if os.stat("result____").st_size == 0:
    print("Everything Looks Good!!!!")
    system("rm -f result____")
