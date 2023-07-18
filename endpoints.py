from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def home():
    return "Welcome Home"

class Student_details(db.Model):
    id=db.Column(db.Integer, nullable=False, unique=True,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    standard=db.Column(db.String(5),nullable=False)
    parent=db.relationship('Parent_details',backref='student',lazy=True)
    con = db.relationship('Contact_details', backref='contacts',uselist=False, lazy=True)

    def __repr__(self):
        return f'{self.name}-{self.standard}'

class Parent_details(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    father=db.Column(db.String(30),nullable=False)
    mother = db.Column(db.String(30), nullable=False)
    stu_id=db.Column(db.Integer,db.ForeignKey('student_details.id'),nullable=False,unique=True)
    # studet=db.relationship('Student_details',backref='parents')

    def __repr__(self):
        return f'{self.father}-{self.mother}'

class Contact_details(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    address=db.Column(db.String(230),nullable=False)
    mobile=db.Column(db.Integer,nullable=False)
    cont_id = db.Column(db.Integer, db.ForeignKey('student_details.id'), nullable=False)
    contact = db.relationship('Student_details', backref='contacts_')

    def __repr__(self):
        return f'{self.address}-{self.mobile}'

@app.route('/students',methods=['GET','POST'])
def stu_det():
    if request.method=='POST':
        stu=Student_details(name=request.json['name'],standard=request.json['standard'])
        db.session.add(stu)
        db.session.commit()
        return f'{stu.id}'
    else:
        stu=Student_details.query.all()
        stu_dict_list = [{'id': stu.id, 'name': stu.name, 'standard': stu.standard} for stu in stu]
        return jsonify(stu_dict_list)

@app.route('/parents',methods=['GET','POST'])
def parents():
    if request.method=='POST':
        p_detials=Parent_details(father=request.json['father'],mother=request.json['mother'],stu_id=request.json['stu_id'])
        db.session.add(p_detials)
        db.session.commit()
        return f'{p_detials.father}, {p_detials.mother} were added to student with id {p_detials.stu_id}'
    else:
        p_details=Parent_details.query.all()
        p_dict=[{'father': p_details.father,'mother':p_details.mother,'student':p_details.stu_id} for p_details in p_details]
        return jsonify(p_dict)


@app.route('/del/<id>',methods=['DELETE'])
def del_entries(id):
    del_stu=Student_details.query.filter_by(id=id).delete()
    del_par=Parent_details.query.filter_by(stu_id=id).delete()
    db.session.commit()
    return f'The account {id} deleted succesfully'

@app.route('/deleteall', methods=['DELETE'])
def del_all():
    del_stu = Student_details.query.delete()
    del_par = Parent_details.query.delete()
    del_con= Contact_details.query.delete()
    db.session.commit()
    return f'All accounts were deleted succefully'





if __name__=='__main__':
    app.run(debug=True)
