# Blind Assistance App

This project is a Blind Assistance App designed to help visually impaired individuals navigate their surroundings. The app captures images every 5 seconds and sends them to an AI service (Gemini Flash) for analysis, providing feedback on what’s in front of the user and whether it is safe. The app also features voice interaction and uses geolocation and motion detection to enhance usability.

## Features

- **Real-time Image Capture:** Captures images using the device's camera every 5 seconds.
- **AI Analysis:** Sends images to Gemini Flash for object detection and safety analysis.
- **Voice Interaction:** Uses speech recognition to take voice commands and text-to-speech for feedback.
- **Geolocation:** Utilizes the device's GPS to provide navigation support.
- **Motion Detection:** Detects device motion to trigger actions such as starting or stopping recordings.

## Technologies Used

- **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
- **Backend:** Python, FastAPI
- **AI Integration:** Google Generative AI
- **Hosting and Deployment:** Uvicorn for server management

## Requirements

The project requires the following Python packages, as listed in `requirements.txt`:

