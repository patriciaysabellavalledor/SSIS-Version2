import sqlite3

conn = sqlite3.connect('SSISData.db')
cur = conn.cursor()


def CourseCodes():
    cur.execute('SELECT course_code FROM courses')
    courses = cur.fetchall()
    courses = [i[0] for i in courses]
    return courses

def allCourses():
    cur.execute('SELECT course_code, course_name FROM courses')
    return cur.fetchall()


def addCourse(ccode=None, cname=None):
    cur.execute('INSERT INTO courses (course_code, course_name) VALUES("%s","%s")' %(ccode, cname))
    conn.commit()
    return

def deleteCourse(ccode=None):
    cur.execute('DELETE FROM courses WHERE course_code =  "%s"' %ccode)
    conn.commit()
    return

def updateCourse(code=None, name=None):
    cur.execute('UPDATE courses SET course_code = "%s", course_name = "%s" WHERE course_code = "%s"' %(code,name,code))
    conn.commit()
    return




