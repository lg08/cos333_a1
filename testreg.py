from os import system
from sqlite3 import connect


connection = connect('reg.sqlite')
cursor = connection.cursor()

cursor.execute("SELECT crosslistings.dept " + \
    "FROM crosslistings")

courseid = cursor.fetchall()
cursor.close()
connection.close()

for count, area in enumerate(courseid):
    ourProg = 'python reg.py -d "{}"'.format(area[0])
    refProg = 'python ref_reg.pyc -d "{}"'.format(area[0])
    system(ourProg + ' > ourFile')
    system(refProg + ' > refFile')
    system('diff ourFile refFile >> result')
    system('rm -f ourFile refFile')
    if (count == 100):
        break


#for count,id in enumerate(courseid):
#    ourProg = 'python regdetails.py {}'.format(id[0])
#    refProg = 'python ref_regdetails.pyc {}'.format(id[0])
#    system(ourProg + ' > ourFile')
#    system(refProg + ' > refFile')
#    system('diff ourFile refFile >> result')
#    system('rm -f ourFile refFile')
