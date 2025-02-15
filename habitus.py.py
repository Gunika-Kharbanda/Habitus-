import mysql.connector as sqtor
from prettytable import PrettyTable
from datetime import date
#---------------------------------------------------------------------------------  
def creating_db1():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234')
    if conn.is_connected():
        print("connection established")
        print()
        cur=conn.cursor()
        q1="create database users;"
        q2="use users;"
        cur.execute(q1)
        cur.execute(q2)
        conn.commit
    else:

        print("error in connection")
    conn.close()
    
#---------------------------------------------------------------------------------  
def creating_tb_db1():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="create table user_rec(user_name varchar(20), uniqid int(4) primary key \
    ,acquiring_habit char(30) ,habits char(150) default NULL ,password char(20) unique );"
    cur.execute(q)
    conn.commit()
    conn.close()
#---------------------------------------------------------------------------------
    
def creating_db2():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234')
    if conn.is_connected():
        print("connection established")
        print()
        cur=conn.cursor()
        q1="create database tracker;"
        q2="use tracker;"
        cur.execute(q1)
        cur.execute(q2)
    else:

        print("error in connection")
    conn.commit()
    conn.close()
#---------------------------------------------------------------------------------      
def generating_uniqid():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="select * from user_rec;"
    cur.execute(q)
    d=cur.fetchall()
    l=len(d)
    uniqid=1000+len(d)
    conn.commit()
    conn.close()
    return uniqid

#---------------------------------------------------------------------------------    
def new_user():
    user_name=input("enter your name")
    uniqid=generating_uniqid()
    print("your uniqid is",uniqid)
    password=input("enter a password")
    password2=input("confirm password")
    acq_h=input("enter acquiring habit")
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q1="insert into user_rec(user_name,uniqid,acquiring_habit,password) values('{}',{},'{}','{}');".format(user_name,uniqid,acq_h,password2)
    cur.execute(q1)
    conn.commit()
    conn.close()
    return (user_name+'_'+str(uniqid))

#---------------------------------------------------------------------------------  
def creating_tb_db2(k):
    column1='yes_or_no'
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
    cur=conn.cursor()
    q1=f"create table {k}({column1}  char(6),date  DATE);"
    cur.execute(q1)
    conn.commit()
    conn.close()

#---------------------------------------------------------------------------------
    
def checking():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    while True:        
        u=int(input("enter your unique id"))
        password=input("enter your password")
        q=f"select * from user_rec where password={password};"
        cur.execute(q)
        d=cur.fetchall()
        return(d)

#---------------------------------------------------------------------------------  
def check(u):
    ##to confirm if there is any other false table in db2 for this user and then deleteing it and user is part no challenge currently"
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q1="select * from user_rec where uniqid={};".format(u)
    cur.execute(q1)
    data=cur.fetchall()
    if data[0][2]==None:
        pass
    
    else:
        q1=f"update user_rec set acquiring_habit = NULL where uniqid={u} ;"
        cur.execute(q1)
        conn.commit()
        conn.close()

     ##=========================================================================
     
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
    cur=conn.cursor()
    q2="show tables;"
    d=cur.execute(q2)
    d=cur.fetchall()
    if d !=[]:
        for i in d:
            if str(u) in i[0]:
                q3=f"drop table {i[0]};"
                cur.execute(q3)
                conn.commit()
                conn.close()
    else:
        pass
    
#---------------------------------------------------------------------------------  
def updation3(u,acq_h):
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="update user_rec set acquiring_habit ='{}' where uniqid={} ;".format(acq_h,u)
    cur.execute(q)
    conn.commit()
    conn.close()

#---------------------------------------------------------------------------------  
def update_rec_after_comp(u):
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q1=f"update user_rec set habits =[acq_h] where uniqid={u} ;"
    cur.execute(q1)
    conn.commit()
    conn.close()  

#---------------------------------------------------------------------------------  
def tracking(k,u):
    n_days=21
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
    cur=conn.cursor()
    q1=f"select * from {k};"
    cur.execute(q1)
    d=cur.fetchall()
    if len(d)<n_days :
        today = date.today()
        ans=input("did you complete the habit for today?(y-or-n)")
        if ans =='n':
            ##======================================================
            conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
            cur=conn.cursor()
            q1=f"select *  from {k};"
            cur.execute(q1)
            d=cur.fetchall()
            l=[]
            for da in d:
                l.append(da[0])
            count=l.count('n')
            if count ==0:
                n_days+=1
                print("warning - you will lose this challenge after one more day of incompletion")
                print("-------------------------------------------------------------------------")
                print("kindly dont lose motivation and try to complete this challenge,you can do it!!")
                print("-------------------------------------------------------------------------------")
                print("see you tomorrow ,we hope that you will honour your challenge")
                q2=f"insert into {k} values(%s,%s);"
                cur.execute(q2,(ans,today))
                conn.commit()
                conn.close()
                
            else:
                print("you have lost your 21-days challenge")
                check(u)
                ##check module sets acq_h=null and deletes tables related to user from tracker            
                ch=input("enter 1 to start a new challenge  -or- enter 0 to exit:")
                if ch==1:
                    return(1)
                                
                elif ch==0:
                    return(0)
            
            
        elif ans =='y':
            q2=f"insert into {k} values(%s,%s);"
            cur.execute(q2,(ans,today))
            conn.commit()
            conn.close()
            return(0)

    else:
        print("congratulations !! you have completed your challenge!")       
        print("you have acquired your habit")
        update_rec_after_comp()
        check(u)

