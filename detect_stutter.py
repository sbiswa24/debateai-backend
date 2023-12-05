import librosa
import numpy as np
import tensorflow as tf
from pydub import AudioSegment
from keras.models import load_model
from pygame import mixer
import os




model_rep = load_model('best_model_rep.h5')
model_pro = load_model('best_model_pro.h5')


def detect_prolongation(mfcc): 
    s = 0
    for m in mfcc:
        y = model_pro.predict(m.reshape(1,2,44,1), batch_size=1)
        y = np.around(y,decimals=2)
        if y[0][0] > 0.5:
            s += y[0][0]
    p_sev = s/len(mfcc)*100
    return p_sev, s

def detect_repetition(mfcc):
    s = 0
    for m in mfcc:
        y = model_rep.predict(m.reshape(1,13,44,1), batch_size=1)
        y = np.around(y,decimals=2)
        if y[0][0] > 0.5:
            s += y[0][0]
    r_sev = s/len(mfcc)*100
    return r_sev, s

def detect_stutter(audio):
    print("audio: "+audio)
    sound_file = AudioSegment.from_wav(audio)

    # define stream chunk
    audio_chunks = sound_file[::1000]
    ps = 0
    rs = 0
    mfcc_arr_p = []
    mfcc_arr_r = []
    for i, chunk in enumerate(audio_chunks):
        chunkfile = "chunk{0}.wav".format(i)
        chunk.export(chunkfile, format="wav")
        y, sr = librosa.load(chunkfile)
        mfcc = np.array(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))
        
        if mfcc.shape[0] == 13 and mfcc.shape[1] == 44:
            a = []
            a.append(mfcc)
            mfcc_arr_r.append(a)
            b = []
            b.append(mfcc[0])
            b.append(mfcc[12])
            mfcc_arr_p.append(b)
            
    mfcc_arr_r = np.array(mfcc_arr_r)  
    mfcc_arr_p = np.array(mfcc_arr_p)    
    
    mfcc_arr_r.reshape(mfcc_arr_r.shape[0], 13, 44, 1)
    mfcc_arr_p.reshape(mfcc_arr_p.shape[0], 2, 44, 1)
    
    p_sev, p_count = detect_prolongation(mfcc_arr_p)
    r_sev, r_count = detect_repetition(mfcc_arr_r)
    
    o_sev = (p_sev+r_sev)/2

    print('Prolongation % : ' + str(p_sev))
    print('Repetition % : ' + str(r_sev))
    print('Overall stutter % : ' + str(o_sev))
    
    return p_sev, r_sev, o_sev, p_count, r_count

