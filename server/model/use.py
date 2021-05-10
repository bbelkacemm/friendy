import random
import pickle
import nltk
import numpy as np
from pathlib import Path
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from server.database.models import *

ERROR_THRESHOLD = 0.25

lemmatizer = WordNetLemmatizer()


def get_label(lang, context):
    """
    :param lang: label's language
    :param context: Context object
    :return: context's label based on the specified language
    """
    label = None
    if lang == 'en':
        label = context.label_en
    if lang == 'fr':
        label = context.label_fr
    if lang == 'ar':
        label = context.label_ar
    return label


def get_proposition(lang, context):
    """
    :param lang: proposition's language
    :param context: Context object
    :return: context's proposition based on the specified language
    """
    proposition = None
    if lang == 'en':
        proposition = context.proposition_en
    if lang == 'fr':
        proposition = context.proposition_fr
    if lang == 'ar':
        proposition = context.proposition_ar
    return proposition


def predict_class(user_input, model, words, classes):
    """
    Takes the user input,
    transform it to numeric values,
    then feed it to the model,
    finally return each class with its respective probability.

    :param user_input: user's message
    :param model: loaded model
    :param words: list of words used while training the model
    :param classes: list of classes used while training the model
    :return: a dictionary in the format of { 'class': '', 'probability': '' }
    """
    input_words = [lemmatizer.lemmatize(word) for word in nltk.word_tokenize(user_input)]
    input_representation = np.zeros(len(words))
    for input_word in input_words:
        for index, word in enumerate(words):
            if input_word == word:
                input_representation[index] = 1
    probabilities = []
    for index, probability in enumerate(model.predict(np.array([input_representation]))[0]):
        if probability > ERROR_THRESHOLD:
            probabilities.append([index, probability])
    probabilities.sort(key=lambda x: x[1], reverse=True)
    result = []
    for probability in probabilities:
        result.append({
            'class': classes[probability[0]],
            'probability': str(probability[1])
        })
    return result


def generate_response(user_input, lang):
    """
    Loads model/data based on the user's preferred language from the database,
    call @predict_class function,
    generate a response randomly using the 'label' related to the highest probability.

    :param user_input: the user's message
    :param lang: the language chosen by the user
    :return: an object containing the response and the recommended prepositions
    """
    # LOAD NECESSARY DATA
    words = pickle.load(open(f'{Path().absolute()}/server/model/output/words_{lang}.pkl', 'rb'))
    classes = pickle.load(open(f'{Path().absolute()}/server/model/output/classes_{lang}.pkl', 'rb'))
    # LOAD MODEL
    model = load_model(f'{Path().absolute()}/server/model/output/model_{lang}.h5')
    # PREDICT CLASS
    predictions = predict_class(user_input, model, words, classes)
    response = 'Error'
    next_contexts = []
    for context in Context.query.all():
        if get_label(lang=lang, context=context) == predictions[0]['class']:
            responses = list(filter(lambda x: x.language == lang, context.responses))
            response = random.choice(responses).label
            next_contexts = context.contexts

    return {
        'response': response,
        'propositions': list(map(lambda x: get_proposition(lang=lang, context=x), next_contexts))
    }
