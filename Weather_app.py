
import sys

import requests
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit,      #importing modules and libraries
                             QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):      #main WeatherApp class
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)      #my main elements of the app
        self.temperature_label = QLabel(self)
        self.pixmap = (QPixmap())
        self.sun_label = QLabel(self)
        self.description_label = QLabel(self)
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("Images/icon.jpg"))    #icon for the app

        vbox = QVBoxLayout()   #creating layout

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)    #adding all my widgets to a layout
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.sun_label)
        vbox.addWidget(self.description_label)


        self.setLayout(vbox)    #setting the VBox layout

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)    #alligning everything at center
        self.description_label.setAlignment(Qt.AlignCenter)
        self.sun_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")   #setting object names so it's easier to style them
        self.sun_label.setObjectName("sun_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            
            QLabel, QPushButton{
                font-family: calibri;
            }
            
            QLabel#city_label{
                font-size: 25px;
                font-style: medium;
                font-family: Segoe UI;
                color: #94A3B8;
            }
            
            QLineEdit#city_input{
                font-size: 40px;
                font-family: Segoe UI;
                color: #F8FAFC;
                border-radius: 15px;
                background-color: #131b2b;
                margin-bottom: 50px;
            }
            
            QPushButton#get_weather_button{
                font-size: 30px;
                font-family: Segoe UI;
                background-color: #38BDF8;
                color: #111827;
                border: none;
                border-radius: 20px;
                padding: 10px;
                color: #111827;
                margin-bottom: 50px;
            }
            
            QPushButton#get_weather_button:hover{background-color: #0EA5E9;}
            QPushButton#get_weather_button:pressed{background-color: #0284C7;}
            
            QLabel#temperature_label{
                font-size: 65px;
                font-family: Segoe UI Light;
                color: #F8FAFC;
                margin-top: 15px;
            }
            
            
            QLabel#description_label{
                font-size: 60px;
                font-family: Segoe UI;
                color: #F8FAFC;
            }
            
            QWidget{
                background-color: #111827;
            }
        """)    #styling all elements in CSS

        self.city_input.returnPressed.connect(self.get_weather)   #this is when you press "Enter" after you enter the city name(you don't have to press the button)

        self.get_weather_button.setMinimumSize(500,55)  #setting minimum sizes of button
        self.setMinimumSize(600,850)                    #setting minimum size of the windows itself

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "91cb9ea86bf0fb0e58242d8465e856c1"    #my api key (PLEASE USE YOURS, this is a begginer mistake that I put it here, but you learn on your mistakes)
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:  #if evetyrhing is right then just display the weather
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:     #if there is an error then you will get a error message
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP Error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nRequest timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCkeck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):   #here im displaying that error
        self.temperature_label.setStyleSheet("font-size: 35px;")

        self.temperature_label.setText(message)

        self.sun_label.clear()
        self.description_label.clear()

    def display_weather(self, data): #displaying the temperature and the description of it
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15

        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{round(temperature_c, 1)}°C") #this is temperature
        self.temperature_label.setStyleSheet("font-size: 75px;")

        weather_description = data["weather"][0]["description"]
        self.description_label.setText(f"{weather_description.capitalize()}") #this is description

        image_path = self.get_weather_pic(weather_id)
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(350,200,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.sun_label.setPixmap(scaled_pixmap)   #all of this is for displaying the description image

    @staticmethod
    def get_weather_pic(weather_id):    #if there is a certain type of weather, a specific photo will be displayed

        if 200 <= weather_id <= 232:
            return "Images/thunderstorm.png"

        elif 300 <= weather_id <= 321:
            return "Images/clouds.png"

        elif 500 <= weather_id <= 531:
            return "Images/rain.png"

        elif 600 <= weather_id <= 622:
            return "Images/snow.png"

        elif 701 <= weather_id <= 741:
            return "Images/fog.png"

        elif weather_id == 762:
            return "Images/volcano.png"

        elif weather_id == 781:
            return "Images/tornado.png"

        elif weather_id == 800:
            return "Images/sun.png"

        elif 801 <= weather_id <= 804:
            return "Images/clouds.png"

        else:
            return ""


if __name__ == "__main__":  #this ensures that the main function only runs when its executed directly
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()  #displaying the app itself
    sys.exit(app.exec_())
