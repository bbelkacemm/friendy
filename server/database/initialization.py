import json
from .models import *
from pathlib import Path
import pandas as pd


def save_data(data, lang):
    for index in reversed(range(len(data))):
        context = dict()
        patterns = []
        responses = []
        contexts = []

        current_context = data[index]
        context['code'] = current_context['code']
        context[f'label_{lang}'] = current_context['tag']
        context[f'proposition_{lang}'] = current_context['proposition'] if not pd.isnull(
            current_context['proposition']) else None

        for label in current_context['patterns']:
            patterns.append(Pattern(label=label, language=lang))
        for label in current_context['responses']:
            responses.append(Response(label=label, language=lang))
        for code in current_context['to']:
            c = Context.query.filter_by(code=code).first()
            if c is not None:
                contexts.append(c)

        # GET ADMINISTRATOR
        admin = database.session.query(User).filter_by(username='belkacem').first()
        # SAVE CONTRIBUTION
        contribution = Contribution(
            title='NO TITLE',
            status='valid',
            contributor_id=admin.id,
            validator_id=admin.id,
            validated_at=datetime.datetime.utcnow(),
            context=Context(
                code=context['code'],
                label_en=context['label_en'] if 'label_en' in context else None,
                label_fr=context['label_fr'] if 'label_fr' in context else None,
                label_ar=context['label_ar'] if 'label_ar' in context else None,
                proposition_en=context['proposition_en'] if 'proposition_en' in context else None,
                proposition_fr=context['proposition_fr'] if 'proposition_fr' in context else None,
                proposition_ar=context['proposition_ar'] if 'proposition_ar' in context else None,
                patterns=patterns,
                responses=responses,
                contexts=contexts,
            )
        )
        database.session.add(contribution)
        database.session.commit()


def initialize_database():
    # INITIALIZE ROLES
    if database.session.query(Role).count() == 0:
        roles = json.loads(open(f'{Path().absolute()}/server/database/data/roles.json').read())
        for role in roles:
            database.session.add(
                Role(
                    label=role['label'],
                    permissions=Permission.dict_to_permissions(role['permissions'])
                )
            )
            database.session.commit()

    # INITIALIZE USERS
    if database.session.query(User).count() == 0:
        # GET ADMINISTRATOR ROLE
        role = database.session.query(Role).filter_by(label='administrator').first()
        # CREATE AN ADMINISTRATOR
        belkacem = User(
            username='belkacem',
            password='123456789',
            first_name='Belkacem',
            last_name='Bouzerzour',
            birth_date='21-05-1997',
            gender='m',
            role_id=role.id
        )
        database.session.add(belkacem)
        database.session.commit()

    # INITIALIZE CONTRIBUTIONS
    if database.session.query(Context).count() == 0:
        en = json.loads(open(f'{Path().absolute()}/server/model/data/database_en.json').read())
        fr = json.loads(open(f'{Path().absolute()}/server/model/data/database_fr.json').read())
        ar = json.loads(open(f'{Path().absolute()}/server/model/data/database_ar.json').read())

        data = [
            {
                'lang': 'en',
                'contexts': en
            },
            {
                'lang': 'fr',
                'contexts': fr
            },
            {
                'lang': 'ar',
                'contexts': ar
            },
        ]

        for index in reversed(range(len(en))):
            contribution = dict()
            context = dict()
            patterns = []
            responses = []
            contexts = []

            contribution['title'] = data[0]['contexts'][index]['title']
            contribution['description'] = data[0]['contexts'][index]['description']
            contribution['date'] = data[0]['contexts'][index]['date']

            for collection in data:
                current_context = collection['contexts'][index]
                context['code'] = current_context['code']
                context[f'label_{collection["lang"]}'] = current_context['tag']
                context[f'proposition_{collection["lang"]}'] = current_context['proposition'] if not pd.isnull(
                    current_context['proposition']) else None

                for label in current_context['patterns']:
                    patterns.append(Pattern(label=label, language=collection['lang']))
                for label in current_context['responses']:
                    responses.append(Response(label=label, language=collection['lang']))
                for code in current_context['to']:
                    c = Context.query.filter_by(code=code).first()
                    if c is not None:
                        if c not in contexts:
                            contexts.append(c)

            # GET ADMINISTRATOR
            admin = database.session.query(User).filter_by(username='belkacem').first()
            # SAVE CONTRIBUTION
            contribution = Contribution(
                title=contribution['title'],
                description=contribution['description'],
                status='valid',
                contributor_id=admin.id,
                validator_id=admin.id,
                created_at=datetime.datetime.strptime(contribution['date'], '%Y-%m-%d'),
                validated_at=datetime.datetime.strptime(contribution['date'], '%Y-%m-%d'),
                context=Context(
                    code=context['code'],
                    label_en=context['label_en'] if 'label_en' in context else None,
                    label_fr=context['label_fr'] if 'label_fr' in context else None,
                    label_ar=context['label_ar'] if 'label_ar' in context else None,
                    proposition_en=context['proposition_en'] if 'proposition_en' in context else None,
                    proposition_fr=context['proposition_fr'] if 'proposition_fr' in context else None,
                    proposition_ar=context['proposition_ar'] if 'proposition_ar' in context else None,
                    patterns=patterns,
                    responses=responses,
                    contexts=contexts,
                )
            )
            database.session.add(contribution)
            database.session.commit()
