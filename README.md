# MOBICARE — Smart Wheelchair (Graduation Project)

**Mobile Health Revolution: The MobiCare Approach to Patient Support**

> This repository contains the code, documentation, datasets pointers, and design files for **MOBICARE** — a smart, multi-modal assistive wheelchair integrating embedded systems, AI-based control (voice & eye-tracking), and a mobile app for control & health monitoring. The full final project report (book) is included in `final_book.pdf`. 

---

## Quick overview (TL;DR)

* **Goal:** Provide an adaptive wheelchair controlled via **voice**, **head movement**, **eye-tracking**, and **mobile app**, with integrated **real-time health/environment monitoring** and a human-centered UI/UX. 
* **Main components:** Raspberry Pi 4 (AI processing), STM32 microcontroller (real-time motor control), ESP32 (Wi-Fi/Bluetooth), BTS7960 motor drivers, Flutter mobile app, and AI models (CNN-LSTM for voice; MediaPipe/OpenCV for gaze).
* **Highlights / Results:** Voice recognition >90% accuracy; eye-tracking ≈95% gaze detection; system latency <100 ms in tests.

---

## Table of contents

1. [Project structure](#project-structure)
2. [Features](#features)
3. [System architecture](#system-architecture)
4. [Hardware components & wiring summary](#hardware-components--wiring-summary)
5. [Software components & folders](#software-components--folders)
6. [How to run / reproduce (developer instructions)](#how-to-run--reproduce-developer-instructions)
7. [AI model training & inference (voice recognition)](#ai-model-training--inference-voice-recognition)
8. [Mobile app (Flutter) setup](#mobile-app-flutter-setup)
9. [Embedded firmware (STM32 & ESP32)](#embedded-firmware-stm32--esp32)
10. [Testing, results & evaluation](#testing-results--evaluation)
11. [Datasets, size and Git LFS recommendation](#datasets-size-and-git-lfs-recommendation)
12. [Folder layout (recommended)](#folder-layout-recommended)
13. [Contributors & acknowledgments](#contributors--acknowledgments)
14. [License & citation](#license--citation)

---

## Project structure

(High-level; adapt to actual repository layout)

```
/ai/                     # AI models, training scripts, notebooks
/embedded/               # STM32/ESP32 firmware source, schematics
/mobile_app/             # Flutter project (UI, Firebase integration)
/hardware/               # PCB files, wiring diagrams, BOM
/datasets/               # small sample datasets or pointers (large data stored externally)
/models/                 # trained model weights (if included) or download scripts
/docs/                   # final_book.pdf, reports, diagrams
/scripts/                # helpers: flash scripts, data preprocessing
README.md
LICENSE
```

See final report for detailed chapters, tables and figures. 

---

## Features

* **Multi-modal control:** Voice commands, head-motion detection, eye-tracking, and mobile-app navigation. 
* **Real-time health/environment monitoring:** Temperature, humidity (option for biometric sensors). Data streamed to mobile app. 
* **Hybrid architecture:** Heavy AI on Raspberry Pi 4; deterministic motor control on STM32; ESP32 for connectivity. 
* **Accessible UI/UX:** App designed in Figma and implemented with Flutter focusing on clarity and accessibility. 
* **Modular & extensible:** Gesture, GPS tracking, cloud storage or BCI can be added in future iterations. 

---

## System architecture

### High-level flow

1. **User input (voice / gaze / head / mobile)** →
2. **Raspberry Pi 4** (runs AI inference: speech model, gaze detection using MediaPipe/OpenCV) →
3. **Command messaging** (UART/Wi-Fi) →
4. **STM32 microcontroller** receives direction commands → generates **PWM** to BTS7960 motor drivers → motor actuation.

### Why hybrid?

Offloading AI tasks to Raspberry Pi keeps real-time motor control deterministic on the STM32 while still enabling complex ML models to run locally (low latency, privacy). 

---

## Hardware components & wiring summary

**Core hardware used in the project**

* Raspberry Pi 4 (AI / camera / voice capture). 
* STM32F103 (“Blue Pill”/STM32F103C8T6) as motor controller and sensor aggregator. 
* ESP32 module for Wi-Fi/Bluetooth & communication with mobile app. 
* Motor drivers: BTS7960 (H-bridge) for DC motors. 
* Camera (for gaze tracking), microphone (for voice), environmental sensors (DHTxx), optional heart-rate sensor. 

**Notes**

* Motor PWM controlled via STM32 timers; STM32 uses UART ports to receive commands from Raspberry Pi / ESP32. STM32 was chosen over AVR (e.g. ATmega32) for better peripherals and multiple UARTs. 

Refer to `/hardware/README.md` (or schematic PDFs) for detailed pinouts and wiring diagrams. 

---

## Software components & folders

* `/ai/` — audio preprocessing (Librosa), model architecture (Keras/TensorFlow), training notebooks, inference scripts. 
* `/mobile_app/` — Flutter frontend, Firebase integration (Auth + Realtime DB). See `android/` and `ios/` configs. 
* `/embedded/` — STM32 (HAL or CubeMX-based) firmware, ESP32 comms code, flash instructions. 
* `/hardware/` — BOM, PCB/external wiring diagrams, motor driver datasheets. 
* `/docs/` — `final_book.pdf` (full project report). 

---

## How to run / reproduce — developer instructions

> These are general steps — check each subfolder for exact scripts/configs.

### Prereqs

* Raspberry Pi 4 (Raspbian / Raspberry Pi OS) with camera & USB microphone.
* PC for Flutter dev (Android Studio + Flutter SDK) or terminal for `flutter run`.
* STM32 toolchain: STM32CubeIDE / PlatformIO / OpenOCD + ST-Link.
* Python 3.8+ for AI (TensorFlow, Keras, Librosa, OpenCV, MediaPipe). 

### AI (on Raspberry Pi)

```bash
# create venv
python3 -m venv venv
source venv/bin/activate
pip install -r ai/requirements.txt   # includes: tensorflow, keras, librosa, opencv-python, mediapipe

# Run inference (example)
python ai/inference.py --model models/voice_cnn_lstm.h5 --audio_device 0
```

(See `ai/README.md` for exact training commands & hyperparams.) 

### Mobile app (Flutter)

```bash
cd mobile_app
flutter pub get
flutter run    # on connected device or emulator
```

Firebase setup: add `google-services.json` and `GoogleService-Info.plist` as instructed in `/mobile_app/README.md`. 

### Embedded (STM32)

* Open `embedded/STM32/` project in STM32CubeIDE or PlatformIO.
* Flash using ST-Link: `st-flash write build/firmware.bin 0x8000000` or via IDE.
* Ensure UART baud matches Raspberry Pi/ESP32 side.

---

## AI model training & dataset notes

* Models are CNN-LSTM hybrids trained on labeled command audio (“forward”, “back”, “left”, “right”, “stop”). Data augmentation (noise, pitch/time-shift) used to increase robustness. 
* Training notebooks and scripts are in `/ai/notebooks/` and `/ai/train.py`. Outputs (best model weights) go to `/models/`. 

**Important:** large raw audio datasets are heavy — use Git LFS or host datasets externally (Google Drive) and include downloader scripts. See section below. 

---

## Mobile App (Flutter) & Firebase

* UI designed in Figma; widgets and navigation implemented in Flutter. Features: login (Email/Google), dashboard (temperature/humidity), control page (joystick & direction buttons), reminders, user profile.
* Firebase Realtime Database is used to stream sensor & system data; Authentication via Firebase Auth. Steps to setup included in `/mobile_app/README.md`. 

---

## Embedded firmware (STM32 & ESP32)

* STM32 handles ADC (joystick), PWM motor control, and UART comms. Uses BTS7960 drivers for high-power DC motors. STM32 was selected after comparing to ATmega32 due to additional UARTs and performance.
* ESP32 module bridges STM32 & mobile app (Wi-Fi/Bluetooth) and relays sensor readings to Firebase (optional). 

---

## Testing & evaluation

* Extensive testing across light/noise conditions; models were trained with augmented datasets for dialects/background noise. Final reported metrics: voice recognition >90% accuracy; eye-tracking ~95% success in gaze detection; system latency <100 ms. See Chapter 4 and Conclusion for full test tables & plots.

---

## Datasets, size and Git LFS recommendation

* If your repo includes raw audio datasets or large model weights, use **Git LFS**:

```bash
git lfs install
git lfs track "*.wav"
git lfs track "*.h5"
git add .gitattributes
git add path/to/largefiles
git commit -m "Track large files with LFS"
git push
```

* Alternatively: host big datasets on Google Drive/Dropbox and provide download scripts (`scripts/download_datasets.sh`).

---

## Folder layout (recommended)

Add a `README.md` inside each major folder (`/ai`, `/mobile_app`, `/embedded`) with precise per-module instructions and environment variables. The repository `README` should act as the top-level index.

---

## Contributing

1. Fork the repo.
2. Create a feature branch (`feature/your-feature`).
3. Test on hardware or simulator where applicable.
4. Submit PR with description, test results, and updated docs.

---

## License

This project is released under the **MIT License** — see `LICENSE` file. *(Change if needed.)*

---

## Acknowledgments & references

* Project report: *Mobile Health Revolution: The MobiCare Approach to Patient Support* — full report included (`/docs/final_book.pdf`). 
* Supervisor: Dr. Ayman Soliman; Co-supervisor: Eng. Mohammed Gharib. 

---

## Contact & citation

If you use this work, please cite the project report and contact the contributors listed in `CONTRIBUTORS.md`. The final report contains full explanations, tables, figures and appendices for reproduction. 

---

### Need help polishing this README or generating the per-folder `README` files and `.gitattributes` for Git LFS?

I can generate:

* A ready-to-commit `README.md` file (this file) as a repo-ready markdown.
* `ai/requirements.txt` snippet and `mobile_app/README.md` starter.
* `.gitattributes` lines for the large files you want tracked.

## Supervisor 
Dr/Ayman Soliman 
## Team member 
* Mahmoud Saad 
* Mahmoud Maher
* Ahmed Maher
* Mostafa Salama 
* Eman taha
   
