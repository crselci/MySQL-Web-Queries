#!"C:\Users\crsel\AppData\Local\Programs\Python\Python311\python"
import cgi
import cgitb
cgitb.enable() ##help with error tracking
#connect to mysql database/server
import mysql.connector
mydb = mysql.connector.connect(
    user='root',
    passwd = #REMOVED PASSWORD,
    host='localhost',
    database="SupplyDB")
mycursor = mydb.cursor()
#print a header and a blank line her
print("Content-type: text/html")
print()

#form is a dictionary with the element names as the keys
form = cgi.FieldStorage()
print(form)
##Given the color and address, retrieve the names of the parts with that color which
##were supplied by all the suppliers in the given address
if 'color' in form:
    color = form['color'].value
    address = form['address'].value
    sql = "SELECT P.pname FROM Parts P WHERE P.color = '" + color + "' AND NOT EXISTS (SELECT S.sid FROM Suppliers S WHERE S.address = '" + address + "' AND NOT EXISTS (SELECT C.pid FROM Catalog C WHERE C.pid = P.pid AND C.sid = S.sid))"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print('<table align="center" border><tr><th>pname</tr></th>')
    for x in myresult:
       print('<tr><td>%s</td></tr>' % x[0])
    print('</table>')
##Given the name of a part, retrieve the information about each supplier who
##supplied it. This information can be any subset of the supplier’s id, supplier’s
##name, address, and the cost the supplier charged for that part    
elif 'pname' in form:
    pname = form['pname'].value
    choices = []
    try:
        sid = form['supid'].value
        choices.append('S.sid')
    except:
        None
        
    try:
        sname = form['supname'].value
        choices.append('S.sname')
    except:
        None
        
    try:
        address = form['supadd'].value
        choices.append("S.address")
    except:
        None
        
    try:
        cost = form['supcost'].value
        choices.append("C.cost")
    except:
        None

    sql = "SELECT " + ",".join(choices) + " FROM Suppliers S, Catalog C, Parts P WHERE S.sid = C.sid AND C.pid = P.pid AND P.pname = '" + pname + "'"
    try:
        mycursor.execute(sql)
    except:
        print("Make a selection")
    myresult = mycursor.fetchall()
    cols = [choice.split(".")[1] for choice in choices]
    print('<table align="center" border><tr>' + ''.join(['<th>' + col + '</th>' for col in cols]) + '</tr>')
    for row in myresult:
        print('<tr>' + ''.join(['<td>%s</td>' % item for item in row]) + '</tr>')
    print('</table>')

##Given the cost, retrieve the names of the suppliers who have ever supplied a part
##with that cost or higher.
elif 'cost' in form:
    cost = form['cost'].value
    sql = "SELECT C.cost, S.sname FROM Catalog C, Suppliers S WHERE S.sid=C.sid AND C.cost >="+"'"+cost+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print('<table align="center" border><tr><th>cost</th><th>sname</th></tr>')
    for x in myresult:
       print('<tr><td>%.2f</td><td>%s</td></tr>' % (x[0], x[1]))
    print('</table>')

##Given the pid, retrieve the names and addresses for the suppliers who charge the
##most for that part.
elif 'pid' in form:
    pid = form['pid'].value
    sql = "SELECT S.sname, S.address FROM Suppliers S, Catalog C WHERE S.sid = C.sid AND C.pid = '" + pid + "' AND C.cost = (SELECT MAX(cost) FROM Catalog WHERE pid = '" + pid + "')"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print('<table align="center" border><tr><th>sname</th><th>address</th></tr>')
    for x in myresult:
       print('<tr><td>%s</td><td>%s</td></tr>' % (x[0], x[1]))
    print('</table>')

##Given the address, retrieve the sids and names of the suppliers in that address who
##do not supply any part
elif 'address' in form:
    address = form['address'].value
    sql = ("SELECT S.sname, S.sid FROM Suppliers S "
           "WHERE S.address = '" + address + "' AND "
           "NOT EXISTS (SELECT 1 FROM Catalog C WHERE C.sid = S.sid)")
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print('<table align="center" border><tr><th>sname</th><th>sid</th></tr>')
    for x in myresult:
       print('<tr><td>%s</td><td>%d</td></tr>' % (x[0], x[1]))
    print('</table>')   

##if input fails
else:
    print("<h4> Try again <h4>")



