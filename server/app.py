import shutil

from pathlib import Path
from flask import Flask, jsonify, make_response
from flask import request
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from database.models import *
from database.initialization import initialize_database
from flask_cors import CORS
from model.use import generate_response
from model.train import train_model

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1278@localhost:5433/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 20

database.init_app(app)
migrate = Migrate(app, database)

app.app_context().push()

database.create_all()

initialize_database()


# CHAT
@app.route('/', methods=['GET'])
def chat():
    lang = request.args.get('lang')
    user_input = request.args.get('user-input')
    tag = request.args.get('tag')

    try:
        response = generate_response(user_input=user_input, lang=lang, tag=tag)
        return response, 200
    except ModuleNotFoundError as exception:
        return 'noModel', 400
    except Exception as exception:
        return 'responseError', 400


# DASHBOARD
@app.route('/dashboard/train', methods=['POST'])
def train():
    # TODO ADD FR, AR
    data = request.get_json()

    user_id = data['user_id']

    languages = ['en']
    for lang in languages:
        train_model(lang, user_id)
    return 'trainingCompleted', 200


# AUTHENTICATION
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        username = data['username']
        password = data['password']

        try:
            user = User.query.filter_by(username=username, password=password).first()
            return make_response(jsonify(user.as_dict()), 200)
        except Exception as exception:
            print(exception)
            return 'loginError', 400


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()

        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        birth_date = data['birth_date']
        gender = data['gender']

        try:
            role = Role.query.filter_by(label='client').first()
            database.session.add(User(username=username, password=password, first_name=first_name, last_name=last_name,
                                      birth_date=birth_date, gender=gender, role_id=role.id))
            database.session.commit()
            return 'signupSuccess', 201
        except Exception as exception:
            print(exception)
            return 'signupError', 400


