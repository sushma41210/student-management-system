from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def home():

    search = request.args.get('search')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        """, ('%' + search + '%',))

    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return render_template('index.html', students=students)


# ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        rollno = request.form['rollno']
        department = request.form['department']
        marks = request.form['marks']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO students
        (name, rollno, department, marks)
        VALUES (?, ?, ?, ?)
        """, (name, rollno, department, marks))

        connection.commit()
        connection.close()

        return redirect('/')

    return render_template('add.html')


# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    connection.commit()
    connection.close()

    return redirect('/')


# EDIT STUDENT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # UPDATE DATA
    if request.method == 'POST':

        name = request.form['name']
        rollno = request.form['rollno']
        department = request.form['department']
        marks = request.form['marks']

        cursor.execute("""
        UPDATE students
        SET name=?, rollno=?, department=?, marks=?
        WHERE id=?
        """, (name, rollno, department, marks, id))

        connection.commit()
        connection.close()

        return redirect('/')

    # FETCH EXISTING STUDENT
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))

    student = cursor.fetchone()

    connection.close()

    return render_template('edit.html', student=student)


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)