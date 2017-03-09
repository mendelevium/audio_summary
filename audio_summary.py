# Example : Produce an audio summary of a podcast
# http://traffic.libsyn.com/timferriss/TIMFERRISSSHOW028.mp3

# download and install FFMEG from https://ffmpeg.org/
from pydub import AudioSegment
from pydub.silence import split_on_silence

#AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"
root_file = "C:/audio/"
audio_file = "C:/audio/TIMFERRISSSHOW028.mp3"
split_file = "C:/audio/split/"
chunk_file = "chunk{0}.wav"
sound_file = AudioSegment.from_mp3(audio_file)

# split audio file base on silences
# must be silent for at least 750 millisecond and consider it silent if quieter than -45 dBFS
audio_chunks = split_on_silence(sound_file, min_silence_len=750, silence_thresh=-45)

# generate flac audio files for each splitted chunk
for i, chunk in enumerate(audio_chunks):
    out_file = split_file + chunk_file.format(i)
    chunk.export(out_file, format="wav")
    print out_file


import speech_recognition as sr
from os import path
r = sr.Recognizer()
file_list = os.listdir(split_file)
#dic = {}
transcript = []

# go through splitted files
for i, wav in enumerate(file_list):

    # load file
    AUDIO_FILE = path.join(path.dirname(split_file), chunk_file.format(i))
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using Sphinx
    try:
        sentence = r.recognize_sphinx(audio) + "."
        #dic[chunk_file.format(i)] = sentence
        transcript.append((i, chunk_file.format(i), sentence))
        print(chunk_file.format(i) + " : " + sentence )
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


import json
# export json
with open(root_file + 'transcripts.json', 'w') as fp:
    #json.dump(dic, fp, sort_keys=True, indent=4)
    json.dump(transcript, fp, indent=4)
# reimport json
#with open(root_file + 'transcripts.json', 'r') as fp:
#    transcript = json.load(fp)


# summarize transcript
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
sents= ""

LANGUAGE = "english"
SENTENCES_COUNT = 3
parser = PlaintextParser.from_string(transcript, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

for sent in summarizer(parser.document, SENTENCES_COUNT):
    sents = sents + str(sent)

import re
files = re.findall("chunk\d{1,}\.wav", str(sents))

file1 = AudioSegment.from_wav(split_file + files[0])
file2 = AudioSegment.from_wav(split_file + files[1])
file3 = AudioSegment.from_wav(split_file + files[2])
audio_summary = file1 + file2 + file3

audio_summary.export(root_file + "audio_summary.mp3", format="mp3")
