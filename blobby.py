import argparse
import soundfile
import pyrubberband as pyrb
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def wav_sound(filestem, shift_num=0):
    #fix wav format, plus change pitch
    data, samplerate = soundfile.read(f'{filestem}.wav')
    shifted_data = pyrb.pitch_shift(data, samplerate, shift_num)
    soundfile.write(f'{filestem}.wav', shifted_data, samplerate)

    return AudioSegment.from_file(f'{filestem}.wav', format='wav')

def say_string(s):
    #synthesize
    i = 0
    for voice in filter(lambda v: 'en_US' in v.languages, voices):
       engine.setProperty('voice', voice.id)
       engine.save_to_file(s, f'{i}.wav')
       i += 1
    engine.runAndWait()

    #overlay
    n = i
    merged = wav_sound(0)
    mod = 8
    for i in range(1, n):
        merged = merged.overlay(wav_sound(i, -2), position=i%mod)
        merged = merged.overlay(wav_sound(i, 9), position=(i+2)%mod)
        merged = merged.overlay(wav_sound(i, 6), position=(i+4)%mod)
        merged = merged.overlay(wav_sound(i, 8), position=(i+6)%mod)
    merged.export('merged.wav', format='wav')
    play(merged)

parser = argparse.ArgumentParser(description='synthesize a string')
parser.add_argument('input', help='string to synthesize')
args = parser.parse_args()
say_string(args.input)
