import os
import matplotlib
import matplotlib.pyplot as plt
import pylab
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import pandas as pd
from glob import glob
import scipy
from pathlib import Path
from sklearn.cluster import KMeans
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
'''
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics
from numpy import loadtxt
from keras.models import load_model'''
#MR


#for finding the current dir
DIR = os.getcwd()

#the sampling rate we are taking our data at, can be adjusted for tuning
SAMPLERATE = 11025

#ambient energy of the node with normal traffic
#found from analyzing the data recieved from Longwood Ave Node - If values exceed check
AMBIENTENERGY = 500

#the categories for training the ML model
CATEGORIES = ['gunshot', 'car crash']




def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colours(image, number_of_colors, show_chart):
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)

    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.show()

    return hex_colors

def get_mel_spectrogram_data(audio_file):
    sig, fs = librosa.load(audio_file, SAMPLERATE)
    return (sig, fs)

def build_mel_spectrogram_in_dir(audio_file):
    #build a library of test data
    try:
        sig, fs = librosa.load(audio_file, SAMPLERATE)
    except Exception as e:
        print('Can\'t build spectrogram')

    #filtering the white noise
    sig = scipy.signal.medfilt(sig)
    # make pictures name
    save_path =  audio_file.split('.')[0] + '.jpg'

    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(save_path, bbox_inches=None, pad_inches=0)
    pylab.close()


#create mel specs for all .wav and .flac files in directory
def create_training_data(directory):
    #adding the audio files to be processed
    audio_file = get_wav_files(directory)
    audio_file += get_flac_files(directory)
    print('Processing audio files')
    for af in audio_file:
        build_mel_spectrogram_in_dir(af)

def get_wav_files(directory):
    audio_files = glob(directory + '/*.wav')
    return audio_files

def get_flac_files(directory):
    audio_files = glob(directory + '/*.flac')
    return audio_files

#find the abs magnitude of the frequency buckets in FFT
def get_fft_magnitude(audio_file):
    try:
        sig, fs = librosa.load(audio_file, SAMPLERATE)
        sig = scipy.signal.medfilt(sig)
    except Exception as e:
        print("Can't parse file")
        return None
    #get the fft of the data array
    yf = scipy.fft(sig)
    yf_abs = np.absolute(yf)
    #return the normalized values (without phase angles)
    return yf_abs

#find the amount of energy in the audio sample in the higher frequency range
def get_sample_energy(audio_file):
    #get the signal and filter
    try:
        sig, fs = librosa.load(audio_file, SAMPLERATE)
        sos = scipy.signal.butter(10, 200, 'hp', fs=SAMPLERATE/2, output='sos')
        sig = scipy.signal.sosfilt(sos, sig)
    except Exception as e:
        print("Can't parse file")
        return None

    #get the fft of the data array
    yf = scipy.fft(sig)
    #absolute values of the data
    yf_abs = np.abs(yf)

    #computing the energy in the audio sample

    N = SAMPLERATE/2
    #remove the lower frequencies
    yf_abs = yf_abs[round(N/4):]

    #determine energy
    square_sum = 0
    for y in yf_abs:
        square_sum += y*y

    energy = square_sum/(3*N/4)
    return energy

def grab_incident(file_name):
    if "crash" in file_name:
        return "Car crash"
    elif "gun" in file_name:
        return "Gun shot"
    else:
        return None

def extract_feature(file_name):
    #find the features for the models
    try:
        sig, fs = librosa.load(file_name, SAMPLERATE)
        mfccs = librosa.feature.mfcc(y=sig, sr=fs, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)

    except Exception as e:
        print('Error encountered while parsing file ')
        return None

    #return the data for model testing
    return np.array([mfccsscaled])


def determine_if_event(audio_file):
    #algorithm to get the energy of the filtered signal
    sample_energy = get_sample_energy(audio_file)

    #use for removing file

    if(sample_energy > AMBIENTENERGY and grab_incident(audio_file) != None):
        #build the spectogram for the ML model
        build_mel_spectrogram_in_dir(audio_file)
        #check to see what type of event
        return grab_incident(audio_file)
    else:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        else:
            print("The file does not exist")
        return None





##Building the model####
'''
def print_prediction(file_name):
    model = load_model('model.hdf5')

    prediction_feature = extract_feature(file_name)
    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    print("The predicted class is:", predicted_class[0], '\n')

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)):
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )
'''

########Functions for testing the algorithm and model#########

def display_fft(audio_file):
    #return the fft graph
    sig, fs = librosa.load(audio_file, SAMPLERATE)
    #sig = scipy.signal.medfilt(sig)
    sos = scipy.signal.butter(10, 200, 'hp', fs=SAMPLERATE/2, output='sos')
    sig = scipy.signal.sosfilt(sos, sig)

    n = len(sig)
    T = 1/fs
    yf = scipy.fft(sig)
    xf = np.linspace(0.0, 1.0/(2.0*T), n/2)
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n *np.abs(yf[:n//2]))
    plt.grid()
    plt.ylabel('Magnitude')
    plt.xlabel('Frequency(Hz)')
    plt.title(audio_file.split('\\')[-1])
    plt.show()
    plt.close('all')
    return


######### Testing #####################
'''
#create_training_data(os.getcwd() + '/carcrash')
#create_training_data(os.getcwd())
#display_fft(os.getcwd() + '\\carcrash\\sample.flac')
#display_fft(os.getcwd() + '\\carcrash\\carcrash2.wav')
#display_fft(os.getcwd() + '\\gunshot\\gunshot_1.wav')
#print(get_sample_energy(os.getcwd() + '\\carcrash\\sample.flac'))
print(get_sample_energy(os.getcwd() + '\\carcrash\\carcrash1.wav'))
print(get_sample_energy(os.getcwd() + '\\carcrash\\carcrash2.wav'))
#print(get_sample_energy(os.getcwd() + '\\gunshot\\sample.flac'))

print(get_sample_energy(os.getcwd() + '\\gunshot\\gunshot_1.wav'))
print(get_sample_energy(os.getcwd() + '\\gunshot\\gunshot_2.wav'))
print(get_sample_energy(os.getcwd() + '\\carcrash\\sample_1.flac'))
#display_fft('jackhammer_1.wav')
#print(determine_if_event(os.getcwd() + '\\carcrash\\carcrash1.wav'))
#print(determine_if_event(os.getcwd() + '\\carcrash\\carcrash2.wav'))
#print(determine_if_event(os.getcwd() + '\\carcrash\\sample.flac'))
#get_colours(get_image('gunshot_1.jpg'), 8, True)
#print(get_colours(get_image('sample.jpg'), 8, True))
#get_sample_energy('rev.wav')
#get_sample_energy('siren.wav')
#print(get_sample_energy('jackhammer_1.wav'))
#display_fft('jackhammer_1.wav')
#print(get_sample_energy(os.getcwd()+'\\carcrash\\sample_1.flac'))

'''
