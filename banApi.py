####################################################################################################
#Standard imports

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields


####################################################################################################
#Instantiation of flask and the REST-Plus API

app = Flask(__name__)
api = Api(app, title='NBRP Germplasm', description='A sample database of the Musa cultivars')

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/ban'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True

#####################################################################################################
#API models of users and crops

api_NewUser = api.model('New_User', {
    'name' : fields.String(description='User name'),
    'password' : fields.String(description='User pasword to access archive'),
    'admin' : fields.Boolean(False)
    })

apiUser = api.model('User', {
    'name' : fields.String(description='An existing api user')
})

apiNewCrop = api.model('New_Crop', {
    'name' : fields.String(50, description = 'A new crop in the database'),
    'genus' : fields.String(50),
    'data_entrant' : fields.Integer(5)
})

apiCrop = api.model('Crop', {
    'name' : fields.String(50, description = 'An existing crop in the database')
})

#######################################################################################################
#Instantiation and definition of database models for persistent storage in a Postgres db

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__: 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    crops = db.relationship('Crop', backref = db.backref('crop'))

class Crop(db.Model):

    __tablename__: 'crop'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    genus = db.Column(db.String(50))

    data_entrant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
#######################################################################################################
#######################################################################################################

#Definition of user routes

@api.route('/user')
class Users(Resource):
    
    @api.expect(api_NewUser)
    def post(self):
        '''
        Create a new user in the database
        '''
        new_user = User(name=api.payload['name'], password=api.payload['password'], admin=False)

        db.session.add(new_user)
        db.session.commit()
        return {'message':'new user added!'}

    def get(self):
        '''
        Get all users in the database
        '''
        ban_users = User.query.all()
        
        output = []

        for user in ban_users:
            user_data = {}
            user_data['name'] = user.name
            user_data['password'] = user.password
            output.append(user_data)

        return {'users' : output}

    @api.expect(apiUser)
    def put(self):
        '''
        Update user details 
        '''
        
        user_name = api.payload['name']
        user = User.query.filter_by(name=user_name).first()

        if not user:
            return {'message' : 'no user found'}

        user.admin = True
        db.session.commit()
        return {'message' : 'The user has been promoted'}
        
    @api.expect(apiUser)
    def delete(self):
        '''
        Remove user from database
        '''
        user_name = api.payload['name']
        user = User.query.filter_by(name=user_name).first()

        if not user:
            return {'message' : 'no user found'}
        
        db.session.delete(user)
        db.session.commit()
        return {'message' : 'User deleted'}

#######################################################################################################
#Definition of crops routes 

@api.route('/crops')
class Crops(Resource):
    
    @api.expect(apiNewCrop)
    def post(self):
        '''
        Add a crop 
        '''
        new_crop = Crop(name = api.payload['name'], genus = api.payload['genus'])

        db.session.add(new_crop)
        db.session.commit()

        return {'message' : 'New crop added!'}

    @api.expect(apiCrop)
    def put(self):
        '''
        Edit a crop's details
        '''
        
        return ''

    def get(self):
        '''
        Retrieve all the crops
        '''
        
        crops_list = Crop.query.all()

        output = []

        for crop in crops_list:
            crop_data = {}
            crop_data['name'] = crop.name
            crop_data['genus'] =  crop.genus
            output.append(crop_data)
        
        return {'crops' : output}

    @api.expect(apiCrop)
    def delete(self):
        '''
        Remove a crop from the records
        '''
        crop_name = api.payload['name']
        crop = User.query.filter_by(name=crop_name).first()

        if not crop:
            return {'message' : 'no crop found'}
        
        db.session.delete(crop)
        db.session.commit()
        return {'message' : 'User deleted'}
        
if __name__ == '__main__':
    app.run(debug=True)