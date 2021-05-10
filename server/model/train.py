import os
import random
import string
import pickle
import numpy as np
import nltk
from pathlib import Path
from server.database.models import *
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD

# nltk.download()

IGNORED_LETTERS = [p for p in string.punctuation]

lemmatizer = WordNetLemmatizer()


def get_classes(lang):
    """
    Retrieve contexts' labels from the database

    :param lang: label's language
    :return: a sorted list of labels
    """
    classes = []
    if lang == 'en':
        classes = [context[0] for context in Context.query.with_entities(Context.label_en).all()]
    elif lang == 'fr':
        classes = [context[0] for context in Context.query.with_entities(Context.label_fr).all()]
    elif lang == 'ar':
        classes = [context[0] for context in Context.query.with_entities(Context.label_ar).all()]
    return sorted(classes)


def get_patterns(lang):
    """
    Retrieve contexts' patterns from the database

    :param lang: patterns' language
    :return: a list of patterns
    """
    return [pattern[0]
            for pattern in
            Pattern.query.with_entities(Pattern.label, Pattern.language).filter(Pattern.language == lang).all()]


def get_words(patterns):
    """
    Tokenize patterns
    Remove ignored letters

    :param patterns: a list of patterns
    :return: sorted set of words
    """
    words = []
    for pattern in patterns:
        words.extend(nltk.word_tokenize(pattern))
    words = [lemmatizer.lemmatize(word) for word in words if word not in IGNORED_LETTERS]
    return sorted(set(words))


def get_label(lang, context):
    """
    :param lang: label's language
    :param context: Context object
    :return: context's label based on the specified language
    """
    label = ''
    if lang == 'en':
        label = context.label_en
    elif lang == 'fr':
        label = context.label_fr
    elif lang == 'ar':
        label = context.label_ar
    return label


def train_model(lang):
    """
    Prepare data,
    save words/classes,
    train model,
    save model.

    :return: None
    """

    # PREPARE DATA
    classes = get_classes(lang=lang)
    patterns = get_patterns(lang)
    words = get_words(patterns)

    # GENERATE DOCUMENTS
    documents = []
    for context in Context.query.all():
        for pattern in filter(lambda p: p.language == lang, context.patterns):
            documents.append((nltk.word_tokenize(pattern.label), get_label(lang, context)))

    # PREPARE TRAINING DATA
    training = []
    for document in documents:
        input_representation = np.zeros(len(words))
        output_representation = np.zeros(len(classes))
        for word in words:
            if word in document[0]:
                input_representation[words.index(word)] = 1
        output_representation[classes.index(document[1])] = 1
        training.append([input_representation, output_representation])

    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    # SAVE WORDS/CLASSES
    if not os.path.exists('server/model/output'):
        os.mkdir('server/model/output')
    pickle.dump(words, open(f'{Path().absolute()}/server/model/output/words_{lang}.pkl', 'wb'))
    pickle.dump(classes, open(f'{Path().absolute()}/server/model/output/classes_{lang}.pkl', 'wb'))

    # CREATE/TRAIN/SAVE MODEL
    model = Sequential()

    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(learning_rate=0.01)

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    result = model.fit(x=np.array(train_x), y=np.array(train_y), batch_size=4, epochs=200, verbose=1)
    model.save(f'{Path().absolute()}/server/model/output/model_{lang}.h5', result)
