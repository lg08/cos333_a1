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

# checks the different departments
for count, area in enumerate(courseid):
    for item in ['-d', '-t', '-n', '-a']:
        ourProg = 'python reg.py {} "{}"'.format(item, area[0])
        refProg = 'python ref_reg.pyc {} "{}"'.format(item, area[0])
        system(ourProg + ' > ourFile')
        system(refProg + ' > refFile')
        system('diff ourFile refFile >> result')
        system('rm -f ourFile refFile')
    print(count)
    if (count == 100):
        break


for count,id in enumerate(classid):
   ourProg = 'python regdetails.py {}'.format(id[0])
   refProg = 'python ref_regdetails.pyc {}'.format(id[0])
   system(ourProg + ' > ourFile')
   system(refProg + ' > refFile')
   system('diff ourFile refFile >> result')
   system('rm -f ourFile refFile')
   print("-" + str(count))
   if (count == 100):
       break
