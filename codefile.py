from tkinter import *
from tabulate import tabulate
import cv2
import os
from tkinter import messagebox
import mysql.connector
import numpy as np
import face_recognition
from datetime import datetime


def save_info():
    mydatabase = mysql.connector.connect(host="localhost", user="root", passwd="", database="mydatabase")
    mycursor = mydatabase.cursor()

    mycursor.execute("Select rollnumber from student")
    myresult = mycursor.fetchall()

    new = []
    for row in myresult:
        new.append(row)
    out = [item for t in new for item in t]

    if entry1.get() == "" or entry2.get() == "" or entry3.get() == "" or entry4.get() == "" or entry5.get() == "":
        return messagebox.showinfo('Notification', 'Entries cannot be empty!!', parent=app)
    if(entry2.get() in out):
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        messagebox.showinfo('Notification', 'Student Already Exist!!', parent=app)
    else:
        name = entry1.get()
        rollnumber = entry2.get()
        fathername = entry3.get()
        course = entry4.get()
        section = entry5.get()

        mycursor.execute("insert into student values('"+name+"','" +rollnumber + "','"+fathername+"','"+course+"','"+section+"')")
        mycursor.execute("commit")
        mydatabase.close()

        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()
            cv2.imshow("Press Space to capture and Enter to exit", frame)

            k = cv2.waitKey(1)
            if k == 13:
                break
            elif k == 32:
                path = "images"
                img_name = "{}_{}.png".format(name, rollnumber)
                cv2.imwrite(os.path.join(path, img_name), frame)

        cam.release()
        cv2.destroyAllWindows()

        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        messagebox.showinfo('Notification', 'Data Inserted!!', parent=app)


def attend():
    path = 'images'
    images = []
    personNames = []
    myList = os.listdir(path)
 
    for i in myList:
        currentimage = cv2.imread(f'{path}/{i}')
        images.append(currentimage)
        personNames.append(os.path.splitext(i)[0])



    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    encodeListKnown = faceEncodings(images)

    def attendance(name):
        splitted = name.split("_")

        roll_file = open("rollnumber.txt","a")
        new = []
        with open('rollnumber.txt','r') as file:
            lines = file.readlines()

        for i in lines:
            new.append(i.replace('\n',''))
        
        if(splitted[1] not in new):

            mydatabase = mysql.connector.connect(host="localhost", user="root", passwd="", database="mydatabase")
            mycursor = mydatabase.cursor()
            mycursor.execute("Select * from student where rollnumber='" + splitted[1] + "'")
            myresult = mycursor.fetchall()
            
            new1=[]
            for row in myresult:
                new1.append(row)
            out = [item for t in new1 for item in t]

            roll_file.write(splitted[1])
            file = open("attendancerecord.txt", "a")

            name_array = ["Name","Roll Number","Father's Name","Course","Section","Attendance Date and time"]
            now = datetime.now()
            datetime_string = now.strftime("%d/%m/%Y %H:%M:%S")
            data_array = [out[0], out[1],out[2],out[3],out[4],datetime_string]
        
            file.write(tabulate([data_array], headers=name_array, tablefmt='orgtbl'))
            file.write("\n")
            file.write("\n")
            roll_file.write("\n")
            file.close()
        roll_file.close()


    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.2, 0.2)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
        
        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 5, x2 * 5, y2 * 5, x1 * 5
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2),(0, 255, 0), cv2.FILLED)
                cv2.putText(frame,name,(x1 + 6, y2 - 6),cv2.FONT_HERSHEY_COMPLEX,0.6,(255, 255, 255),1)
                attendance(name)
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 5, x2 * 5, y2 * 5, x1 * 5
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2),(0, 0, 255), cv2.FILLED)
                cv2.putText(frame,"Not registered!",(x1 + 6, y2 - 6),cv2.FONT_HERSHEY_COMPLEX,0.6,(255, 255, 255),1)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

