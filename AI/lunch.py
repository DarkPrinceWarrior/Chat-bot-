import json

import random

import lunch as lunch

import AI.nltk_utils
import numpy as np
import os

from AI import nltk_utils
from AI.model import model_create, model_compile, model_fit, K_fold_validation

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.utils.np_utils import to_categorical


class Model:

    def jsonOpen(self):
        with open('AI/dataset/intents.json', 'r') as f:
            intents = json.load(f)
        return intents

    def prepare_train_labels(self):

        intents = self.jsonOpen()
        for intent in intents['intents']:
            tag = intent['tag']
            self.tags.append(tag)
            for pattern in intent['patterns']:
                w = nltk_utils.tokenize(pattern)
                self.all_words.extend(w)
                self.results.append((w, tag))

        ignore_words = ['.', '?', '!', ',']

        self.all_words = [nltk_utils.stemming(w) for w in self.all_words
                     if w not in ignore_words]
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(self.tags)


        random.shuffle(self.results)

        for (pattern_sentence, tag) in self.results:
            # X: bag of words for each pattern_sentence
            bag = nltk_utils.bag_of_words(pattern_sentence, self.all_words)
            self.x_train.append(bag)
            label = self.tags.index(tag)
            self.y_train.append(label)

        self.x_train = np.array(self.x_train)
        self.y_train = to_categorical(self.y_train, 7)

        # create the NN model
        self.input_size = len(self.all_words)
        # number of hidden neurons
        self.hidden_size = 128
        # number of output neurons
        self.output_size = 7
        self.loss = "categorical_crossentropy"
        self.metrics = "accuracy"
        self.epochs = 400
        self.batch_size = 20

        self.model = self.build_model(self.x_train, self.y_train,
                                      self.input_size, self.hidden_size,
                                      self.output_size,
                                      self.loss, self.metrics, self.epochs,
                                      self.batch_size)


    def getResponse(self,tag):
        answer = "some answer"
        intents = self.jsonOpen()
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                responses = intent["responses"]
                i = random.randint(0,len(responses)-1)
                print(i)
                answer = responses[i]
                break
        return answer



    def __init__(self):
        self.loss = "categorical_crossentropy"
        self.metrics = "accuracy"
        self.epochs = 200
        self.batch_size = 20
        self.input_size = 0
        self.hidden_size = 0
        self.output_size = 0
        self.x_train = []
        self.y_train = []
        self.all_words = []
        self.tags = []
        self.results = []
        self.model = None

    def build_model(self, x_train, y_train, input_size, hidden_size, output_size,
                    loss, metrics, epochs,
                    batch_size):

        # create the model
        self.model = model_create(input_size, hidden_size, output_size)

        # compile the model
        self.model = model_compile(self.model, loss, metrics)

        # fit the model and get the results

        x_val = x_train[:30]
        partial_x_train = x_train[30:]

        y_val = y_train[:30]
        partial_y_train = y_train[30:]

        self.model.fit(partial_x_train,
                       partial_y_train,
                       epochs=epochs,
                       batch_size=batch_size,
                       validation_data=(x_val, y_val), shuffle=True, verbose=1)

        return self.model

    def getModel(self):
        return self.model
