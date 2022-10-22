import mysql.connector as mycon
import sys
import time
import pickle
import random


roomvac = [1,2]


con = mycon.connect(host = 'localhost', user = 'root', password = '12345678',database = 'resort')
cur = con.cursor()


def connect():
    con = mycon.connect(host = 'localhost', user = 'root', password = '12345678')
    print('connection successful')
    cur = con.is_connected()
    print(con.is_connected())
    print(type(cur))


def addguest():
    global con, cur
    query = 'select RoomNum from room where status = "Vacant"'
    cur.execute(query)
    results = cur.fetchall()
    #print(row for row in results)
    a = int(input('enter Room Number '))
    b = input('enter Guest name ')
    c = int(input('enter Contact number '))
    d = input('Check In Date ')
    e = input('Check Out Date ')
    rt = int(input('''Enter room type
1. Suite            price 500
2. Deluxe           price 1000
3. Beachside        price 5000
4. Water Bungalow   price 7500  '''))
    if rt == 1:
        pr = 500
    elif rt == 2:
        pr = 1000
    elif rt == 3:
        pr = 5000
    elif rt == 4:
        pr = 7500
    query1 = "insert into guests values('{}','{}','{}','{}','{}','{}')".format(a,b,c,d,e,pr)
    query2 = "insert into payments values({},{},{},{})".format(a,pr,0,0)
    print("you order is being processed")
    ask = input('confirm ? ')
    if ask in 'Yy':
        if a>=1 and a<=10:
            try :
                cur.execute(query1)
                cur.execute(query2)
                con.commit()
                time.sleep(3)
            except:
                print('sorry, room is booked, please select another room')
                addguest()
        else:
            print("room does not exist")
            ans = input('try again ?')
            if ans in "Yyes":
                addguest()
            else:
                main()
    else :
        return


def deleteguest(num):
    global con,cur
    sql = 'delete from guests where RoomNum ='+str(num)
    roomvac.remove(num)
    cur.execute(sql)
    con.commit()
    time.sleep(2)
    print('Deleted')


def editguest(num):
    global con, cur
    sql = 'select * from guests where RoomNum = {}'.format(num)
    cur.execute(sql)
    results = cur.fetchall()
    print('*' * 100)
    print('%4s' % 'RoomNum', '%18s' % 'Name', '%13s' % 'Contact', '%13s' % 'Check In', '%17s' % 'Check Out',
          '%15s' % 'Total')
    for row in results:
        print('%2s' % row[0], '%21s' % row[1], '%12s' % row[2], '%17s' % row[3], '%16s' % row[4], '%14s' % row[5])
    print('*' * 100)
    print()
    if cur.rowcount <= 0:
        print('no matching details')
        employeemenu()
    else:
        ans = input('enter y to continue ')
        if ans in "Yyes":
            rn = int(input('enter room number '))
            co = input('enter check out date ')
            query = 'Update guests set RoomNum={}, Check_out = "{}" where RoomNum ={}'.format(rn,co,rn)
            cur.execute(query)
            con.commit()
            time.sleep(3)
            print('Update Successful')
            employeemenu()


def searchguest():
    global con, cur
    print('SEARCH')
    gn = int(input('enter room number to search'))
    query = 'select * from guests where RoomNum ='+str(gn)
    cur.execute(query)
    results = cur.fetchall()
    if cur.rowcount <= 0:
        print('no results')
    else:
        print(results)


def printguest():
    q = "select * from guests"
    cur.execute(q)
    results = cur.fetchall()
    print()
    print('*' * 100)
    print('%4s' % 'RoomNum', '%18s' % 'Name', '%13s' % 'Contact', '%13s' % 'Check In', '%17s' % 'Check Out',
          '%15s' % 'Total')
    for row in results:
        print('%2s' % row[0], '%21s' % row[1], '%12s' % row[2], '%17s' % row[3], '%16s' % row[4], '%14s' % row[5])
    print('*' * 100)
    print()


