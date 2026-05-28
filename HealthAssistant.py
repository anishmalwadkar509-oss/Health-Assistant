import pyaudio
import wave
import assemblyai as aai
import pyttsx3
import time

# Replace with your AssemblyAI API key
aai.settings.api_key = "fd98b50d5f214048b863f491cf4553c4"


# Function to record audio from the microphone and save it to a file
def record_audio(file_path, duration=6, sample_rate=44100, chunk_size=1024):
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    frames = []

    # Speak "Plz ask me a question"
    engine = pyttsx3.init()
    engine.say("Plz ask me a question")
    engine.runAndWait()

    print("Recording...")
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()


while True:
    # Path to save the recorded audio
    FILE_PATH = "/home/pi/test_recording.wav"

    # Record audio from the microphone and save it to the specified file path
    record_audio(FILE_PATH)

    # Transcribe the recorded audio
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_PATH)

    if transcript.status == aai.TranscriptStatus.error:
        print("Transcription error:", transcript.error)
    else:
        print("Transcription:", transcript.text.lower())

        # Extract transcribed text
        transcribed_text = transcript.text.lower()

        # Check if the transcribed text matches any of the predefined questions
        if "what is your name" in transcribed_text:
            response = "My name is Health Assistant."
        elif "how much water should i drink in a day" in transcribed_text:
            response = "Drink at least 8 glasses of water per day."
        elif "what are some good sources of protein for a vegetarian diet" in transcribed_text:
            response = "Vegetarians can get protein from sources like beans, lentils, tofu, nuts, seeds, and dairy products."
        elif "how can i improve my sleep quality" in transcribed_text:
            response = "Create a relaxing bedtime routine, limit screen time before bed, keep the bedroom cool and dark, and avoid caffeine or heavy meals close to bedtime."
        elif "what are the benefits of regular exercise" in transcribed_text:
            response = "Regular exercise can improve cardiovascular health, boost mood, enhance weight management, strengthen muscles and bones, and reduce the risk of chronic diseases such as diabetes."
        elif "how can i manage stress in my daily life" in transcribed_text:
            response = "Practice stress-reducing techniques such as deep breathing, meditation, yoga, exercise, and maintaining a healthy work-life balance."
        elif "what are the warning signs of a heart attack" in transcribed_text:
            response = "Symptoms of a heart attack may include chest pain or discomfort, shortness of breath, nausea, and pain."
        elif "how can i maintain a healthy diet" in transcribed_text:
            response = "Focus on a balanced diet that includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, sugary drinks, and excessive intake of salt."
        elif "what are some ways to prevent the flu" in transcribed_text:
            response = "Get an annual flu vaccine, practice good hand hygiene, avoid close contact with sick individuals, and maintain a healthy lifestyle to support your immune system."
        elif "how much exercise is recommended for adults each week" in transcribed_text:
            response = "Adults should aim for at least 150 minutes of moderate-intensity aerobic exercise or 75 minutes of vigorous-intensity exercise per week, along with muscle-strengthening activities."
        elif "what are the benefits of staying hydrated" in transcribed_text:
            response = "Staying hydrated supports bodily functions, helps regulate body temperature, improves skin health, aids digestion, and can contribute to better overall physical and mental well-being."
        elif "who made you" in transcribed_text:
            response = "I was built by Harsh Phadnis and Anish Malwadkar."
        elif "what is your purpose" in transcribed_text:
            response = "I am a prototype and my main purpose is to assist the medical staff/patient."
        elif "how much do you weigh" in transcribed_text:
            response = "I weigh approximately two kilograms."
        elif "whom are you allowed to assist" in transcribed_text:
            response = "I am allowed to assist anyone who needs basic medical guidance, as well as doctors who need equipment that are at faraway distances."
        else:
            response = "I'm sorry, I didn't understand your question."

        # Respond with the appropriate answer
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()

    # Take a break of 10 seconds before starting again
    time.sleep(10)