# USERS
@app.route('/users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        try:
            users = database.session.query(User).all()
            return make_response(jsonify([x.as_dict() for x in users]), 200)
        except Exception as exception:
            print(exception)


# SAVE USER
@app.route('/users/user', methods=['POST'])
def save_user():
    if request.method == 'POST':
        data = request.get_json()

        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        birth_date = data['birth_date']
        gender = data['gender']
        role_id = data['role_id']

        try:
            user = User(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                gender=gender,
                role_id=role_id
            )
            database.session.add(user)
            database.session.commit()
            return user.as_dict(), 201
        except Exception as exception:
            print(exception)
            return 'addError', 400


# UPDATE USER
@app.route('/users/user/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        data = request.get_json()
        try:
            user = User.query.filter_by(id=id).first()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.birth_date = data['birth_date']
            user.gender = data['gender']
            user.role_id = data['role_id']
            database.session.commit()
            return user.as_dict(), 200
        except Exception as exception:
            print(exception)
            return 'updateError', 400


# DELETE USER
@app.route('/users/user/<id>', methods=['DELETE'])
def delete_user(id):
    if request.method == 'DELETE':
        try:
            user = User.query.filter_by(id=id).first()

            database.session.delete(user)
            database.session.commit()

            return 'OK', 200
        except SQLAlchemyError as exception:
            print(exception)
            return 'deleteErrorRelatedEntities', 400
        except Exception as exception:
            print(exception)
            return 'deleteError', 400


# ROLES
@app.route('/roles', methods=['GET'])
def get_roles():
    if request.method == 'GET':
        try:
            roles = database.session.query(Role).all()
            return make_response(jsonify([role.as_dict() for role in roles]), 200)
        except Exception as exception:
            print(exception)
            return 400


# SAVE ROLE
@app.route('/roles/role', methods=['POST'])
def save_role():
    if request.method == 'POST':
        try:
            data = request.get_json()

            label = data['label']

            permissions = Permission.dict_to_permissions(data['permissions'])

            role = Role(label=label, permissions=permissions)
            database.session.add(role)
            database.session.commit()
            return role.as_dict(), 201
        except Exception as exception:
            print(exception)
            return 'addError', 400


# UPDATE ROLE
@app.route('/roles/role/<id>', methods=['POST'])
def update_role(id):
    if request.method == 'POST':
        try:
            data = request.get_json()

            role = Role.query.filter_by(id=id).first()
            role.label = data['label']

            for permission in data['permissions']:
                if permission['status'] == 'edit':
                    p = Permission.query.filter_by(id=permission['id']).first()
                    p.label = permission['label']
                    p.can_create_all = permission['canCreateAll']
                    p.can_create = permission['canCreate']
                    p.can_read_all = permission['canReadAll']
                    p.can_read = permission['canRead']
                    p.can_update_all = permission['canUpdateAll']
                    p.can_update = permission['canUpdate']
                    p.can_delete_all = permission['canDeleteAll']
                    p.can_delete = permission['canDelete']
                elif permission['status'] == 'delete':
                    Permission.query.filter_by(id=permission['id']).delete()
                elif permission['status'] == 'add':
                    database.session.add(Permission(
                        label=permission['label'],
                        can_create=permission['canCreate'],
                        can_read=permission['canRead'],
                        can_update=permission['canUpdate'],
                        can_delete=permission['canDelete'],
                        role_id=id,
                    ))

            database.session.commit()
            return role.as_dict(), 200
        except Exception as exception:
            print(exception)
            return 'editError', 400


# DELETE ROLE
@app.route('/roles/role/<id>', methods=['DELETE'])
def delete_role(id):
    if request.method == 'DELETE':
        try:
            role = Role.query.filter_by(id=id).first()

            database.session.delete(role)
            database.session.commit()

            return 'OK', 200
        except SQLAlchemyError as exception:
            print(exception)
            return 400


# CONTRIBUTIONS
@app.route('/contributions', methods=['GET'])
def get_contributions():
    try:
        # TODO BASED ON THE ROLE
        result = database.session.query(Contribution).all()
        return make_response(jsonify([item.as_dict() for item in result]), 200)
    except SQLAlchemyError as exception:
        print(exception)
        return 400


# ADD CONTRIBUTION
@app.route('/contributions/contribution', methods=['POST'])
def context():
    if request.method == 'POST':
        try:
            data = request.get_json()

            patterns = Pattern.dict_to_patterns(data['patterns'])
            responses = Response.dict_to_patterns(data['responses'])

            r_contexts = []
            for code in data['relatedContexts']:
                r_contexts.append(Context.query.filter_by(code=code).first())

            user = database.session.query(User).filter_by(id=data['user_id']).first()

            contribution = Contribution(
                title=data['contribution']['title'],
                description=data['contribution']['description'],
                contributor_id=user.id,
                context=Context(
                    code=data['context']['code'],
                    label_en=data['context']['label_en'],
                    label_fr=data['context']['label_fr'],
                    label_ar=data['context']['label_ar'],
                    proposition_en=data['context']['proposition_en'],
                    proposition_fr=data['context']['proposition_fr'],
                    proposition_ar=data['context']['proposition_ar'],
                    patterns=patterns,
                    responses=responses,
                    contexts=r_contexts,
                )
            )

            database.session.add(contribution)
            database.session.commit()

            return contribution.as_dict(), 200
        except Exception as exception:
            print(exception)
            return 400


# UPDATE CONTRIBUTION
@app.route('/contributions/contribution/<id>', methods=['POST'])
def update_contribution(id):
    if request.method == 'POST':
        try:
            data = request.get_json()

            status = data.get('status', None)

            contribution = Contribution.query.filter_by(id=id).first()

            if status is None:
                r_contexts = []
                for code in data['relatedContexts']:
                    r_contexts.append(Context.query.filter_by(code=code).first())

                contribution.title = data['contribution']['title']
                contribution.description = data['contribution']['description']
                contribution.context.code = data['context']['code']
                contribution.context.label_en = data['context']['label_en']
                contribution.context.label_fr = data['context']['label_fr']
                contribution.context.label_ar = data['context']['label_ar']
                contribution.context.proposition_en = data['context']['proposition_en']
                contribution.context.proposition_fr = data['context']['proposition_fr']
                contribution.context.proposition_ar = data['context']['proposition_ar']

                for pattern in data['patterns']:
                    if pattern['status'] == 'edit':
                        p = Pattern.query.filter_by(id=pattern['id']).first()
                        p.label = pattern['label']
                        p.language = pattern['language']
                    elif pattern['status'] == 'delete':
                        Pattern.query.filter_by(id=pattern['id']).delete()
                    elif pattern['status'] == 'add':
                        database.session.add(Pattern(
                            label=pattern['label'],
                            language=pattern['language'],
                            context_id=contribution.context.id
                        ))

                for response in data['responses']:
                    if response['status'] == 'edit':
                        r = Response.query.filter_by(id=response['id']).first()
                        r.label = response['label']
                        r.language = response['language']
                    elif response['status'] == 'delete':
                        Response.query.filter_by(id=response['id']).delete()
                    elif response['status'] == 'add':
                        database.session.add(Response(
                            label=response['label'],
                            language=response['language'],
                            context_id=contribution.context.id
                        ))

                contribution.context.contexts = r_contexts
            else:
                contribution.status = status
                contribution.validator_id = data['user_id']
                contribution.validated_at = datetime.datetime.now()

            database.session.commit()

            return contribution.as_dict(), 200
        except SQLAlchemyError as exception:
            print(exception)
            return 400


# DELETE CONTRIBUTION
@app.route('/contributions/contribution/<id>', methods=['DELETE'])
def delete_contribution(id):
    if request.method == 'DELETE':
        try:
            contribution = Contribution.query.filter_by(id=id).first()

            database.session.delete(contribution)
            database.session.commit()

            return 'ok', 200
        except SQLAlchemyError as exception:
            print(exception)
            return 'deleteError', 400


# CONTEXTS BY STATUS
@app.route('/contexts/<status>', methods=['GET'])
def get_contexts(status):
    if request.method == 'GET':
        try:
            result = database.session.query(Contribution).filter_by(status=status).all()
            return make_response(jsonify([c.context.as_dict() for c in result]), 200)
        except SQLAlchemyError as exception:
            print(exception)
            return 400


@app.route('/models', methods=['GET'])
def get_models():
    if request.method == 'GET':
        try:
            models = Model.query.all()
            return make_response(jsonify([model.as_dict() for model in models]), 200)
        except SQLAlchemyError as exception:
            print(exception)
            return 400


# UPDATE MODEL
@app.route('/models/model/<path>', methods=['POST'])
def edit_model(path):
    if request.method == 'POST':
        data = request.get_json()

        state = data['state']
        tag = data['tag']

        try:
            model = Model.query.filter_by(path=path).first()
            if state is not None:
                model.state = state
                if model.state == 'disabled':
                    model.tag = 'none'
                if model.state == 'enabled' and model.tag == 'none':
                    model.tag = 'dev'
            if tag is not None:
                model.tag = tag

            database.session.commit()

            return model.as_dict(), 200
        except SQLAlchemyError as exception:
            print(exception)
            return 400


# DELETE MODEL
@app.route('/models/model/<path>', methods=['DELETE'])
def delete_model(path):
    if request.method == 'DELETE':
        try:
            model = Model.query.filter_by(path=path).first()

            database.session.delete(model)
            database.session.commit()

            # DELETE FOLDER USING PATH
            shutil.rmtree(f'{Path().absolute()}/server/model/output/{path}')

            return 'OK', 200
        except SQLAlchemyError as exception:
            print(exception)
            return 400


if __name__ == '__main__':
    app.run()
