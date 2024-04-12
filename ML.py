import nltk
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
import tensorflow as tf
import numpy as np
import sys
sys.dont_write_bytecode = True
import random
import speech_recognition as sr
from gtts import gTTS
import os
from nltk.stem import WordNetLemmatizer
import json
import assets.config as config
import playsound
from openai import OpenAI

client = OpenAI(api_key="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")

lemmatizer = WordNetLemmatizer()

r = sr.Recognizer()

def voice_command_processor(ask=False):
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source,phrase_time_limit=4) #odposlech z mikrofonu
        text = '' #preset pro řečenou frázi
        try:
            text=r.recognize_google(audio)
            if text == '': #pokud bude ticho tak bude ai ignorovat
                print('')
            else:
                print(f"User: {text}") #zobrazí frázi řečenou uživatelem
        except:
            pass
        return text.lower()

def audio_playback(text):
    text = text
    language = 'cs'#jazyk hlasové výslovnosti
    voice = gTTS(text=text, lang=language) #vytvoření hlasového modelu
    voice.save("Voice.mp3") # uložení hlasového modelu
    playsound.playsound("Voice.mp3") #přehrání hlasového modelu
    print(text) #zobrazení řečeného text
    

# #otevření přednastavených frází ze kterých se bude AI učit
# with open("assets/intents/intents.json") as file:
#     data = json.load(file) #načtě intents.json


# words = []
# classes = []
# documents = []
# ignore_chars = ["?", "!", ".", ","]

# for intent in data["intents"]:
#     for pattern in intent["patterns"]:
#         word_list = nltk.word_tokenize(pattern)
#         words.extend(word_list)
#         documents.append((word_list, intent["tag"]))
#         if intent["tag"] not in classes:
#             classes.append(intent["tag"])

# words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
# words = sorted(list(set(words)))
# classes = sorted(list(set(classes)))


# training = []
# output_empty = [0] * len(classes)

# for doc in documents:
#     bag = []
#     pattern_words = doc[0]
#     pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
#     for word in words:
#         bag.append(1) if word in pattern_words else bag.append(0)

#     output_row = list(output_empty)
#     output_row[classes.index(doc[1])] = 1
#     training.append([bag, output_row])

# random.shuffle(training)
# training = np.array(training, dtype=object)

# train_x = list(training[:, 0])
# train_y = list(training[:, 1])


# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation="relu"),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(64, activation="relu"),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(len(train_y[0]), activation="softmax")
# ])

# model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])


# history = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5)


# model.save("chatbot_model.h5")


# def predict_class(sentence): #Funkce bere jako vstup větu a předpovídá třídu nebo úmysl této věty pomocí natrénovaného modelu.
#     bag = []
#     sentence_words = nltk.word_tokenize(sentence)
#     sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

#     for word in words:
#         bag.append(1) if word in sentence_words else bag.append(0)

#     res = model.predict(np.array([bag]))[0]
#     ERROR_THRESHOLD = 0.25
#     results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list = []

#     for r in results:
#         return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

#     return return_list

# def get_response(intents_list, intents_json): #snaží se formulovat větu pomocí modelu
#         tag = intents_list[0]["intent"]
#         list_of_intents = intents_json["intents"]
#         for i in list_of_intents:
#             if i["tag"] == tag:
#                 result = random.choice(i["responses"])
#                 break
#         return result
# print("Chatbot is ready to help you!")
memory = []

def get_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jsi hlasový asistent pro seniory, který má za úkol pomoci s každodenními úkoly. Pokud se tě senior zeptá na něco ohledně technologií a nebudeš vědět, odpověz pouze nevím."},
            {"role": "user", "content": message},
            {"role": "assistant", "content": memory}
        ]
    )
    memory.append(response.choices[0].message.content)
    return response.choices[0].message.content



def execute_voice_command(text): #zařizuje možnost odpovědí hlasem
    if text == '':
        pass
    else:
        message = text
        #intents = predict_class(message)
        response = get_response(message)
        audio_playback(response)



def kripl():
    while True:
        if config.VOICE == True:
            command = voice_command_processor()
            execute_voice_command(command)
        elif config.VOICE == False:
            message = input('[?] >> ')
            response = get_response(message)
            print(response)
        else:
            print('voice_command_processor isnt definied')
    

