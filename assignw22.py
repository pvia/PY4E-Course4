# This application will read the mailbox data (mbox.txt) and count the number of email messages per organization 
# (i.e. domain name of the email address) using a database with the following schema to maintain the counts.
# CREATE TABLE Counts (org TEXT, count INTEGER)

import sqlite3

conn = sqlite3.connect('assignw22.sqlite')
curs = conn.cursor()

curs.execute('DROP TABLE IF EXISTS Counts')

curs.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'

lst = []

fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    dom = email.find('@')
    org = email[dom+1:len(email)]

    curs.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = curs.fetchone()
    if row is None:
        curs.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        curs.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in curs.execute(sqlstr):
    print(str(row[0]), row[1])

curs.close()
