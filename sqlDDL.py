import sqlite3

conn = sqlite3.connect('SSISData.db')
cur = conn.cursor()


statement = [
'''
CREATE TABLE courses (
course_code VARCHAR(10) PRIMARY KEY,
course_name VARCHAR(50) Not Null
)
''',
'''
CREATE TABLE data (
student_id VARCHAR(9) PRIMARY KEY,
name VARCHAR(50) Not Null,
course VARCHAR(50) Not Null,
year INT Not Null,
gender VARCHAR(10) Not Null,
FOREIGN KEY (course) REFERENCES courses(course_code)
)
'''
]

def create_table(query=None):
    cur.execute(query)
    conn.commit()

for i in statement:
    create_table(i)
