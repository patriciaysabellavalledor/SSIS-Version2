import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import database

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

code_lbl = tk.Label(detail_frame, text="COURSE CODE ", font=("Arial", 17), bg=BACKGROUND_COLOR)
cname_lbl = tk.Label(detail_frame, text="COURSE NAME", font=("Arial", 17), bg=BACKGROUND_COLOR)

#============== INPUT FIELD SA ID NUMBER ======================= #

id_no_lbl = tk.Label(detail_frame, text="ID Number ",font=("Arial",17), bg=BACKGROUND_COLOR)
id_no_lbl.grid(row=0,column=0,padx=2,pady=2)

id_no_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=id_number, width = 15)
id_no_ent.grid(row=0, column=1, padx=2,pady=2)


#=============== INPUT FIELD SA NAME ===========================# 

name_lbl = tk.Label(detail_frame, text="Name ",font=("Arial",17), bg=BACKGROUND_COLOR)
name_lbl.grid(row=1,column=0,padx=2,pady=2)

name_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=name, width = 15)
name_ent.grid(row=1, column=1, padx=2,pady=2)


# ==================INPUT FIELD SA COURSE==================== # 

course_lbl = tk.Label(detail_frame, text="Course ",font=("Arial",17), bg=BACKGROUND_COLOR)
course_lbl.grid(row=2,column=0,padx=2,pady=2)

course_ent = tk.Entry(detail_frame,bd=7,font=("arial",17), textvariable=course, width = 15)
course_ent.grid(row=2, column=1, padx=2,pady=2)


#====================INPUT FIELD SA COURSE YEAR======================== # 

year_lbl = tk.Label(detail_frame, text="Year ",font=("Arial",17), bg=BACKGROUND_COLOR)
year_lbl.grid(row=3,column=0,padx=2,pady=2)

year_ent = ttk.Combobox(detail_frame,font=("arial",17),state="readonly", textvariable=year, width = 15)
year_ent["values"] = ("1st Year", "2nd Year", "3rd Year", "4th Year")
year_ent.grid(row=3, column=1, padx=2,pady=2)



# ===================== INPUT FIELD SA GENDER================= # 

gender_lbl = tk.Label(detail_frame,text="Gender ",font=('Arial',15),bg=BACKGROUND_COLOR)
gender_lbl.grid(row=4,column=0,padx=2,pady=2)

gender_ent = ttk.Combobox(detail_frame,font=("Arial",17),state="readonly",textvariable=gender, width = 15)
gender_ent["values"] = ("Male", "Female", "Others")
gender_ent.grid(row=4,column=1,padx=2,pady=2)


#================================= FUNCTIONS =============================================

#Kaning fetch_data() na function, mao ni nga function ang mo manage sa pag connect sa database ug sa pag kuha sa mga information na
#naka store sa current database. Ang akong gi buhat is nag gi setup nako ang akong XAMPP then didto nasab nako gi manual ug setup akong
#database


def fetch_data(caller='student'):
	conn = sqlite3.connect('SSISData.db')
	curr = conn.cursor()

	student_table.delete(*student_table.get_children())

	if caller == 'student':
		curr.execute("SELECT * FROM data")
		rows = curr.fetchall()
		for row in rows:
			student_table.insert('', tk.END, values=row)
	else:
		rows = database.allCourses()
		for course in rows:
			student_table.insert('', 0, values=course)


				


#Nya kaning add_student() na function, self explanatory raman ni siya. Kani nga function kay mo kuha sa string values na gi input sa user
#then i insert dayon sa database ang string values.

def add_student():
	if id_number.get() == "" or name.get() == "" or course.get() == "" or year.get() == "" or gender.get()=="":
		messagebox.showerror("ERROR", "Please fill all the fields!")
	elif course.get() not in database.CourseCodes():
		messagebox.showinfo('Add Student', 'The course you entered is not in the database. Please add it in the course section.')
		return
	else:
		conn = sqlite3.connect('SSISData.db')
		curr = conn.cursor()

		curr.execute('''
		INSERT INTO data(student_id, name, course, year, gender) VALUES (?,?,?,?,?)
		''', (id_number.get(), name.get(), course.get(), int(year.get()[0]), gender.get()))
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
	try:
		course.set(row[2])
		year.set(row[3])
		gender.set(row[4])
	except:
		print('operating with courses data')

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
	conn = sqlite3.connect('SSISData.db')
	curr = conn.cursor()
	curr.execute("UPDATE data SET name=?, course=?, year=?, gender=? WHERE student_id=?",(name.get(),course.get(),year.get()[0],gender.get(), id_number.get()))
	conn.commit()
	conn.close()
	messagebox.showinfo("SUCCESS", "Student info updated!")
	fetch_data()
	clear()

#kaningg delete na function is i delete rani niya ang info sa isa ka student na naka store sa table sa database

def delete():
	warning = messagebox.askquestion('WARNING','Are you sure you want to delete the following student info?',icon = 'warning')
	if warning == 'yes':
		conn = sqlite3.connect('SSISData.db')
		curr = conn.cursor()
		print(id_number.get())
		curr.execute("DELETE from data WHERE student_id=?",(id_number.get(),))
		conn.commit()
		conn.close()
		fetch_data()
		clear()
	else:
		pass



