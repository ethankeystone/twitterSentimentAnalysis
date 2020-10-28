from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import datetime
import tensorflow as tf
from tensorflow import keras

import generalUtil
import random
import os
import TweepyTest
cwd = os.getcwd()

TweepyTest.generateDailyTwitterData(200,tweetName, consumer_key, consumer_secret, access_token, access_token_secret)
for i in range(1):
    data = generalUtil.writefromCSVFile('training.1600000.processed.noemoticon.csv')
    #data = open('training.1600000processed.noemoticon.csv',encoding="utf8")

    trainDF = pandas.DataFrame()
    texts, labels = [], []


    for i in range(len(data)):
        texts.append(data[i][5])
        labels.append(data[i][0])


    trimData = generalUtil.generateSubsetArray(data, 60000)

    texts, labels = [], []

    for i in range(len(trimData)):
        texts.append(trimData[i][1])
        labels.append(trimData[i][0])


    trainDF['text'] = texts
    trainDF['label'] = labels

    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])


    encoder = preprocessing.LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    valid_y = encoder.fit_transform(valid_y)

    # create a tokenizer
    token = text.Tokenizer()
    token.fit_on_texts(trainDF['text'])
    word_index = token.word_index

    train_seq_x = sequence.pad_sequences(token.texts_to_sequences(train_x), maxlen=70)
    valid_seq_x = sequence.pad_sequences(token.texts_to_sequences(valid_x), maxlen=70)

    embeddings_index = {}
    for i, line in enumerate(open('wiki-news-300d-1M.vec',encoding="utf8")):
        values = line.split()
        embeddings_index[values[0]] = numpy.asarray(values[1:], dtype='float32')

    # create token-embedding mapping
    embedding_matrix = numpy.zeros((len(word_index) + 1, 300))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    vocab_size = len(word_index) + 1

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['acc'])


    checkpoint_dir = 'C:\\Users\\ethan\\Dropbox\\Ethan\'s Programs\\TensorFlow Test\\Machine Learning Testing\\Test Twitter Sentiment Analysis\\checkpoints'

    # Create checkpoint callback
    #cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,

    history = model.fit(train_seq_x,
                        train_y,
                        epochs=5,
                        batch_size=512,
                        validation_data=(valid_seq_x, valid_y),
                        verbose=1)

    date = datetime.datetime.today()
    dateString = (str(date.month) + '-' + str(date.day) + '-' + str(date.year))

    temp = generalUtil.writefromCSVFile(cwd + '\\All Twitter Data\\' + tweetName + dateString + '.csv')
    count = 0
    for i in range(len(temp)):
            if(temp[i - count] == []):
                del temp[i - count]
                count += 1

    evaldata = []

    for i in range(len(temp)):
        evaldata.append(temp[i][0])

    evaldata_seq_x = sequence.pad_sequences(token.texts_to_sequences(evaldata), maxlen=70)

    evaldata_seq_y = model.predict(evaldata_seq_x)

    generalUtil.uploadToGoogleSheets(evaldata_seq_x, evaldata_seq_y, i, tweetName)
