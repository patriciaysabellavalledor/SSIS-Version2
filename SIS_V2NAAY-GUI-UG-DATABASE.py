import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

BACKGROUND_COLOR = "grey"




win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Simple Student Information System")


#====== variables ======="


#diri na part, nag declare ratag variables para ma store ang string value na i input sa user
	
id_number = tk.StringVar()
name = tk.StringVar()
course = tk.StringVar()
year = tk.StringVar()
gender = tk.StringVar()

#kani diri nga part, mao rani ang pag design ngalan sa system.

title_label = tk.Label(win, text="Student Information System",  font=("Arial",30,"bold"), border=12,relief=tk.GROOVE,bg=BACKGROUND_COLOR)
title_label.pack(side=tk.TOP, fill=tk.X)

#kani diri mao ni ang frame para sa mga input fields

detail_frame = tk.LabelFrame(win, text="Enter Details",font=("Arial",20),bd=12,relief=tk.GROOVE,bg=BACKGROUND_COLOR)
detail_frame.place(x=20,y=90,width=420,height=575)

#kaning data frame mao ni ang frame na kanang ma display ang mga naka store nga student info sa database. Bali makita nimo dira tanan ang
#mga student na imong gipang add

data_frame = tk.Frame(win,bd=12,bg=BACKGROUND_COLOR,relief=tk.GROOVE)
data_frame.place(x=475,y=90,width=810,height=575)


#KANI DIRI NGA PART MAO NANI ANG DESIGN SA INPUT FIELD


#============== INPUT FIELD SA ID NUMBER ======================= #

id_no_lbl = tk.Label(detail_frame, text="ID Number ",font=("Arial",17), bg=BACKGROUND_COLOR)
id_no_lbl.grid(row=0,column=0,padx=2,pady=2)

id_no_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=id_number)
id_no_ent.grid(row=0, column=1, padx=2,pady=2)


#=============== INPUT FIELD SA NAME ===========================# 

name_lbl = tk.Label(detail_frame, text="Name ",font=("Arial",17), bg=BACKGROUND_COLOR)
name_lbl.grid(row=1,column=0,padx=2,pady=2)

name_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=name)
name_ent.grid(row=1, column=1, padx=2,pady=2)


# ==================INPUT FIELD SA COURSE==================== # 

course_lbl = tk.Label(detail_frame, text="Course ",font=("Arial",17), bg=BACKGROUND_COLOR)
course_lbl.grid(row=2,column=0,padx=2,pady=2)

course_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=course)
course_ent.grid(row=2, column=1, padx=2,pady=2)


#====================INPUT FIELD SA COURSE YEAR======================== # 

year_lbl = tk.Label(detail_frame, text="Year ",font=("Arial",17), bg=BACKGROUND_COLOR)
year_lbl.grid(row=3,column=0,padx=2,pady=2)

year_ent = ttk.Combobox(detail_frame,font=("arial",17),state="readonly", textvariable=year)
year_ent["values"] = ("1st Year", "2nd Year", "3rd Year", "4th Year")
year_ent.grid(row=3, column=1, padx=2,pady=2)



# ===================== INPUT FIELD SA GENDER================= # 

gender_lbl = tk.Label(detail_frame,text="Gender ",font=('Arial',15),bg=BACKGROUND_COLOR)
gender_lbl.grid(row=4,column=0,padx=2,pady=2)

gender_ent = ttk.Combobox(detail_frame,font=("Arial",17),state="readonly",textvariable=gender)
gender_ent["values"] = ("Male", "Female", "Others")
gender_ent.grid(row=4,column=1,padx=2,pady=2)


#================================= FUNCTIONS =============================================

#Kaning fetch_data() na function, mao ni nga function ang mo manage sa pag connect sa database ug sa pag kuha sa mga information na
#naka store sa current database. Ang akong gi buhat is nag gi setup nako ang akong XAMPP then didto nasab nako gi manual ug setup akong
#database


def fetch_data():
	conn = pymysql.connect(host="localhost",user="root",password="",database="sms1")
	curr = conn.cursor()
	curr.execute("SELECT * FROM data")
	rows = curr.fetchall()
	if len(rows)!=0:
		student_table.delete(*student_table.get_children())
		for row in rows:
			student_table.insert('',tk.END,values=row)
		conn.commit()
	conn.close()	
				


#Nya kaning add_student() na function, self explanatory raman ni siya. Kani nga function kay mo kuha sa string values na gi input sa user
#then i insert dayon sa database ang string values.