def printemp():
    q = "select * from employees"
    cur.execute(q)
    results = cur.fetchall()
    print()
    print('*' * 100)
    print('%4s' % 'Employee ID', '%18s' % 'Employee Name', '%13s' % 'Job', '%13s' % 'Email', '%18s' % 'Salary',)
    for row in results:
        print('%2s' % row[0], '%23s' % row[1], '%17s' % row[2], '%19s' % row[3], '%13s' % row[4])
    print('*' * 100)
    print()


def addemp():
    global con, cur
    a = int(input('enter Employee ID '))
    b = input('enter Employee name ')
    c = input('enter Job ')
    d = input('Enter Email ')
    e = int(input('Enter Salary '))
    query = "insert into employees values('{}','{}','{}','{}','{}')".format(a, b, c, d, e)
    time.sleep(2)
    print()
    print("Employee has been added")
    ask = input('confirm ?')
    if ask in 'Yy':
        cur.execute(query)
        con.commit()
        time.sleep(3)


def deleteemp():
    global con, cur
    printemp()
    d = input('enter Employee ID to delete')
    sql = 'delete from Employees where empID = {}'.format(d)
    cur.execute(sql)
    con.commit()
    time.sleep(2)
    print('Deleted')
    time.sleep(2)
    print()


def editemp():
    global con, cur
    e = int(input('enter Employee Id to edit '))
    q = "select * from employees where empID = {}".format(e)
    cur.execute(q)
    results = cur.fetchall()
    print()
    print('*' * 100)
    print('%4s' % 'Employee ID', '%18s' % 'Employee Name', '%13s' % 'Job', '%13s' % 'Email', '%18s' % 'Salary', )
    for row in results:
        print('%2s' % row[0], '%23s' % row[1], '%17s' % row[2], '%19s' % row[3], '%13s' % row[4])
    print('*' * 100)
    print()
    ans = input('enter y to continue')
    if ans == 'y' or ans == 'Y':
        rn = input('enter Employee Name ')
        jo = input('enter new job ')
        co = int(input('enter Salary '))
        query = 'update employees set EmpNm ="{}", JOB = "{}", Salary ={} where empID = {}'.format(rn,jo,co,e)
        cur.execute(query)
        con.commit
        print('Update Successful')


def searchemp():
    global con, cur
    print('SEARCH')
    gn = int(input('enter Emp ID to search'))
    query = 'select * from employees where empID =' + str(gn)
    cur.execute(query)
    results = cur.fetchall()
    if cur.rowcount <= 0:
        print('no results')
    else:
        print(results)


def addpayments():
    global con, cur
    a = int(input('enter Room Number '))
    b = input('enter Package cost ')
    c = input('enter Restaurant_expenses ')
    d = input('Enter Activities ')
    query = "insert into payments values({},'{}','{}','{}',)".format(a,b,c,d,)
    print("Query OK, 1 row affected")
    ask = input('confirm ?')
    if ask in 'Yy':
        cur.execute(query)
        con.commit()
        time.sleep(2)


def deletpayments():
    global con, cur
    d = input('enter payment(room number) to delete')
    sql = 'delete from payments where RoomNum =',d
    cur.execute(sql)
    con.commit()
    time.sleep(2)
    print('Deleted')


def editpayments():
    global con, cur
    e = int(input('enter RoomNum to edit '))
    sql = 'select * from guest where RoomNum = '+ str(e)
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount <= 0:
        print('no matching details')
    else:
        ans = input('enter y to continue')
        if ans == 'y' or ans == 'Y':
            rn = int(input('enter Restaurant expences '))
            co = int(input('enter Activities  '))
            query = 'Update payments set Restaurant_expences ='+rn+', Activities = '+co+' where RoomNum = '+str(e)
            cur.execute(query)
            con.commit
            print('Update Successful')