# kaning showCourses na function kay ichange niya ang structure sa table to cater to the Course_View

def showCourses():

	# altering the table columns
	student_table.delete(*student_table.get_children())
	student_table['columns'] = (1,2)
	student_table.heading(1, text="COURSE CODE")
	student_table.heading(2, text="COURSE NAME")

	student_table.column(1, width=100)
	student_table.column(2, width=500)

	# showing courses to the table
	fetch_data(caller='course')

	# changing input fields and their corresponding label
	code_lbl.grid(row=0, column=0, padx=2, pady=2)
	cname_lbl.grid(row=1, column=0, padx=2, pady=2)
	id_no_ent['width'] = 13
	name_ent['width'] = 13


	destroyWidgets()

	# altering signals
	delete_student_btn['command'] = delCourse
	add_student_btn['command'] = addCourse
	update_student_btn['command'] = updateCourse
	clear_student_btn['command'] = clear



def addCourse():
	ccode = id_number.get()
	cname = name_ent.get()

	if ccode == '' or cname == '':
		messagebox.showerror('Add Course', 'Please fill all the fields')

	elif ccode in database.CourseCodes():
		messagebox.showerror('Add Course', 'You entered an existing Course Code.')

	else:
		database.addCourse(ccode,cname)
		fetch_data(caller='course')


def delCourse():
	cursor_row = student_table.focus()
	content = student_table.item(cursor_row)
	row = content['values']
	if row != []:
		database.deleteCourse(ccode=row[0])
		fetch_data(caller='course')
		messagebox.showinfo('Delete Course', 'Course deleted.')
	else:
		messagebox.showinfo('Delete Course', 'Please select the course you want to be deleted.')

def updateCourse():
	cursor_row = student_table.focus()
	content = student_table.item(cursor_row)
	row = content['values']
	print(row)
	print(id_number.get(),name_ent.get())
	if row != []:
		database.updateCourse(id_number.get(), name_ent.get())
		fetch_data(caller='course')


def showStudents():
	student_table['columns'] = ("ID NUMBER", "NAME", "COURSE", "YEAR", "GENDER")
	student_table.heading("ID NUMBER", text="ID NUMBER")
	student_table.heading("NAME", text="NAME")
	student_table.heading("COURSE", text="COURSE")
	student_table.heading("YEAR", text="YEAR")
	student_table.heading("GENDER", text="GENDER")

	student_table['show'] = 'headings'

	student_table.column("ID NUMBER", width=200)
	student_table.column("NAME", width=200)
	student_table.column("COURSE", width=100)
	student_table.column("YEAR", width=100)
	student_table.column("GENDER", width=100)
	student_table.pack(fill=tk.BOTH, expand=True)
	fetch_data()

	# commands
	delete_student_btn['command'] = delete
	add_student_btn['command'] = add_student
	update_student_btn['command'] = update
	clear_student_btn['command'] = clear

	# removing the course_fields from the grid
	code_lbl.grid_forget()
	cname_lbl.grid_forget()

	# changing input fields width
	id_no_ent['width'] = 15
	name_ent['width'] = 15

	restateWidgets()


# this will remove the unnecessary fields and label when shifting to course_table
def destroyWidgets():
	id_no_lbl.grid_forget()
	name_lbl.grid_forget()
	course_lbl.grid_forget()
	course_ent.grid_forget()
	year_lbl.grid_forget()
	year_ent.grid_forget()
	gender_lbl.grid_forget()
	gender_ent.grid_forget()

# this will show the destroyedWidgets back to the screen when shifting back to student_table
def restateWidgets():
	id_no_lbl.grid(row=0, column=0, padx=2, pady=2)
	id_no_ent.grid(row=0, column=1, padx=2, pady=2)
	name_lbl.grid(row=1, column=0, padx=2, pady=2)
	name_ent.grid(row=1, column=1, padx=2, pady=2)
	course_lbl.grid(row=2, column=0, padx=2, pady=2)
	course_ent.grid(row=2, column=1, padx=2, pady=2)
	year_lbl.grid(row=3, column=0, padx=2, pady=2)
	year_ent.grid(row=3, column=1, padx=2, pady=2)
	gender_lbl.grid(row=4, column=0, padx=2, pady=2)
	gender_ent.grid(row=4, column=1, padx=2, pady=2)










#KANI DIRI MAO RANI ANG DESIGN SA BUTTONS


# ====  ANG DESIGN SA BUTTON ==== #
btn_frame = tk.Frame(detail_frame,bg=BACKGROUND_COLOR,bd=10,relief=tk.GROOVE)
btn_frame.place(x=20,y=300,width=300,height=165)


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

#==== show courses ====

show_courses_btn = tk.Button(btn_frame, bg='white',text="Courses",bd=7,font=("Arial",13),width=12, command=showCourses)
show_courses_btn.grid(row=2,column=0,padx=3,pady=2)

#==== show students ====

show_students_btn = tk.Button(btn_frame, bg='white',text="Students",bd=7,font=("Arial",13),width=12, command=showStudents)
show_students_btn.grid(row=2,column=1,padx=3,pady=2)



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
