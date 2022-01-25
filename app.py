from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from rdflib import XSD, URIRef, Literal, Graph, RDF

app = Flask('scheduler')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:tecrur-rusjic-qEsgy8@central-db.ctxuo4jlqpyv.eu-central-1.rds.amazonaws' \
                                 '.com:3306/mcsw'
CORS(app)
db = SQLAlchemy(app)


# _______Models_______
class Museum(db.Model):
    __tablename__ = "museums"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    museumURI = db.Column(db.String(200))
    museumAbstract = db.Column(db.String(1000))
    museumGeo = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, museumURI, museumAbstract = "", museumGeo = ""):
        self.museumURI = museumURI
        self.museumAbstract = museumAbstract
        self.museumGeo = museumGeo

    def __repr__(self):
        return '' % self.id


db.create_all()


# _______Schema_______
class MuseumSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Museum
        sql_session = db.session

    museumURI = fields.String(required=True)
    museumAbstract = fields.String(required=True)
    museumGeo = fields.String(required=True)


# _______Routes_______
@app.route('/museums', methods=['GET'])
def get_all_museums():
    get_teachers = Museum.query.all()
    museum_schema = MuseumSchema(many=True)
    museums = museum_schema.dump(get_teachers)
    return make_response(jsonify({"museums": museums}))


@app.route('/museums/<id>', methods=['GET'])
def get_museum_by_id(id):
    get_museum = Museum.query.get(id)
    museum_schema = MuseumSchema()
    museum = museum_schema.dump(get_museum)
    return make_response(jsonify({"museum": museum}))


@app.route('/museums/<id>', methods=['PUT'])
def update_museum_by_id(id):
    data = request.get_json()
    get_museum = Museum.query.get(id)
    if data.get('id'):
        get_museum.id = data['id']
    db.session.add(get_museum)
    db.session.commit()
    museum_schema = MuseumSchema(only=['id', 'museumURI'])
    museum = museum_schema.dump(get_museum)
    return make_response(jsonify({"museum": museum}))


@app.route('/museums/<id>', methods=['DELETE'])
def delete_teacher_by_id(id):
    get_museum = Museum.query.get(id)
    db.session.delete(get_museum)
    db.session.commit()
    return make_response("", 204)


@app.route('/museums/', methods=['POST'])
def create_museum():
    data = request.get_json(force=True)
    museum_schema = MuseumSchema()
    museum = Museum(data.get("museumURI"))
    result = museum_schema.dump(museum.create())
    return make_response(jsonify({"museum": result}), 200)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/findMuseumsURIs/<city>')
def findMuseumsURIs(city):
    g = Graph()
    g.parse('http://dbpedia.org/resource/' + city)
    museums = []

    for s, p, o in g:
        if o.find("Museum") != -1 and isinstance(o, URIRef):
            museums.append(o)

    for o in museums:
        if o.find('jpeg') == -1 and o.find('png') == -1 and o.find('jpg') == -1:
            museum_schema = MuseumSchema()
            museum = Museum(o.n3())
            museum_schema.dump(museum.create())

    return 'Done'


@app.route('/fetchMuseumsInformation')
def fetchMuseumsInformation():

    museums = Museum.query.all()
    for museum in museums:
        museumData = Graph()
        museumData.parse(museum.museumURI[1:len(museum.museumURI) - 1])
        for c, p, o in museumData:
            try:
                if p.find('abstract') != -1 and o.language.find('en') != -1:
                    museum.museumAbstract = o.value
                    db.session.add(museum)
                    db.session.commit()
                    print(c, p, o)
            except:
                print('exception')
            # print(isinstance(c, Literal), p.find("abstract") != -1, isinstance(o, Literal))
            # if isinstance(o, Literal) and p.find("abstract") != -1:
            #     museumAbstract.language = o.language
            #     museumAbstract.abstract = o.value
            #     print(museumAbstract.language, museumAbstract.abstract)
    return 'Done'


    # for s in museums:
    #     if isinstance(s, URIRef):
    #         try:
    #             museumData = Graph()
    #             print(s)
    #             museumData.parse(s)
    #             for c, p, o in museumData:
    #                 print(c, p, o)
    #                 print(isinstance(c, Literal), p.find("abstract") != -1, isinstance(o, Literal))
    #                 if isinstance(o, Literal) and p.find("abstract") != -1:
    #                     museumAbstract.language = o.language
    #                     museumAbstract.abstract = o.value
    #                     print(museumAbstract.language, museumAbstract.abstract)
    #
    #         except:
    #             print("ValueError")
    # return 'getMuseums'


if __name__ == '__main__':
    app.run()