def searchpayments():
    global con, cur
    print('SEARCH')
    gn = int(input('enter RoomNum to search'))
    query = 'select * from payments where RoomNum =' + str(gn)
    cur.execute(query)
    results = cur.fetchall()
    if cur.rowcount <= 0:
        print('no results')
    else:
        print(results)


def addroom():
    global con, cur
    a = int(input('enter Room Number '))
    b = input('enter Room Type ')
    c = input('enter Status ')
    d = input('Enter Price ')
    query = "insert into room values({},'{}','{}','{}',)".format(a,b,c,d,)
    print("Query OK, 1 row affected")
    ask = input('confirm ?')
    if ask in 'Yy':
        cur.execute(query)
        con.commit()
        time.sleep(2)


def deleteroom():
    global con, cur
    d = input('enter Room Number to delete')
    sql = 'delete from room where RoomNum =',d
    cur.execute(sql)
    con.commit()
    time.sleep(2)
    print('Deleted')


def editroom():
    global con, cur
    e = int(input('enter RoomNum to edit '))
    q = "select * from guests where RoomNum ={}".format(e)
    cur.execute(q)
    results = cur.fetchall()
    print()
    print('*' * 100)
    print('%4s' % 'RoomNum', '%18s' % 'Name', '%13s' % 'Contact', '%13s' % 'Check In','%17s' % 'Check Out', '%15s' % 'Total')
    for row in results:
        print('%2s' % row[0], '%21s' % row[1], '%12s' % row[2],'%17s' % row[3],'%16s' % row[4],'%14s' % row[5])
    print('*' * 100)
    print()
    ans = input('enter y to continue')
    if ans in "Yyes":
        rn = int(input('enter room number '))
        co = input('enter Check Out date ')
        pr = int(input('enter new Total'))
        query = 'update guests set RoomNum ={}, Check_out = {},Total = {} where RoomNum = {}'.format(rn, co, pr, e)
        cur.execute(query)
        con.commit
        print('Update Successful')


def searchroom():
    global con, cur
    print('SEARCH')
    gn = int(input('enter Room to search'))
    query = 'select * from room where RoomNum =' + str(gn)
    cur.execute(query)
    results = cur.fetchall()
    if cur.rowcount <= 0:
        print('no results')
    else:
        print(results)


def backup():
    with open('backup.dat', 'rb+'):
        tables = ['guests', 'employees', 'rooms', 'payments', 'activities']
        for x in tables:
            query = 'select * from'+str(x)
            cur.execute(query)
            records = cur.fetchall()
            pickle.dump(records, 'backup.dat')
            pickle.dump(' ', 'backup.dat')


def bookactivity(num):
    cur.execute("SELECT * FROM Activities")
    results = cur.fetchall()
    print()
    print()
    print('*' * 70)
    print('%4s' % 'Serial', '%18s' % 'Activity', '%14s' % 'Price')
    for row in results:
        print('%2s' % row[0], '%21s' % row[1], '%12s' % row[2])
    print('*' * 70)
    print()
    print()
    x = input('do you want to book a certain activity ?')
    if x in 'Yyes':
        y = int(input("please select activity number"))
        if y == 1:
            price = 100
        elif y == 2:
            price = 50
        elif y == 3:
            price = 200
        elif y == 4:
            price = 150
        elif y == 5:
            price = 125
        elif y == 6:
            price = 250
        cur.execute("update guests set total = total +'{}' where RoomNum ={}".format(price, num))
        cur.execute("update payments set Activities = Activities + {} where RoomNum = {}".format(price, num))
        con.commit()
        time.sleep(2)
        print('activity booked. your card will be charged at the end of your stay')


