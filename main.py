from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging as lg



app = Flask(__name__)
app.secret_key = "Secret Key"
#lg.basicConfig(filename='Employee_data.log', level=lg.INFO,  format='%(asctime)s %(message)s', filemode='w')
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jazz@localhost/EmpData1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    dept = db.Column(db.String(100))


    def __init__(self, name, age, dept):

        self.name = name
        self.age = age
        self.dept = dept

class Dept(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Dept_Name=db.Column(db.String(100))

    def __init__(self,Dept_Name):
        self.Dept_Name=Dept_Name




#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)


#this route is for inserting Deptarment to mysql database via html forms
@app.route('/dept_insert',methods=['GET','POST'])
def dept_insert():
    if request.method=='POST':
        Dept_Name = request.form['Dept_Name'].replace['']

        my_dept=Dept(Dept_Name)
        db.session.add(my_dept)
        db.session.commit()

        flash('Department Inserted Succesfully')
        return redirect(url_for('Index'))


#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        dept = request.form['dept']


        my_data = Data(name, age, dept)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.age = request.form['age']
        my_data.dept = request.form['dept']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    lg.info("Everything is exectued in proper manner")
    app.run(debug=True)