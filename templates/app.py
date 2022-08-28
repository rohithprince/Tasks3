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


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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


class EmpListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date_created')


# instantiate schema objects
emplist_schema = EmpListSchema(many=False) #one emp
emplists_schema = EmpListSchema(many=True) #all emp

@app.route("/")



@app.route("/emplist", methods = ["POST"])
def add_emp():
    try:
        name = request.json['name']
        description = request.json['designation']

        new_emp = EmpList(name=name, description=description)
        
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

if __name__=="__main__":
    app.run(debug=True)