def restaurants(num):
    print('''available restaurants are 
    1. Fast Food        avg cost 30 per head
    2. Bar & Grill      avg cost 50 per head
    3. Fine Dining      avg cost 100 per head''')
    print()
    print()
    ch = input('book restaurant ?')
    if ch in "Yyes":
        n = int(input("enter number of peopple"))
        wh = int(input('which restaurant ?'))
        if wh == 1:
            pri = 30
        elif wh == 2:
            pri = 50
        elif wh == 3:
            pri = 100
        cur.execute("update guests set total = total +{} where RoomNum = {}".format(pri * n, num))
        cur.execute("update payments set Restaurant_expences = Restaurant_expences + {} where RoomNum = {}".format(pri * n, num))
        con.commit()
        time.sleep(2)
        print('order is being processed')
        time.sleep(3)
    guestmenu(num)


def sysfail():
    x = random.randint(0,100000)
    if not  x == 69420:
        print("SYSTEM FAILURE IMMINENT")
        backup()
        sys.exit()


def guestlogin():
    global con,cur
    print("\t============GUEST LOGIN============")
    print('Welcome to guest login')
    print('''1. Book a room
2. already have a room
3. back''')
    ch = int(input('enter choice'))
    if ch == 1:
        addguest()
        num = int(input('enter room number'))
        guestmenu(num)
    elif ch == 2:
        num = int(input('enter room number'))
        nam = input('enter name')
        guestmenu(num)
    elif ch == 3:
        main()


def guestmenu(num):
    global con,cur
    print('''  
   ________  ___________________   __  __________   ____  __
  / ____/ / / / ____/ ___/_  __/  /  |/  / ____/ | / / / / /
 / / __/ / / / __/  \__ \ / /    / /|_/ / __/ /  |/ / / / / 
/ /_/ / /_/ / /___ ___/ // /    / /  / / /___/ /|  / /_/ /  
\____/\____/_____//____//_/    /_/  /_/_____/_/ |_/\____/   
                                                            
                                                            ''')
    print()
    print('''1. check activities
2. check room tab
3. Check restaurants
4. extend visit 
5. Request staff assistance
6. back''')
    ch = int(input('enter choice'))
    if ch == 1:
        bookactivity(num)
        guestmenu(num)
    elif ch == 2:
        query = "SELECT Restaurant_expences,Activities from payments where RoomNum ='{}'".format(num)
        cur.execute(query)
        results = cur.fetchall()
        print()
        print()
        print('*'*70)
        print('%4s' % 'Restaurant_expences', '%18s' % 'Activities')
        for row in results:
            print('%5s' % row[0], '%27s' % row[1])
        print('*' * 70)
        print()
        print()
        guestmenu(num)
    elif ch == 3:
        restaurants(num)
        guestmenu(num)
    elif ch == 4:
        e = input('Check Out Date ')
        sql = 'update guests set Check_out = "{}" where RoomNum = {}'.format(e,num)
        cur.execute(sql)
        con.commit()
        time.sleep(2)
        guestmenu(num)
    elif ch == 5:
        print('a member of staff will be helping you shortly')
        print()
        time.sleep(3)
        guestmenu(num)
    elif ch == 6:
        guestlogin()


def employeelogin():
    id = int(input('Welcome to employee login, please enter employee number'))
    n = input('enter name ')
    if id>5:
        employeemenu1()
    else:
        employeemenu()


def employeemenu1():
    print('''
    ________  _______  __    ______  ______________   __  __________   ____  __
   / ____/  |/  / __ \/ /   / __ \ \/ / ____/ ____/  /  |/  / ____/ | / / / / /
  / __/ / /|_/ / /_/ / /   / / / /\  / __/ / __/    / /|_/ / __/ /  |/ / / / / 
 / /___/ /  / / ____/ /___/ /_/ / / / /___/ /___   / /  / / /___/ /|  / /_/ /  
/_____/_/  /_/_/   /_____/\____/ /_/_____/_____/  /_/  /_/_____/_/ |_/\____/   
                                                                          
                                                                          ''')
    print()
    print('''1. check on guests)
    2. Edit guest information
    3. Backup
    4. Charge on a Guests tab ''')
    ch = int(input('enter choice'))
    if ch == 1:
        a = int(input('enter room number'))
        sql = "select * from guests where RoomNum ="+a
        cur.execut(sql)
        con.commit()
        time.sleep(2)
        employeemenu1()
    elif ch == 2:
        editguest()
        employeemenu1()
    elif ch == 3:
        backup()
        employeemenu1()
    elif ch == 4:
        editroom()
        employeemenu1()