def add_student():
	if id_number.get() == "" or name.get() == "" or course.get() == "" or year.get() == "" or gender.get()=="":
		messagebox.showerror("ERROR", "Please fill all the fields!")
	else:
		conn = pymysql.connect(host="localhost", user="root", password="",database="sms1")
		curr = conn.cursor()
		curr.execute("INSERT INTO data VALUES(%s, %s, %s, %s, %s)",(id_number.get(), name.get(), course.get(), year.get(), gender.get()))
		conn.commit()
		conn.close()
		messagebox.showinfo("SUCCESS", "Student has been successfully added!")
		fetch_data()


#kaning get_cursor nga function kay i fetch ra niya ang data pag naa kay pisliton nga student then i display dayon niya sa input field.

def get_cursor(event):

	cursor_row = student_table.focus()
	content = student_table.item(cursor_row)
	row = content['values']
	id_number.set(row[0])
	name.set(row[1])
	course.set(row[2])
	year.set(row[3])
	gender.set(row[4])

#self explanatory rasab ning clear() na function. Ang buhaton ra ani is i clear ra niya ang mga naka display sa input field.

def clear():
	
	id_number.set("")
	name.set("")
	course.set("")
	year.set("")
	gender.set("")


#kaning update nga function, ang buhaton ani niya is mo connect siya una sa database then i update niya ang name,course,year,ug gender.
#ang update na function is only limited sa pag update sa 4 fields, dili na pwede ma update ang id number (assuming na unchangeable)

def update():
	conn = pymysql.connect(host="localhost",user="root",password="",database="sms1")
	curr = conn.cursor()
	curr.execute("UPDATE data SET name=%s, course=%s, year=%s, gender=%s WHERE id_number=%s",(name.get(),course.get(),year.get(),gender.get(), id_number.get()))
	conn.commit()
	conn.close()
	messagebox.showinfo("SUCCESS", "Student info updated!")
	fetch_data()
	clear()

#kaningg delete na function is i delete rani niya ang info sa isa ka student na naka store sa table sa database

def delete():
	warning = messagebox.askquestion('WARNING','Are you sure you want to delete the following student info?',icon = 'warning')
	if warning == 'yes':
		conn = pymysql.connect(host="localhost",user="root",password="",database="sms1")
		curr = conn.cursor()
		curr.execute("DELETE from data WHERE id_number=%s",(id_number.get()))
		conn.commit()
		conn.close()
		fetch_data()
		clear()
	else:
		pass








#KANI DIRI MAO RANI ANG DESIGN SA BUTTONS


# ====  ANG DESIGN SA BUTTON ==== #
btn_frame = tk.Frame(detail_frame,bg=BACKGROUND_COLOR,bd=10,relief=tk.GROOVE)
btn_frame.place(x=20,y=390,width=352,height=120)


#==== add student === #

add_student_btn = tk.Button(btn_frame,bg=BACKGROUND_COLOR,text="Add",bd=7,font=("Arial",13),width=12, command=add_student)
add_student_btn.grid(row=0,column=0,padx=2,pady=2)

#== update student ==== #

update_student_btn = tk.Button(btn_frame,bg=BACKGROUND_COLOR,text="Update",bd=7,font=("Arial",13),width=12, command=update)
update_student_btn.grid(row=0,column=1,padx=3,pady=2)

# ==== delete student ==== # 

delete_student_btn = tk.Button(btn_frame,bg=BACKGROUND_COLOR,text="Delete",bd=7,font=("Arial",13),width=12, command=delete)
delete_student_btn.grid(row=1,column=0,padx=2,pady=2)

#==== clear ====

clear_student_btn = tk.Button(btn_frame,bg=BACKGROUND_COLOR,text="Clear",bd=7,font=("Arial",13),width=12, command=clear)
clear_student_btn.grid(row=1,column=1,padx=3,pady=2)




#===== DATA BASE FRAME ====== #

main_frame = tk.Frame(data_frame,bg=BACKGROUND_COLOR,bd=11,relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH,expand=True)

y_scroll = tk.Scrollbar(main_frame,orient=tk.VERTICAL)


student_table = ttk.Treeview(main_frame,columns=("ID NUMBER", "NAME", "COURSE", "YEAR", "GENDER"),yscrollcommand=y_scroll.set)

y_scroll.config(command=student_table.yview)

y_scroll.pack(side=tk.RIGHT,fill=tk.Y)

student_table.heading("ID NUMBER", text="ID NUMBER")
student_table.heading("NAME", text="NAME")
student_table.heading("COURSE", text="COURSE")
student_table.heading("YEAR", text="YEAR")
student_table.heading("GENDER", text="GENDER")

student_table['show'] = 'headings'

student_table.column("ID NUMBER", width=100)
student_table.column("NAME", width=100)
student_table.column("COURSE", width=100)
student_table.column("YEAR", width=100)
student_table.column("GENDER", width=100)

student_table.pack(fill=tk.BOTH,expand=True)



fetch_data()

student_table.bind("<ButtonRelease-1>",get_cursor)

win.mainloop()
