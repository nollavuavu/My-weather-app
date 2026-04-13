import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Weather_App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("cloud.jpg"))
        self.city_label = QLabel("What's the city yo: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
        self.api_key = "ee2bf2ff698d8a69902cc4b02138cec6"

    def initUI(self):
        self.setWindowTitle("Weather app")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Arial;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 70px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;    
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        self.city =  self.city_input.text()
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=5&appid={self.api_key}"

        response = requests.get(url)
        lon_lat_data = response.json()

        if not lon_lat_data:
            self.display_error(f"{self.city} is not found!")
        elif len(lon_lat_data) == 1:
            self.display_weather(lon_lat_data)
        else:
            self.show_disambiguation(lon_lat_data)


    def display_error(self, message):
        self.get_weather_button.setText(message)

    def display_weather(self, lon_lat_data):
        print(lon_lat_data)
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        weather_url = base_url + "appid=" + self.api_key + "&q=" + self.city + "&units=metric"

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        print(weather_data)

        weather_data = weather_response.json()
        temp = weather_data["main"]["temp"]
        weather = weather_data['weather'][0]["main"]
        weather_id = weather_data["weather"][0]["id"]

        self.temperature_label.setText(f"{temp}°C")
        self.description_label.setText(weather)
        if 200 <= weather_id <= 232:
            self.description_label.setText("Thunderstorm")
            self.emoji_label.setText("⛈")
        elif 300 <= weather_id <= 321:
            self.description_label.setText("Drizzle")
            self.emoji_label.setText("❤")
        elif 500 <= weather_id <= 531:
            self.description_label.setText("Rain")
            self.emoji_label.setText("🌧")
        elif 600 <= weather_id <= 622:
            self.description_label.setText("Snow")
            self.emoji_label.setText("❄")
        elif 700 <= weather_id <= 781:
            self.description_label.setText("Shit crazy brah")
            self.emoji_label.setText("😎")
        elif weather_id == 800:
            self.description_label.setText("Clear")
            self.emoji_label.setText("☀")
        elif 801 <= weather_id <= 804:
            self.description_label.setText("Clouds")
            self.emoji_label.setText("⛈")
        else:
            self.description_label.setText("We ain't know bout this one yet")

    def show_disambiguation(self, data):
        choices = []
        for location in data:
            parts = [location.get("name")]
            if location.get("state"):
                parts.append(location["state"])
            if location.get("country"):
                parts.append(location["country"])
            choices.append(", ".join(parts))

        choice, ok = QInputDialog.getItem(
            self,
            "Multiple matches found",
            "Which one did you mean?",
            choices,
            current = 0,
            editable=False
        )

        if ok:
            index = choices.index(choice)
            self.display_weather(data[index])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = Weather_App()
    weather_app.show()
    sys.exit(app.exec_())