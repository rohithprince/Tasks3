from ssl import AlertDescription
from flask import Flask, jsonify, request, make_response,render_template,request
from flask_sqlalchemy import SQLAlchemy #database
from flask_marshmallow import Marshmallow #schema
from datetime import datetime
from flask_cors import CORS, cross_origin



app=Flask(__name__)
CORS(app)
cors=CORS(app,resources={
    r"/*":{
        "origins":"*"
    }
})


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# create db instance
db = SQLAlchemy(app)

# instanctiate ma
ma = Marshmallow(app)

#create db
class EmpList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(300), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    age = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.Integer(), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    joinlocation = db.Column(db.String(100), nullable=True)


class EmpListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date_created', 'age', 'salary', 'address', 'state', 'joinlocation')


# instantiate schema objects
emplist_schema = EmpListSchema(many=False) #one emp
emplists_schema = EmpListSchema(many=True) #all emp

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uipost",methods=["GET","POST"])
def post_emp():
    if request.method=="POST":
        name=request.form["name"]
        description=request.form["desig"]
        new_emp = EmpList(name=name, description=description)
        
        db.session.add(new_emp)
        db.session.commit()

        return render_template("index.html")

    else:
        return render_template("insert.html")

@app.route("/emplist", methods = ["POST"])
def add_emp():
    try:
        name = request.json['name']
        description = request.json['designation']
        age = request.json['age']
        salary = request.json['salary']
        address = request.json['address']
        state = request.json['state']
        joinlocation = request.json['joinlocation']
        new_emp = EmpList(name=name, description=description, age=age, salary=salary, address=address, state=state, joinlocation=joinlocation)
        
        db.session.add(new_emp)
        db.session.commit()

        return emplist_schema.jsonify(new_emp)
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

@app.route("/emplist", methods = ["GET"])
def get_emps():
    emps = EmpList.query.all()
    result_set = emplists_schema.dump(emps)
    return jsonify(result_set)

@app.route("/emplist/update",methods=["POST","GET"])
def up_emp():
    if request.method=="POST":
        id=request.form["up"]
        emp = EmpList.query.get_or_404(int(id))
        name = request.form["upname"]
        description = request.form["updesig"]
        #completed = request.json['completed']

        emp.name = name
        emp.description = description
        #todo.completed = completed

        db.session.commit()
        return render_template("index.html")
    

    else:
        return render_template("update.html")

# update
@app.route("/emplist/put/<int:id>", methods=["PUT"])
def update_emp(id):

    emp = EmpList.query.get_or_404(int(id))

    try:
        name = request.json['name']
        description = request.json['designation']
        emp.name = name
        emp.description = description
        db.session.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})
        
    return emplist_schema.jsonify(emp)


# delete
@app.route("/emplist/delete/<int:id>", methods=["DELETE"])
def delete_emp(id):
    emp = EmpList.query.get_or_404(int(id))
    db.session.delete(emp)
    db.session.commit()
    #return jsonify({"Success" : "Emp deleted."})

@app.route("/emplist/delete",methods=["GET","POST"])
def del_emp():
    if request.method=="POST":
        id=request.form["del"]
        emp = EmpList.query.get_or_404(int(id))
        db.session.delete(emp)
        db.session.commit()
        return render_template("index.html")

    else:
        return render_template("delete.html")

if __name__=="__main__":
    app.run(debug=True)
