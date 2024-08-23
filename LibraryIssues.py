import sqlite3
from datetime import datetime
def person(connection,studentid,password): #searches for the id in database, will return the matching password, if password is same, return yes
    try:
        cursor=connection.cursor()
        cursor.execute(f"SELECT Password FROM Student WHERE ID='{studentid}'")
        results=cursor.fetchall()
        for item in results: 
            if item[0]==password:
                return ('yes')
    except:
        print("The login (person) function failed")

def view(connection,studentid): #selects books issued to user and prints them in a nice layout
    try:
        cursor=connection.cursor()
        cursor.execute(f'SELECT Book.Title,Book.ID FROM MiddleTable JOIN Book ON Book.ID=MiddleTable.BookID WHERE MiddleTable.StudentID="{studentid}"')
        results = cursor.fetchall()
        print(f"You currently have the following issued to {studentid}\nTitle                    BookId")
        for item in results:
            print(f"{item[0]:<30}{item[1]:<30}")
    except:
        print("The view function failed")
        
def confirm(connection,book1,studentid): #selects bookids issued to user, if the bookid entered is one of the ones issued, return yes
    try:
        cursor=connection.cursor()
        cursor.execute(f'SELECT Book.ID FROM MiddleTable JOIN Book ON Book.ID=MiddleTable.BookID WHERE MiddleTable.StudentID="{studentid}"')
        results=cursor.fetchall()
        for item in results:
            if item[0]==book1:
                return ('yes')
    except:
        print("The confirm function failed")

def remove(connection,studentid,book,time): #select item from middle table, insert into log then remove from middle table
    try:
        cursor=connection.cursor()
        sql="SELECT * FROM MiddleTable WHERE BookID=?"
        cursor.execute(sql,(book,))
        results=cursor.fetchall()
        for item in results:
            sql2="INSERT INTO Log (StudentID, BookID, IssueDate, ReturnDate) VALUES (?,?,?,?)"
            cursor.execute(sql2,(item[1],item[2],item[3],time,))
        sql1="DELETE FROM MiddleTable WHERE BookID=?"
        cursor.execute(sql1,(book,))

    except:
        print("The remove function failed")
    
def avaliable(connection,title,studentid): #check if book is in middle table (already issued), then see if it's in the book table (all books) and return corresponding results
    try:
        cursor=connection.cursor()
        sql="SELECT Book.Title,MiddleTable.StudentID FROM MiddleTable JOIN Book ON Book.ID=MiddleTable.BookID JOIN Student ON Student.ID=MiddleTable.StudentID"
        cursor.execute(sql)
        results=cursor.fetchall()
        for item in results:
            if item[0]==title:
                if item[1]==studentid:
                    return("yours")
                else:
                    return("unavaliable")
        sql1="SELECT Title FROM Book"
        cursor.execute(sql1)
        results=cursor.fetchall()
        for item in results:
            if item[0]==title:
                return("avaliable")
        return("invalid")
    except:
        print("The avaliable function failed")

def issue(connection,studentid,title,time): #fetch id from book table, then insert new entry to middle table with studentid, bookid and current time
    try:
        cursor=connection.cursor()
        sql1="SELECT ID FROM Book WHERE Title=?"
        cursor.execute(sql1,(title,))
        results=cursor.fetchall()
        for item in results:
            sql="INSERT INTO MiddleTable (StudentID,BookID,IssueDate) VALUES (?,?,?)"
            cursor.execute(sql,(studentid,item[0],time))
    except:
        print('The issue function failed')

def welcome(connection,studentid):
    cursor=connection.cursor()
    sql="SELECT FirstName,LastName FROM Student WHERE ID=?"
    cursor.execute(sql,(studentid,))
    results=cursor.fetchall()
    for item in results:
        print(f"Hello {item[0]} {item[1]}, Welcome to my library code thing!!!")
    #next lesson make the program welcome the user with their first and last name here

with sqlite3.connect('Library.db') as connection:
    while True:
        time = datetime.now()
        while True: #loop in case user enters letters not numbers
            studentid=input("Student ID:                                            (0 to exit program)\n")
            if studentid=='0':
                print("exitting...")
                password='0'
            else:
                password=input("Password: \n")
            try:
                studentid=int(studentid)
                password=int(password)
                #turn the inputs into int for a later need, if user enters letters, the program will show an error message and loop, if correct, exit loop
                break
            except:    
                print("error, invalid characters")

        #verify that the username and password provided are equal to those in Student table
        if studentid==0:
            break
        lock=person(connection,studentid,password) #if user and pass correct, continue
        if lock=='yes':
            #if the username & password are correct, continue to actions section
            welcome(connection,studentid)
            while True:
                i=input("Would you like to issue(i), return(r), view issues(v), search(s) or logout(0)?\n")
                if i=='i':
                    title=input("What would you like to issue? ")
                    #if they want to issue a book(i), the user will type in a title
                    var=avaliable(connection,title,studentid)
                    if var=="unavaliable":
                        print("this book is unavalible")  #the book is in the library but is on the currently issued table
                    if var=="invalid":
                        print("book name invalid")  #the book is not in the book table
                    if var=="avaliable":
                        print("book issued")  #the book is the library but not the currently issued table
                        issue(connection,studentid,title,time)  
                    if var=="yours":
                        print("you currently have this book issued")  #the book is issued to the current user
                if i=='r':
                    try:
                        view(connection,studentid)
                        #print the list of books in account so user can type in the bookid to return it
                        book1=int(input("Out of the above, which would you like to return? (use bookid) or 0 to exit\n"))
                        if book1==0: #exit
                            break
                        else:
                            result=confirm(connection,book1,studentid) #confirm function to check that the book is issued to that user
                            if result=='yes':
                                remove(connection,studentid,book1,time)  #remove the book from the middle table, add it to the log (previously issued) table with time of return
                                print("The book has been returned") 
                            else:
                                print("You haven't got this book issued")
                    except:
                        print("ID Invalid")
                if i=='v':
                    view(connection,studentid)
                if i=='s':
                    title=input("Which book would you like to find? ")
                    var=avaliable(connection,title,studentid)
                    if var=="unavaliable":
                        print("this book is in our library but issued to another person")  #the book is in the library but is on the currently issued table
                    if var=="invalid":
                        print("We don't have a book with that title in our library")  #the book is not in the book table
                    if var=='yours':
                        print("you currently have this book issued")  #the book is issued to the current user
                    if var=="avaliable":  #the book is in the library but not in the currently issued table
                        print("This book is in our library and avalibale to be issued, would you like to issue it?")
                            #shortcut to issue book to make it easier
                        q=input("Would you like to issue it? (y or n)\n")
                        if q=='y':
                            issue(connection,studentid,title,time)
                if i=='0':
                    break
        else: #user/pass will be wrong, print this message then loop to top
            print("username or password incorrect")