##=================ADMIN RELATED FUNCTIONS===================
def show_all():
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="select * from user_rec;"
    cur.execute(q)
    d=cur.fetchall()
    l=len(d)
    conn.commit()
    myTable2 = PrettyTable(["user_name", "uniqid","acquiring_habit","habits","password"])
    for da in d:
        myTable2.add_row([da[0],da[1],da[2],da[3],da[4]])
    print(myTable2)
    
    conn.close()
    
    print("There are currently ",l," users associated.")

    print("--------------------------------------------------")
    print("--------------------------------------------------")
#---------------------------------------------------------------
def show_one(u):
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="select * from user_rec where uniqid={};".format(u)
    cur.execute(q)
    d=cur.fetchall()
    
    user_name=d[0][0]
    
    conn.commit()
    conn.close()

    k=user_name+'_'+str(u)
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
    cur=conn.cursor()
    q1=f"select *  from {k};"
    cur.execute(q1)
    d=cur.fetchall()
    l=len(d)
    myTable3 = PrettyTable(["records", "date"])
    for da in d:
        s=da[0]
        i=str(da[1])
        myTable3.add_row([s,i])
    print(myTable3)
    print(l,"records")
    print("--------------------------------------------------")
    print("--------------------------------------------------")        
        
#---------------------------------------------------------------
def selected_deletion(u):  
    conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='users')
    cur=conn.cursor()
    q="select * from user_rec where uniqid={};".format(u)
    cur.execute(q)
    d=cur.fetchall()
    if d==[]:
        print("--------------------------------------------------")
        print("no user with uniqid",u,"exists")
        print("--------------------------------------------------")
       
    else:
        check(u)
        print(d[0])
        print()
        ch8=int(input("press 1 to confirm deletion of this record/0 to cancel::"))
        if ch8==1:
            q1="delete from user_rec where uniqid={};".format(u)
            cur.execute(q1)
            print("record deleted ")
            print("--------------------------------------------------")
            print("--------------------------------------------------")
        
        else:
            print("deletion cancelled")
            print("--------------------------------------------------")
            print("--------------------------------------------------")
        
    conn.commit()
    conn.close()  

##-----------------------------MAIN-BLOCK--------------------------------
    
print("hello! this is a habit tracker!!")
ch_supreme=input("are you admin?y/n")
if ch_supreme=='n':
    print("--------------------------------------------------------------")
    ch1=input("are you an existing user:?")
    if ch1 in 'Nn':
        print("----------------------------------------------------------------")
        print("""Introducing the 21-Day Habit Trial Program. :)
        this is a self-initiated program where you stick to a certain habit
        for 21 days, every day. While it can be used to cultivate new habits,
        you can use it to test out any new activity""")
        print("----------------------------------------------------------------")
        ch=input("do you want to take up this challenge?")
        print("----------------------------------------------------------------")
        if ch in 'yY':
            k=new_user()
            creating_tb_db2(k)
        
        else:
            pass

    elif ch1 in 'yY':
        chec=checking()
        if chec==[]:
            print("wrong password for the id")
            print("you cannot access further  without the correct id and password")
            print("----------------------------------------------------------------")
        else:
            u=chec[0][1]
            pwd=chec[0][4]
            user_name=chec[0][0]
            acq_h=chec[0][2]
                 
            if acq_h==None:
                print("----------------------------------------------------------------")
                print("you dont have any challenge going on currently!!")

                ch3=input("do you want to start another challenge")
                if ch3 in 'yY':
                    check(u)
                    print("----------------------------------------------------------------")
                    acq_h=input("enter habit that you want to start")
                    k=user_name+'_'+str(u)
                    updation3(u,acq_h)
                    creating_tb_db2(k)
                    print("----------------------------------------------------------------")
                    
                else:
                    pass
            else:
                k=user_name+'_'+str(u)
                c=tracking(k,u)
                if c==1:
                    print("----------------------------------------------------------------")
                    acq_h=input("enter habit you want to start")
                    k=user_name+'_'+str(u)
                    creating_tb_db2(k)

                elif c==0:
                    print("----------------------------------------------------------------")
                    ch5=input("do you want to see your progress uptill now?")
                    ("----------------------------------------------------------------")
                    ("----------------------------------------------------------------")
                    if ch5 in 'yY':
                        conn= sqtor.connect(host='localhost',user='root',passwd='1234',database='tracker')
                        cur=conn.cursor()
                        q1=f"select *  from {k};"
                        cur.execute(q1)
                        d=cur.fetchall()
                        l=len(d)
                        myTable = PrettyTable(["records", "date"])
                        for da in d:
                            s=da[0]
                            i=str(da[1])
                            myTable.add_row([s,i])
                        print(myTable)
                    else:
                        pass


elif ch_supreme=='y':
    ps=input("enter your password")
    if ps=="gunika123@":
        while True:
            
            print("------admin_menu------")
            print("-----------------------")
            print("1.show all user records")
            print("2.show progress of any one desired user")
            print("3.delete data of a desired user")
            print("4.exit")
            print("------------------------")
            ch7=int(input("enter choice:"))
            if ch7==1:
                show_all()
#---------------------------------------
            elif ch7==2:
                u=int(input("enter uniqid"))
                show_one(u)
#----------------------------------------
            elif ch7==3:
                u=int(input("enter uniqid to be deleted"))
                selected_deletion(u)

#----------------------------------------
            elif ch7==4:
                break
                    
    else:
        print("wrong password!! access denied.")
