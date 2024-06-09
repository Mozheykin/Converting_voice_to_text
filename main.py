import vosk
import argparse
import speech_recognition as sr
import wave
import datetime
import json

def sr_audio_to_text(mp3_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(mp3_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition не смог распознать аудио")
        except sr.RequestError as e:
            print("Ошибка при запросе к Google Speech Recognition: {0}".format(e))

def vosk_audio_to_text(mp3_file):
    wf = wave.open(mp3_file, "rb")
    model = vosk.Model(lang="ru-Ru")
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            return json.loads(rec.Result())

models = {
        "sr": sr_audio_to_text,
        "vosk": vosk_audio_to_text,
        }

def main():
    global models
    start = datetime.datetime.now()
    print(f'[START] {start.strftime("%H.%M.%S")}')
    parser = argparse.ArgumentParser(
            description="Преобразование аудиофайла в текст с помощью распознавания речи")
    parser.add_argument("-path", dest="mp3_file", required=True, 
                        help="Путь к аудиофайлу в формате MP3")
    parser.add_argument("-voice", dest="voice_model", 
                        help="Модель распознавания голоса (по умолчанию используется vosk)")
    
    args = parser.parse_args()
    
    if args.voice_model:
        print(f'[INFO] Select model is {args.voice_model}')
    else:
        print(f'[INFO] Select model is vosk')

    if args.mp3_file is not None:
        model = models.get(args.voice_model)
        if model is None:
            model = models.get("vosk")
        print('[INFO] Decode...')
        text = model(args.mp3_file)
        print(f'[RESULT] {text}')

    stop = datetime.datetime.now()
    print(f'[STOP] {stop.strftime("%H.%M.%S")}')
    delta = stop - start
    print(f'[WORKED] {delta.seconds} seconds')

if __name__ == "__main__":
    main()
