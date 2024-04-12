import os
os.system("pip install pygobject")
import pyaudio
import nltk
import ssl
import speech_recognition as sr
from gtts import gTTS
import pygame
from multiprocessing import Process, Queue
import math
import playsound
from nltk.stem import WordNetLemmatizer
import random
from openai import OpenAI
p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

p.terminate()

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
import assets.config as config
client = OpenAI(api_key="")

lemmatizer = WordNetLemmatizer()

r = sr.Recognizer()

screenWidth, screenHeight = 480, 320
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
dt = 0

talking = False

pygame.mouse.set_visible(False)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

el1pos = pygame.Vector2((screen.get_width() / 10) * 2.25, screen.get_height() / 3)
er1pos = pygame.Vector2(((screen.get_width() / 10) * 7.75), screen.get_height() / 3)

el2pos = pygame.Vector2((screen.get_width() / 10) * 2.4, (screen.get_height() / 10) * 3.8)
er2pos = pygame.Vector2(((screen.get_width() / 10) * 7.6), (screen.get_height() / 10) * 3.8)

eyelidposr = pygame.Vector2((screen.get_width() / 10) * 2.25, screen.get_height() / 3)
eyelidposl = pygame.Vector2(((screen.get_width() / 10) * 7.75), screen.get_height() / 3)

m1pos = pygame.Vector2(screen.get_width() / 2, -(screen.get_height() / 10) * 1.25)
m2pos = pygame.Vector2(screen.get_width() / 2, -(screen.get_height() / 10) * 8.25)

winkDirection = 1
eyeWinkHeight = 55
wink = 0
frames = 0

cyan = "#00a2ee"

mouthHeight = 60
mouthDir = 1
mouthTopCurveHeight = 50
mouthTopHeight = 60
conditions = 0

class Eye:
    def __init__(self, color, x, y, dx, dy, angle1, angle2, size):
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle1 = angle1
        self.angle2 = angle2
        self.size = size

    def draw(self):
        return pygame.draw.arc(
        screen,
        self.color,
        pygame.Rect(
            self.x - self.dx / 2,
            self.y - self.dy / 2,
            self.dx, self.dy),
            self.angle1, self.angle2, self.size
        )

