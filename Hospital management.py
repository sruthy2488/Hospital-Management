import pymysql
mc=pymysql.connect(host="localhost",user="root", password= "root", database="hospital")
cur=mc.cursor()
print("\n\n\t\t\t\t\t\t\t\tETHICURE MEDICAL HOSPITAL")
print("\n\t\t\t\t\t\t\t\t\tWELCOME")
print("\n\t\t\t\t\t\t\t\t\t LOGIN")
u=input("\n\t\t\t\t\t\t\t\tUsername:")
p=int(input("\t\t\t\t\t\t\t\tPassword:"))


cur.execute("select password from login where username like'" + u + "'")
row = cur.fetchall()
for i in row:
    a = list(i)
    if a[0]==p:
        while True:
            print('\n\n\t\t\t\t\t\t\t\t\tMENU')
            print('\t\t\t\t\t\t\t1.DOCTOR')
            print('\t\t\t\t\t\t\t2.PATIENT')
            print('\t\t\t\t\t\t\t3.STAFF')
            print('\t\t\t\t\t\t\t4.EXIT')
            r=int(input("\n\t\t\t\t\t\t\tEnter your choice(1/2/3/4): "))
    


            if r==1:
                print('\n\t\t\t\t\t\t\t1.Registering Doctor details')
                print("\t\t\t\t\t\t\t2.Total doctor details")
                print('\t\t\t\t\t\t\t3.Doctor detail')
                print('\t\t\t\t\t\t\t4.Back to menu')
                choice=int(input("\n\t\t\t\t\t\t\tEnter your choice(1/2/3/4): "))
                if choice==1:
                    n=int(input("\n\t\t\t\t\t\t\tEnter total no of records: "))
                    for k in range(n):
                        DOC_ID=int(input("\n\t\t\t\t\t\t\tEnter Doctor id: "))
                        DOC_NAME=input("\n\t\t\t\t\t\t\tEnter Doctor's Name:" )
                        DEPARTMENT=input("\n\t\t\t\t\t\t\tEnter the Department: ")
                        PHNO=int(input("\n\t\t\t\t\t\t\tEnter Phone number: "))
                        cur.execute("insert into DOCTOR values(%s,%s,%s,%s)",(DOC_ID,DOC_NAME,DEPARTMENT,PHNO))
                    mc.commit()
                    print('\n\t\t\t\t\t\t\tSUCCESSFULLY REGISTERED')


                elif choice==2:
                    x="select*from doctor"
                    cur.execute(x)
                    s=cur.fetchall()
                    print("\n\t\t\t\t\t\t\tDoctor  details")
                    print("\n{:<30}".format("DOC_ID"),"{:<30}".format("DOC_NAME"),"{:<30}".format("DEPARTMENT"),"{:<30}".format("PHNO"))
                    for i in s:
                        for j in i:
                            print(j,end="                     ")
                        print("       ")


                elif choice==3:
                    d=input("\n\t\t\t\t\t\t\tEnter the Doctor's name: ")
                    l='select*from doctor where docname=("{}")'.format(d)
                    cur.execute(l)
                    v=cur.fetchall()
                    print("\n")
                    for i in v:
                        for j in i:
                            print("{:<15}".format(j),end=" ")

                elif choice==4:
                    continue


            if r==2:
                print('\n\t\t\t\t\t\t\t1.Registering new Patient details')
                print("\n\t\t\t\t\t\t\t2.Total patient details")
                print('\n\t\t\t\t\t\t\t3.Patient detail')
                print('\n\t\t\t\t\t\t\t4.Dicharging a patient')
                print('\n\t\t\t\t\t\t\t5..Back to MENU')
                choice=int(input("\n\t\t\t\t\t\t\tENTER YOUR CHOICE(1/2/3/4): "))
        
                if choice==1:
                    n=int(input("\n\t\t\t\t\t\t\tEnter total no of records: "))
                    for k in range(n):
                        PATIENT_ID=input("\n\t\t\t\t\t\t\tEnter Patient's id: ")
                        PATIENT_NAME=input('\n\t\t\t\t\t\t\tEnter Patient Name: ')
                        PATIENT_AGE=int(input("\n\t\t\t\t\t\t\tEnter patient's age: "))
                        DISEASES=input('\n\t\t\t\t\t\t\tEnter the Disease: ')
                        PHNO=int(input('\n\t\t\t\t\t\t\tEnter Phone number: '))
                    
                        cur.execute("insert into PATIENT values(%s,%s,%s,%s,%s)" ,(PATIENT_ID,PATIENT_NAME, PATIENT_AGE,DISEASES,PHNO))
                    mc.commit()
                    print('\n\t\t\t\t\t\t\tSUCCESSFULLY REGISTERED')


                elif choice==2:
                    w='select*from patient'
                    cur.execute(w)
                    r = cur.fetchall()
                    print("\n\t\t\t\t\t\t\tPatient details")
                    print("\n{:<20}".format("PATIENT ID"),"{:<20}".format("PATIENT NAME"),"{:<20}".format("PATIENT AGE"),"{:<20}".format("DISEASES"),"{:<20}".format("    PHNO"))
                    for i in r:
                        for j in i:
                            print(j,end="                 ")
                        print("       ")
                
                
                
        
                
                elif choice==3:
                    h=input("\n\t\t\t\t\t\t\tEnter the name of the patient: ")
                    w='select*from patient where patient_name=("{}")'.format(h)
                    cur.execute(w)
                    u = cur.fetchall()
                    print("\n")
                    for i in u:
                         for j in i:
                             print("{:<15}".format(j),end=" ")



                elif choice==4:
                    name = input("\n\t\t\t\t\t\t\tEnter the Patient Name:")
                    cur.execute("select * from patient  where patient_name='" + name + "'")
                    row = cur.fetchall()
                    print(row)
                    bill = input("\n\t\t\t\t\t\t\tHas he paid all the bills? (y/n):")
                    if bill == "y":
                        cur.execute("delete from patient where patient_name='" + name + "'")
                        mc.commit()
                        print("\n\t\t\t\t\t\t\tDischarge successfull")



                elif choice==5:
                    continue

                    
        
        
            if r==3:
                print('\n\t\t\t\t\t\t\t1.Registering staff details')
                print("\n\t\t\t\t\t\t\t2.Total staff details")
                print('\n\t\t\t\t\t\t\t3.Staff detail')
                print('\n\t\t\t\t\t\t\t4.Back to MENU')
        
                choice=int(input("\n\t\t\t\t\t\t\tENTER YOUR CHOICE(1/2/3/4): "))  

                if choice==1:
                    n=int(input("\n\t\t\t\t\t\t\tEnter total no of records: "))
                    for k in range(n):
                        STAFF_ID=int(input("\n\t\t\t\t\t\t\tEnter STAFF id: "))
                        STAFF_NAME=input('\n\t\t\t\t\t\t\tEnter staff Name: ')
                        STAFF_AGE=int(input('\n\t\t\t\t\t\t\tEnter Age: '))
                        STAFF_WORK=input('\n\t\t\t\t\t\t\tEnter type of work: ')
                        PHNO=int(input('\n\t\t\t\t\t\t\tEnter Phone number: '))
             
                        cur.execute("insert into staff values (%s,%s,%s,%s,%s)",(STAFF_ID,STAFF_NAME,STAFF_AGE,STAFF_WORK,PHNO))
                    mc.commit()
                    print('\n\t\t\t\t\t\t\tSUCCESSFULLY REGISTERED')
           
                elif choice==2:
                    y="select*from staff"
                    cur.execute(y)
                    t=cur.fetchall()
                    print("\n\t\t\t\t\t\t\tStaff details")
                    print("{:<20}".format("STAFF_ID"),"{:<20}".format("STAFF_NAME"),"{:<20}".format(" STAFF_AGE"),"{:<20}".format("  STAFF_WORK       "),"{:<20}".format("      PHNO"))
                    for i in t:
                        for j in i:
                            print(j,end="                ")
                        print("       ")
              
                   

                elif choice==3:
                    f=input("\n\t\t\t\t\t\t\tEnter the name: ")
                    f='select*from staff where staff_name=("{}")'.format(f)
                    cur.execute(f)
                    w=cur.fetchall()
                    for i in w:
                        for j in i:
                             print("{:<15}".format(j),end=" ")


            if r==4:
                print("\n\t\t\t\t\t\t\tEXITING")
                break
    else:
        print("\t\t\t\t\t\t\t\tIncorrect login!!")
        break

                    
   


   