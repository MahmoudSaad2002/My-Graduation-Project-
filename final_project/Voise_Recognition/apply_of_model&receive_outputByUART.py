# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 07:58:34 2025

@author: Mahmoud_Saad
"""

import sounddevice as sd
import numpy as np
import librosa
import time
import serial
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

# --- الإعدادات ---
SAMPLING_RATE = 8000
DURATION = 1.0
N_MELS = 64
# CLASSES = ['up', 'down', 'left', 'right', 'stop']
CLASSES = ['backward', 'forward', 'left', 'right', 'stop']
THRESHOLD = 0.7  # حد الثقة

# --- تحميل الموديل ---
model = load_model("best_model_f2.keras")
scaler = StandardScaler()

# --- افتح الـ UART (عدّل COM والباودريت حسب إعدادات STM32) ---
ser = serial.Serial('COM5', baudrate=9600, timeout=1)

def extract_features(audio):
    audio = librosa.util.fix_length(audio, size=8000)
    mel = librosa.feature.melspectrogram(y=audio, sr=SAMPLING_RATE, n_mels=N_MELS)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = mel_db.T
    mel_db = scaler.fit_transform(mel_db)
    return np.expand_dims(mel_db, axis=0)

# print(" جاهز للاستماع...")

while True:
    print("🟢 Listening...")
    recording = sd.rec(int(DURATION * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=1, dtype='float32')
    sd.wait()

    audio = recording.flatten()
    features = extract_features(audio)
    predictions = model.predict(features)[0]

    max_idx = np.argmax(predictions)
    confidence = predictions[max_idx]

    if confidence > THRESHOLD:
        command = CLASSES[max_idx]
        print(f"✅ Command: {command} ({confidence*100:.2f}%)")
        if(command=="forward"):
            command="up"
            #print(f"✅ Command: {command} ({confidence*100:.2f}%)")
        if(command=="backward"):
            command="down"
            #print(f"✅ Command: {" send "+command}({confidence*100:.2f}%)")
        # --- إرسال عبر UART مع /n ---
        ser.write((command + '\n').encode())
    else:
        print("fail confidence < THRESHOLD.")

    time.sleep(0.5)  