def kripl2(talking_queue):
    global running
    global eyeWinkHeight
    global wink
    global frames
    global mouthHeight
    global mouthDir
    global mouthTopCurveHeight
    global conditions
    global talking
    global mouthTopHeight
    pygame.init()  # Initialize the Pygame video system
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not talking_queue.empty():
            talking = talking_queue.get()
            print(talking)
        screen.fill("black")

        # LEFT EYE OUT

        eyeLeftOutTop = Eye(cyan, (screenWidth/10) * 2.25, (screenHeight/3), 110, 110, 0, math.pi, 55)
        eyeLeftOutTop = eyeLeftOutTop.draw()
        
        eyeLeftOutBottom = Eye(cyan, (screenWidth/10) * 2.25, (screenHeight/3), 110, 110, math.pi, 0, 55)
        eyeLeftOutBottom = eyeLeftOutBottom.draw()
        
        # RIGHT EYE OUT
        
        eyeRightOutTop = Eye(cyan, (screenWidth/10) * 7.75, (screenHeight/3), 110, 110, 0, math.pi, 55)
        eyeRightOutTop = eyeRightOutTop.draw()

        eyeRightOutBottom = Eye(cyan, (screenWidth/10) * 7.75, (screenHeight/3), 110, 110, math.pi, 0, 55)
        eyeRightOutBottom = eyeRightOutBottom.draw()
        
        # LEFT EYE IN
        
        eyeLeftInTop = Eye("black", (screenWidth/10) * 2.4, (screenHeight/10) * 3.8, 55, eyeWinkHeight, 0, math.pi, 28)
        eyeLeftInTop = eyeLeftInTop.draw()

        eyeLeftInBottom = Eye("black", (screenWidth/10) * 2.4, (screenHeight/10) * 3.8, 55, eyeWinkHeight, math.pi, 0, 28)
        eyeLeftInBottom = eyeLeftInBottom.draw()

        # RIGHT EYE IN

        eyeRightInTop = Eye("black", (screenWidth/10) * 7.6, (screenHeight/10) * 3.8, 55, eyeWinkHeight, 0, math.pi, 28)
        eyeRightInTop = eyeRightInTop.draw()

        eyeRightInBottom = Eye("black", (screenWidth/10) * 7.6, (screenHeight/10) * 3.8, 55, eyeWinkHeight, math.pi, 0, 28)
        eyeRightInBottom = eyeRightInBottom.draw()

        # MOUTH

        mouthBottom = pygame.draw.arc(screen, cyan, pygame.Rect((screenWidth/2) - 150, 216 - mouthHeight / 2, 300, mouthHeight), math.pi, 0, 5)

        mouthHeight += mouthDir * 3

        if talking:
            if conditions == 2:
                mouthTop = pygame.draw.arc(screen, cyan, pygame.Rect((screenWidth/2) - 150, 216 - mouthHeight / 8, 300, mouthHeight / 4), 0, math.pi, 5)
                if mouthHeight >= 120:
                    mouthDir = -random.randint(5, 15) / 10
                elif mouthHeight <= 100:
                    mouthDir = random.randint(5, 15) / 10
            else:
                mouthTop = pygame.draw.arc(screen, cyan, pygame.Rect((screenWidth/2) - 150, 216 - mouthTopHeight / 8, 300, mouthTopHeight / 4), 0, math.pi, 5)
                mouthTopCurve = pygame.draw.arc(screen, "black", pygame.Rect((screenWidth/2) - 200, 216 - 25 - mouthTopCurveHeight/2, 400, mouthTopCurveHeight), math.pi, 0, 50)
                if mouthTopCurveHeight >= 50:
                    mouthTopCurveHeight -= 8
                else:
                    conditions += 1
                if mouthTopHeight <= 100:
                    mouthTopHeight += 8
                else: 
                    conditions += 1


        else:
            conditions = 0
            mouthDir = 0
            mouthHeight = 100
            # mouthTopHeight = 0
            if mouthTopHeight >= 0:
                mouthTop = pygame.draw.arc(screen, cyan, pygame.Rect((screenWidth/2) - 150, 216 - mouthTopHeight / 8, 300, mouthTopHeight / 4), 0, math.pi, 5)
                mouthTopHeight -= 4
            mouthTop = pygame.draw.arc(screen, cyan, pygame.Rect((screenWidth/2) - 150, 216 - 50, 300, mouthHeight), math.pi, 0, mouthTopCurveHeight // 4)
            mouthTopCurve = pygame.draw.arc(screen, "black", pygame.Rect((screenWidth/2) - 200, 216 - 25 - mouthTopCurveHeight/2, 400, mouthTopCurveHeight), math.pi, 0, 50)
            if mouthTopCurveHeight <= 100:
                mouthTopCurveHeight += 4
            # mouthTopCurve = pygame.draw.arc(screen, "black", pygame.Rect((screenWidth/2) - 100, 216 - 75, 200, 100), math.pi, 0, 50)


        # EYELIDS

        if wink < frames:
            # print(eyeLeftInTop)
            if eyeWinkHeight >= 55:
                winkDirection = -1
            elif eyeWinkHeight <= 0:
                winkDirection = 1
            if winkDirection == 1 and eyeWinkHeight >= 44:
                winkDirection = 0
                eyeWinkHeight = 55
                wink += random.randint(300, 420)
            eyeWinkHeight += winkDirection * 10
            # print(eyeLeftInTop[3])

        frames += 1
        pygame.display.flip()
        dt = clock.tick(50) / 1000

    pygame.quit()

def voice_command_processor(ask=False):
    with sr.Microphone(device_index=2) as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source,phrase_time_limit=4) #odposlech z mikrofonu
        text = '' #preset pro řečenou frázi
        text=r.recognize_google(audio, language='cs')
        if text == '': #pokud bude ticho tak bude ai ignorovat
            print('')
        else:
            print(f"User: {text}") #zobrazí frázi řečenou uživatelem
        return text.lower()

def audio_playback(text, talking_queue):
    language = 'cs'#jazyk hlasové výslovnosti
    voice = gTTS(text=text, lang=language) #vytvoření hlasového modelu
    voice.save("Voice.mp3") # uložení hlasového modelu
    talking_queue.put(True)
    playsound.playsound("Voice.mp3") #přehrání hlasového modelu
    print(1)
    talking_queue.put(False)
    print(2)
    print(text) #zobrazení řečeného text

memory = []

def get_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jsi hlasový asistent pro seniory, který má za úkol pomoci s každodenními úkoly. Pokud se tě senior zeptá na něco ohledně technologií a nebudeš vědět, odpověz pouze nevím."},
            {"role": "user", "content": message},
        ]
    )
    return response.choices[0].message.content



def execute_voice_command(text, talking_queue): #zařizuje možnost odpovědí hlasem
    if text == '':
        pass
    else:
        message = text
        #intents = predict_class(message)
        response = get_response(message)
        audio_playback(response, talking_queue)



def kripl(talking_queue):
    while True:
        if config.VOICE == True:
            command = voice_command_processor()
            execute_voice_command(command, talking_queue)
        elif config.VOICE == False:
            message = input('[?] >> ')
            response = get_response(message)
        else:
            print('voice_command_processor isnt definied')
    

if __name__ == '__main__':
    talking_queue = Queue()

    p1 = Process(target=kripl, args=(talking_queue,))
    p2 = Process(target=kripl2, args=(talking_queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
