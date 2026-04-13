import tkinter
import requests

api_key ="ee2bf2ff698d8a69902cc4b02138cec6"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Enter a city name")
        return

    url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(url)

    if response.status_code == "200":
        data = response.json()
        temp = data["temp"]
        weather_discription = data["weather"][0]["description"]

        result = (
            f"City: {city}/n"
            f"Temperature: {temp}"
            f"Description: {weather_discription}"
        )
        result_label.config(text=result)
    else:
        result_label.config(text="City not found or API error")

root = tkinter.Tk()
root.title("Weather app")

city_label = tkinter.Label(root, text = "Enter city")
city_entry = tkinter.Entry(root, width = 30)
city_entry.pack(pady=5)

get_weather_button = tkinter.Button(root, text ="Get weather", command= get_weather)
get_weather_button.pack(pady=10)

result_label = tkinter.Label(root, text = "", justify = "left")
result_label.pack(pady= 10)

root.mainloop()