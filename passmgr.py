import mysql.connector 
import pickle as le
from cryptography.fernet import Fernet
import base64
def generate_key(P) :
    while len(P)!=32:    #this is only there as Fernet key must be 32 base64-encoded bytes
            if len(P)<32:
                P+=P[::-1]
            elif len(P)>32:
                P=P[0:32]
    return base64.urlsafe_b64encode(P.encode('utf-8'))\

def enc(msg):
    fernet = Fernet(generate_key(Pass))
    return fernet.encrypt(msg.encode())

def dec(msg):
    fernet = Fernet(generate_key(Pass))
    return fernet.decrypt(msg).decode()

def SetUp():
    with open('user.dat','wb+') as f:
        global Pass
        while 1:
            P=input('Create a strong Password(min 4 char max 32): ')
            if (len(P)>3) and (len(P)<=32):
                Pass=P
                le.dump(enc(P),f)
                break 
            else:
                print('PASSWORD SHOULD BE WITHIN 4-32 CHARACTERS')
        
def LogIn():
    f= open('user.dat','rb')
    global Pass
    j=le.load(f)     
    for i in range(5):
        ip=Pass=input('Enter Password: ')  
        try:
            ap=dec(j)    
        except:
            print('Incorrect Password','\nAttemps Remaining',5-i);continue
        if ap==ip:
            print('Access Granted')
            Pass= ip
            f.close()
            return True
    else:
        print('ACCESS DENIED');f.close()
        return False

def SavePass():
    while 1:
        app=input('Enter name of application/website/organisation: ')
        if len(app)>0:
            break
        print('INVALID INPUT \n This field cant be left empty.')
    Uname=input('Enter Username used: ')
    while 1:
        mail=input('Enter MailID : ')
        if ('@'  in mail) and ('.'  in mail):
            break
        print('INVALID EMAIL ADRESS')
    while 1:
        AppPass=input('Enter Account Password: ')
        if len(AppPass)>0:
                break
        print('INVALID INPUT \n This field cant be left empty.')
    sql="insert into data values(%s, %s, %s, %s);"
    val=(app,enc(Uname),enc(mail),enc(AppPass))
    cursor.execute(sql,val)
    connector.commit()

def GetPass():
    cursor.execute("SELECT * FROM data")
    print('~'*4,'Saved accounts','~'*4);x=1
    for i in cursor.fetchall():
        print(x,'-',i[0],'| username:',dec(i[1]));x+=1
    cursor.execute("SELECT * FROM data where app = %s",(input('Input name of the app: '),))
    y=cursor.fetchone()
    print('Email:',dec(y[2]),'\nPASS:',dec(y[3]))

def Update():
    cursor.execute("SELECT * FROM data")
    print('~'*4,'Saved accounts','~'*4);x=1
    w=cursor.fetchall()
    for i in w:
        print(x,'-','App name: ',i[0],'| Username:',dec(i[1]));x+=1
    while 1:
        k=input('Input name of app to Update: ')
        for j in w:
            if k not in j:
                print('Invalid Input')
                break
        else:
            break

    cursor.execute("SELECT * FROM data where app = %s",(k,))
    y=cursor.fetchone()
    print('1-Username:',dec(y[1]),'\n2-Email:',dec(y[2]),'\n3-PASS:',dec(y[3]))
    if (input("What would u like to update? 1, 2, 3 or any other key to exit: "))=='1':
        Uname=input('Enter new Username: ')
        cursor.execute("UPDATE data SET Uname = '"+enc(Uname).decode()+"\' WHERE app = \'"+k+"\'")

    if (input("What would u like to update? 1, 2, 3 or any other key to exit: "))=='2':
        while 1:
            mail=input('Enter Mailid : ')
            if ('@'  in mail) and ('.'  in mail):
                break
            print('INVALID EMAIL ADRESS')
        cursor.execute("UPDATE data SET email = '"+enc(mail).decode()+"\' WHERE app = \'"+k+"\'")

    if (input("What would u like to update? 1, 2, 3 or any other key to exit: "))=='3':
        while 1:
            AppPass=input('enter account password: ')
            if len(AppPass)>0:
                    break
            print('INVALID INPUT \n This field cant be left empty.')
        cursor.execute("UPDATE data SET AppPass = '"+enc(AppPass).decode()+"\' WHERE app = \'"+k+"\'")


    connector.commit()
def DelPass():
    cursor.execute("SELECT * FROM data")
    print('~'*4,'Saved accounts','~'*4);x=1
    for i in cursor.fetchall():
        print(x,'-','App name: ',i[0],'| username:',dec(i[1]));x+=1
    ac=input('Input name of app: ')

    if input('ARE YOU SURE YOU WANT TO PERMANENTLY DELETE THIS PASSWORD?(y to continue)').lower()=='y':
        cursor.execute("delete FROM data where app= %s;",(ac,))
  
    print(cursor.rowcount, "record(s) deleted")
    connector.commit()

connector = mysql.connector.connect(
    host="localhost",
    database='passmgr',
    user="root",
    password="mysql"
    )
cursor = connector.cursor()
Pass=''

try:
    IsloggedOn=LogIn()
except:
    SetUp()
   
    IsloggedOn=True
while IsloggedOn :
    print('WELCOME BACK!\n','~'*15+' MENU '+'~'*15)
    ch=input('''Press
    1-To save a new password
    2-To retrieve a password for an account
    3-To update a password or other details for an account
    4-Delete a password for an account
    : ''')
    if ch=='1':
        SavePass()
        if input('to continue enter "y" or any other key to exit: ').lower()!='y':
            IsloggedOn=False
    elif ch=='2':
        GetPass()
        if input('to continue enter "y" or any other key to exit: ').lower()!='y':
            IsloggedOn=False
    elif ch=='3':
        Update()
        if input('to continue enter "y" or any other key to exit: ').lower()!='y':
            IsloggedOn=False
    elif ch=='4':
        DelPass()
        if input('to continue enter "y" or any other key to exit: ').lower()!='y':
            IsloggedOn=False
    else:
        print('INVALID INPUT')
        if input('to continue enter "y" or any other key to exit: ').lower()!='y':
            IsloggedOn=False

