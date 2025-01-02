import speech_recognition as sr
import pyttsx3
import requests
import psutil
import pyautogui
import datetime
import smtplib
import json
import os
import openai

# Set your API keys
openai.api_key = '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'  # Replace with your OpenAI API key
weather_api_key = '3d3c081016b7adc6eea74bbd0c2abae8'  # Replace with your OpenWeather API key
news_api_key = 'e94e3f63643c4095bcd5263c5e7e9d2f'  # Replace with your NewsAPI key

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Define the file to store the name
name_file = "name.json"

# Load the stored name from the file if it exists
def load_name():
    if os.path.exists(name_file):
        with open(name_file, 'r') as f:
            data = json.load(f)
            return data.get("name")
    return None

# Save the name to a file
def save_name(name):
    with open(name_file, 'w') as f:
        json.dump({"name": name}, f)

# Define OpenAI's API function to handle questions
def ask_openai(question):
    try:
        # Use OpenAI's gpt-3.5-turbo model to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the new gpt-3.5-turbo model
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I couldn't process your question."


# Define weather function (OpenWeather API)
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=New+Delhi&appid={weather_api_key}"
    response = requests.get(url).json()
    main = response['main']
    weather = response['weather'][0]['description']
    temperature = main['temp'] - 273.15  # Convert from Kelvin to Celsius
    return f"The temperature is {temperature:.2f}°C with {weather}."

# Define AQI function (OpenWeather API)
def get_aqi():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?q=New+Delhi&appid={weather_api_key}"
    response = requests.get(url).json()
    aqi = response['list'][0]['main']['aqi']
    return f"The Air Quality Index (AQI) is {aqi}."

# Define latest news function (NewsAPI)
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    response = requests.get(url).json()
    articles = response['articles']
    headlines = [article['title'] for article in articles[:5]]
    return "Latest News: " + ", ".join(headlines)

# Define system info function (using psutil)
def get_system_info():
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    return f"Battery: {battery.percent}% remaining, CPU Usage: {cpu_usage}%, Memory: {memory.percent}% used."

# Function to open applications using pyautogui


def open_application(app_name): 
    app_name = app_name.lower()
    if app_name == "notepad":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')
    elif app_name == "calculator":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('calc')
        pyautogui.press('enter')
    elif app_name == "word":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('winword')
        pyautogui.press('enter')
    elif app_name == "chrome":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('chrome')
        pyautogui.press('enter')
    elif app_name == "firefox":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('firefox')
        pyautogui.press('enter')
    elif app_name == "spotify":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('spotify')
        pyautogui.press('enter')
    elif app_name == "vs code":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('code')
        pyautogui.press('enter')
    elif app_name == "paint":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('mspaint')
        pyautogui.press('enter')
    elif app_name == "explorer":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('explorer')
        pyautogui.press('enter')
    elif app_name == "task manager":
        pyautogui.hotkey('ctrl', 'shift', 'esc')
    elif app_name == "cmd":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('cmd')
        pyautogui.press('enter')
    elif app_name == "control panel":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('control')
        pyautogui.press('enter')
    elif app_name == "chatgpt":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('chatgpt')  # Adjust the command based on the app installation
        pyautogui.press('enter')
    elif app_name == "whatsApp":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('whatsApp')  # Assuming the app is named 'whatsapp' in the run command
        pyautogui.press('enter')
    else:
        print(f"Application '{app_name}' is not recognized or not added.")

# Example usage:
# open_application("chatgpt")
# open_application("whatsapp")


# Function to take voice input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, I couldn't connect to the service.")
        return ""

# Function to ask for and set the user's name
def set_name():
    engine.say("What is your name?")
    engine.runAndWait()
    name = take_command()
    if name:
        save_name(name)
        engine.say(f"Nice to meet you, {name}.")
        engine.runAndWait()

# Function to send an email
def send_email(subject, message, recipient_email):
    try:
        # Your email credentials
        sender_email = "your-email@gmail.com"  # Sender's email address
        sender_password = "your-email-password"  # Sender's email password (or app password for Gmail)

        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail's SMTP server
        server.starttls()  # Secure connection

        # Log in to your email account
        server.login(sender_email, sender_password)

        # Create the email
        email_message = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(sender_email, recipient_email, email_message)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error occurred while sending email: {e}"

# Function to tell the current date and time
def get_date_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    return f"The current time is {current_time} and today's date is {current_date}."

# Main function to run Jarvis
def jarvis():
    name = load_name()

    if name:
        engine.say(f"Hello {name}, how can I assist you today?")
        engine.runAndWait()
    else:
        engine.say("Hello, I don't know your name yet. Let's set it up.")
        engine.runAndWait()
        set_name()

    while True:
        command = take_command()

        if "weather" in command:
            response = get_weather()
            engine.say(response)
            engine.runAndWait()

        elif "aqi" in command:
            response = get_aqi()
            engine.say(response)
            engine.runAndWait()

        elif "news" in command:
            response = get_news()
            engine.say(response)
            engine.runAndWait()

        elif "system info" in command:
            response = get_system_info()
            engine.say(response)
            engine.runAndWait()

        elif "open" in command:
            app_name = command.split("open")[-1].strip()
            open_application(app_name)
            engine.say(f"Opening {app_name}")
            engine.runAndWait()

        elif "tell me" in command:
            question = command.split("ask")[-1].strip()
            response = ask_openai(question)  # Use OpenAI's API here
            engine.say(response)
            engine.runAndWait()

        elif "send email" in command:
            engine.say("What is the subject of the email?")
            engine.runAndWait()
            subject = take_command()
            engine.say("What is the message content?")
            engine.runAndWait()
            message = take_command()
            engine.say("What is the recipient's email address?")
            engine.runAndWait()
            recipient_email = take_command()
            response = send_email(subject, message, recipient_email)
            engine.say(response)
            engine.runAndWait()

        elif "time" in command or "date" in command:
            response = get_date_time()
            engine.say(response)
            engine.runAndWait()

        elif "exit" in command:
            engine.say("Goodbye!")
            engine.runAndWait()
            break

# Run the assistant
jarvis()
