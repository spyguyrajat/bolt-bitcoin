import requests, time, json, conf                    
from boltiot import Bolt       
                
mybolt = Bolt(conf.bolt_api_key, conf.device_id)

def get_bitcoin_price():
   URL = "https://min-api.cryptocompare.com/" # REPLACE WITH CORRECT URL
   response = requests.request("GET", URL)
   response = json.loads(response.text)
   current_price = response["INR"]
   return current_price

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False


while True:
    current_price = get_bitcoin_price()
    if current_price <= conf.threshold:
        print("Bitcoin has exceeded threshold")
        message = "Alert! The current Bitcoin Price is " + str(current_price)
        telegram_status = send_telegram_message(message)
        response = mybolt.digitalWrite('0', 'HIGH')
        print(response)
        time.sleep(5)
        response = mybolt.digitalWrite('0', 'LOW')
    time.sleep(10)