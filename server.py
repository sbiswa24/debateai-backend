from flask import request, Blueprint, Flask, jsonify

# Import the required functions from your evidence_scraper module
# from . import evidence_scraper, eyePositionAnalyzer
import evidence_scraper, eyePositionAnalyzer, detect_stutter
# import eyePositionAnalyzer
import glob
import time
import sys
from moviepy.editor import *
import os
from random import randint
from playsound import playsound
# from . import detect_stutter
#import search_google, web_qa

app = Flask(__name__)

# Register the "second" blueprint



# Members API route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/evifinder", methods=['GET', 'POST'])
def evifinder():
    # query = "What is the height of the eiffel tower"
    # query = "What is the height of Mt. Everest"
    # query = "What is the height of the tallest man"
    # query = "What is the height of the shortest man"
    query = request.get_json()
    print (query)

    url_list = evidence_scraper.search_google(query, num_results=2)
    # print(url_list)
    # url_list = ['https://www.toureiffel.paris/en/news/history-and-culture/why-does-eiffel-tower-change-size', 'https://www.cnn.com/videos/travel/2022/03/16/eiffel-tower-height-change-lon-orig-na.cnn', 'https://en.wikipedia.org/wiki/Eiffel_Tower', 'https://www.cometoparis.com/paris-guide/paris-monuments/eiffel-tower-s922', 'https://www.pbs.org/wgbh/buildingbig/wonder/structure/eiffel_tower.html']
    # url_list = ["https://www.toureiffel.paris/en/news/history-and-culture/why-does-eiffel-tower-change-size", 'https://www.cnn.com/videos/travel/2022/03/16/eiffel-tower-height-change-lon-orig-na.cnn', 'https://en.wikipedia.org/wiki/Eiffel_Tower']
    response = evidence_scraper.web_qa(url_list, query)
    return jsonify(response)


@app.route('/startVideoAnalysis', methods=['POST'])
def debate_video_analysis():
    print("here")
    filename = 'demo1.mp4'
    recording = request.files.get('file')
    recording.save(r"C:\Users\subhr\Downloads\experimental_video_save.mp4")


    #return Response({"status": "ok"})
    #query = request.get_json()
    #print(query)
    # Last downloaded mp4 file
    # r'C:\Users\subhr\Downloads\speech-recording.mp4'
    time.sleep(2)
    latest_mp4_file = return_latest_mp4()
    print(latest_mp4_file)
    # video_recording = latest_file
    results = []
    os.rename(latest_mp4_file, latest_mp4_file.replace(' ', str(randint(700000, 9000000))))
    new_mp4 = return_latest_mp4()
    print("file: " + new_mp4)

    accuracy_ratio = eyePositionAnalyzer.analyzeEyePosition(new_mp4)

    ffmpeg_tools.ffmpeg_extract_audio(new_mp4, r"C:\Users\subhr\Downloads\audio_from_video" + str(
        randint(700000, 9000000)) + ".wav")

    p_sev, r_sev, o_sev, p_count, r_count = audio_analyzer(return_latest_wav())
    accuracy_ratio['stuttering_count'] = round(p_count+r_count)
    print(results)
    results.append(accuracy_ratio)
    return jsonify(results)


def audio_analyzer(audio):

    return detect_stutter.detect_stutter(audio)

    #audio = AudioClip(r"C:\Users\subhr\Downloads\audio_from_video.wav")
    #video = VideoFileClip(latest_mp4_file)
    #audio = video.audio
    # if audio is not None:
    #     print("audio extracted")
    # audio.write_audiofile(r'C:\Users\subhr\Downloads\audio_from_video.wav')
    # playsound(audio)

def return_latest_wav():
    list_of_files = glob.glob(r'C:\Users\subhr\Downloads\*.wav')
    latest_wav_file = max(list_of_files, key=os.path.getctime)
    return latest_wav_file

def return_latest_mp4():
    list_of_files = glob.glob(r'C:\Users\subhr\Downloads\*.mp4')
    latest_mp4_file = max(list_of_files, key=os.path.getctime)
    return latest_mp4_file

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=4500)
