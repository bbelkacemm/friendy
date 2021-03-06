import datetime

import sqlalchemy.sql.functions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

database = SQLAlchemy()

related_contexts = database.Table(
    'related_contexts',
    Column('main_context_id', Integer, ForeignKey('contexts.id', ondelete='CASCADE'), primary_key=True),
    Column('related_context_id', Integer, ForeignKey('contexts.id', ondelete='CASCADE'), primary_key=True),
)


class Role(database.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    label = Column(String, unique=True)

    users = database.relationship('User')
    permissions = database.relationship('Permission', cascade='all')

    def as_dict(self):
        return dict({
            'id': self.id,
            'label': self.label,
            'permissions': [permission.as_dict() for permission in self.permissions],
        })


class Permission(database.Model):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    can_create_all = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_read_all = Column(Boolean, default=False)
    can_read = Column(Boolean, default=False)
    can_update_all = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete_all = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def as_dict(self):
        return dict({
            'id': self.id,
            'label': self.label,
            'canReadAll': self.can_read_all,
            'canRead': self.can_read,
            'canCreateAll': self.can_create_all,
            'canCreate': self.can_create,
            'canUpdateAll': self.can_update_all,
            'canUpdate': self.can_update,
            'canDeleteAll': self.can_delete_all,
            'canDelete': self.can_delete,
        })

    @staticmethod
    def dict_to_permissions(data):
        permissions = []
        for permission in data:
            permissions.append(Permission(
                label=permission['label'],
                can_create_all=permission['canCreateAll'],
                can_create=permission['canCreate'],
                can_read_all=permission['canReadAll'],
                can_read=permission['canRead'],
                can_update_all=permission['canUpdateAll'],
                can_update=permission['canUpdate'],
                can_delete_all=permission['canDeleteAll'],
                can_delete=permission['canDelete'],
            ))
        return permissions


class User(database.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    gender = Column(Enum('f', 'm', name="gender"))
    status = Column(Enum('valid', 'pending', 'invalid', name='user_status'), default='valid')
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = database.relationship('Role', back_populates='users')

    def as_dict(self):
        return dict({
            'id': self.id,
            'username': self.username,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'birthdate': self.birth_date,
            'gender': self.gender,
            'status': self.status,
            'role': self.role.as_dict(),
        })


class Contribution(database.Model):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum('pending', 'valid', 'invalid', name="contribution_status"), nullable=False, default='pending')
    contributor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    validator_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    validated_at = Column(TIMESTAMP)

    context = database.relationship('Context', uselist=False, back_populates='contribution', cascade='all')

    def as_dict(self):
        return dict({
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'context': self.context.as_dict(),
            'createdAt': self.created_at,
            'validatedAt': self.validated_at,
            'contributor': self.contributor.as_dict(),
            'validator': self.validator.as_dict() if self.validator else None
        })


User.contributions = database.relationship(
    'Contribution',
    foreign_keys=Contribution.contributor_id,
    back_populates='contributor'
)
User.validated_contributions = database.relationship('Contribution', foreign_keys=Contribution.validator_id)
Contribution.contributor = database.relationship(
    'User',
    back_populates='contributions',
    foreign_keys=Contribution.contributor_id
)
Contribution.validator = database.relationship(
    'User',
    back_populates='validated_contributions',
    foreign_keys=Contribution.validator_id
)


class Context(database.Model):
    __tablename__ = 'contexts'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    label_en = Column(String)
    label_fr = Column(String)
    label_ar = Column(String)
    proposition_en = Column(String)
    proposition_fr = Column(String)
    proposition_ar = Column(String)
    contribution_id = Column(Integer, ForeignKey('contributions.id'))

    contribution = database.relationship('Contribution', back_populates='context')
    patterns = database.relationship('Pattern', cascade='all')
    responses = database.relationship('Response', cascade='all')

    contexts = database.relationship(
        'Context',
        secondary=related_contexts,
        primaryjoin=(related_contexts.c.main_context_id == id),
        secondaryjoin=(related_contexts.c.related_context_id == id),
        cascade="all, delete",
    )

    def as_dict(self):
        return dict({
            "id": self.id,
            "code": self.code,
            "labelEn": self.label_en,
            "labelFr": self.label_fr,
            "labelAr": self.label_ar,
            "propositionEn": self.proposition_en,
            "propositionFr": self.proposition_fr,
            "propositionAr": self.proposition_ar,
            "patterns": [pattern.as_dict() for pattern in self.patterns],
            "responses": [response.as_dict() for response in self.responses],
            "contexts": [context.as_dict() for context in self.contexts],
        })

    @staticmethod
    def dict_to_contexts(data):
        contexts = []
        for item in data:
            contexts.append(Context(
                code=item['code'],
                label_en=item['label_en'],
                label_fr=item['label_fr'],
                label_ar=item['label_ar'],
                proposition_en=item['proposition_en'],
                proposition_fr=item['proposition_fr'],
                proposition_ar=item['proposition_ar'],
            ))
        return contexts


class Pattern(database.Model):
    __tablename__ = 'patterns'
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    language = Column(String, nullable=False)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=False)

    def as_dict(self):
        return dict({
            'id': self.id,
            'label': self.label,
            'language': self.language
        })

    @staticmethod
    def dict_to_patterns(data):
        patterns = []
        for item in data:
            patterns.append(Pattern(label=item['label'], language=item['language']))
        return patterns


class Response(database.Model):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    language = Column(String, nullable=False)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=False)

    def as_dict(self):
        return dict({
            'id': self.id,
            'label': self.label,
            'language': self.language
        })

    @staticmethod
    def dict_to_patterns(data):
        responses = []
        for item in data:
            responses.append(Response(label=item['label'], language=item['language']))
        return responses


class Model(database.Model):
    __tablename__ = 'models'
    path = Column(String, nullable=False, primary_key=True)
    state = Column(Enum('enabled', 'disabled', name="model_states"), nullable=False, default='disabled',
                   primary_key=True)
    tag = Column(Enum('dev', 'prod', 'none', name="model_tags"), nullable=False, default='none', primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sqlalchemy.sql.functions.now(), nullable=False)

    user = database.relationship('User', back_populates='models')

    def as_dict(self):
        return dict({
            'path': self.path,
            'state': self.state,
            'tag': self.tag,
            'createdAt': self.created_at,
            'user': self.user.as_dict(),
        })


User.models = database.relationship('Model')