def main():
    print('''
 _       __     __                             __           __  __            ____  ___________ ____  ____  ______
| |     / /__  / /________  ____ ___  ___     / /_____     / /_/ /_  ___     / __ \/ ____/ ___// __ \/ __ \/_  __/
| | /| / / _ \/ / ___/ __ \/ __ `__ \/ _ \   / __/ __ \   / __/ __ \/ _ \   / /_/ / __/  \__ \/ / / / /_/ / / /   
| |/ |/ /  __/ / /__/ /_/ / / / / / /  __/  / /_/ /_/ /  / /_/ / / /  __/  / _, _/ /___ ___/ / /_/ / _, _/ / /    
|__/|__/\___/_/\___/\____/_/ /_/ /_/\___/   \__/\____/   \__/_/ /_/\___/  /_/ |_/_____//____/\____/_/ |_| /_/     
                                                                                                                   
                                        ''')
    print()
    print("\t============MENU============")
    print('''1. Guest 
2. Employee 
3. Quit''')
    ch = int(input('enter choice '))
    if ch == 1:
        guestlogin()
    elif ch == 2:
        employeelogin()
    elif ch == 3:
        sys.exit()


def employeemenu():
    print('''
    ________  _______  __    ______  ______________   __  __________   ____  __
   / ____/  |/  / __ \/ /   / __ \ \/ / ____/ ____/  /  |/  / ____/ | / / / / /
  / __/ / /|_/ / /_/ / /   / / / /\  / __/ / __/    / /|_/ / __/ /  |/ / / / / 
 / /___/ /  / / ____/ /___/ /_/ / / / /___/ /___   / /  / / /___/ /|  / /_/ /  
/_____/_/  /_/_/   /_____/\____/ /_/_____/_____/  /_/  /_/_____/_/ |_/\____/   
                                                                          
                                                                          ''')
    print()
    print('Welcome to employee login, please ether employee number')
    print('''1. Check Employee Information
2. Charge on a Guests tab
3. Manage employees
4. check guest information
5. Edit guest information
6. Backup
7. back ''')
    ch = int(input('enter choice'))
    if ch == 1:
        printemp()
        time.sleep(3)
        employeemenu()
    elif ch == 2:
        e = int(input('enter RoomNum of guest to charge '))
        q = "select * from guests where RoomNum ={}".format(e)
        cur.execute(q)
        results = cur.fetchall()
        print()
        print('*' * 100)
        print('%4s' % 'RoomNum', '%18s' % 'Name', '%13s' % 'Contact', '%13s' % 'Check In', '%17s' % 'Check Out','%15s' % 'Total')
        for row in results:
            print('%2s' % row[0], '%21s' % row[1], '%12s' % row[2], '%17s' % row[3], '%16s' % row[4], '%14s' % row[5])
        print('*' * 100)
        print()
        ans = input('enter new total')
        qu = "update guests set Total = {} where RoomNum = {}".format(ans,e)
        cur.execute(qu)
        con.commit()
        time.sleep(3)
        print("Done")
        time.sleep(1)
        employeemenu()
    elif ch == 3:
        x = input('edit, add or delete ?')
        if x in 'delete':
            deleteemp()
        elif x in "add":
            addemp()
        else:
            editemp()
        employeemenu()
    elif ch == 4:
        printguest()
        employeemenu()
    elif ch == 5:
        num = input('enter Room number of guest to change')
        editguest(num)
    elif ch == 6:
        backup()
        employeemenu()
    elif ch == 7:
        main()


main()