def deleterecord():
    def record():
        mydatabase = mysql.connector.connect(host="localhost", user="root", passwd="", database="mydatabase")
        mycursor = mydatabase.cursor()
        roll_number = entry13.get()
        
        if roll_number == "":
            messagebox.showinfo('Notification', 'Enter Student Roll Number', parent=app3)
        else:
            newlist = []
            mycursor.execute("Select rollnumber from student")
            myresult = mycursor.fetchall()
        
            for row in myresult:
                newlist.append(row)
            out = [item for t in newlist for item in t]
            if roll_number not in out:
                messagebox.showinfo('Notification', 'No record found!!', parent=app3)
            else:
                mycursor.execute("Select Name from student where rollnumber='" + roll_number + "'")
                myname = mycursor.fetchall()

                sql = "DELETE FROM student where rollnumber='" + roll_number + "'"
                mycursor.execute(sql)
                mydatabase.commit()

                imagename = myname[0][0]+"_"+roll_number+".png"
                location = 'images'
                path = os.path.join(location,imagename)
                os.remove(path)
                messagebox.showinfo('Notification', 'Successfully Deleted', parent=app3)
                entry13.delete(0, END)

    app3 = Tk()
    app3.maxsize(width=300, height=300)
    app3.minsize(width=300, height=300)
    app3.config(bg="slategrey")
    app3.title("Attendance Register")


    label13 = Label(app3, font=("System", "26", "bold"),text="Record Deletion", bg="slategrey")
    label13.place(x=45, y=15)

    label14 = Label(app3, font=("verdana", "10", "bold"),text="Enter Student Roll Number:", bg="slategrey")
    label14.place(x=20, y=80)
    entry13 = Entry(app3,bg="peachpuff", font=("verdana", "13"), justify="left", width=24)
    entry13.place(x=20, y=110)

    btn13 = Button(app3, text="Delete Record", font=("verdana", "8", "bold"),bd="2", padx=80, pady=5, activebackground="slategrey",command=record)
    btn13.place(x=20, y=160)

    app3.mainloop()


app = Tk()
app.maxsize(width=400, height=650)
app.minsize(width=400, height=650)
app.config(bg="slategrey")
app.title("Attendance Register")


label11 = Label(app, font=("System", "26", "bold"),text="Attendance Register Entry", bg="slategrey")
label11.place(x=20, y=15)

label1 = Label(app, font=("verdana", "10", "bold"),text="Enter Your Name:", bg="slategrey")
label1.place(x=20, y=80)
entry1 = Entry(app, bg="peachpuff", font=("verdana", "13"), justify="left", width=30)
entry1.place(x=20, y=110)

label2 = Label(app, font=("verdana", "10", "bold"),text="Enter Class RollNo.:", bg="slategrey")
label2.place(x=20, y=160)
entry2 = Entry(app, bg="peachpuff", font=("verdana", "13"), justify="left", width=30)
entry2.place(x=20, y=190)

label3 = Label(app, font=("verdana", "10", "bold"),text="Enter Father's Name:", bg="slategrey")
label3.place(x=20, y=240)
entry3 = Entry(app, bg="peachpuff", font=("verdana", "13"), justify="left", width=30)
entry3.place(x=20, y=270)

label4 = Label(app, font=("verdana", "10", "bold"),text="Enter Course and Branch:", bg="slategrey")
label4.place(x=20, y=320)
entry4 = Entry(app, bg="peachpuff", font=("verdana", "13"), justify="left", width=30)
entry4.place(x=20, y=350)

label5 = Label(app, font=("verdana", "10", "bold"),text="Enter Section:", bg="slategrey")
label5.place(x=20, y=400)
entry5 = Entry(app, bg="peachpuff", font=("verdana", "13"), justify="left", width=30)
entry5.place(x=20, y=430)

btn1 = Button(app, text="Submit Data & Take Photo", font=("verdana", "8", "bold"),bd="2", padx=75, pady=5, activebackground="slategrey", command=save_info)
btn1.place(x=20, y=480)
btn2 = Button(app, text="Take Attendance", font=("verdana", "8", "bold"),bd="2", padx=105, pady=5, activebackground="slategrey", command=attend)
btn2.place(x=20, y=530)
btn3 = Button(app, text="Delete Student Record", font=("verdana", "8", "bold"),bd="2", padx=86, pady=5, activebackground="slategrey", command=deleterecord)
btn3.place(x=20, y=580)
mainloop()
