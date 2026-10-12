
import os
import json
import time
import RPi.GPIO as GPIO
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Raspberry Pi button setup
BUTTON_PIN = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Telegram configuration
BOT_TOKEN = "8894164562:AAGyFCeFjG1dUXuydN1xqI8fZ0zPDH4kLWY"
CHAT_ID = "8652604470"


def send_telegram_notification():
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID is missing.")
        return

    message = "Someone pressed the alert button!"

    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": message
    }).encode("utf-8")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

            if result.get("ok"):
                print("Telegram notification sent successfully!")
            else:
                print("Telegram error:", result)

    except HTTPError as error:
        print("Telegram HTTP error:", error.code)
        print(error.read().decode("utf-8"))

    except URLError as error:
        print("Network error:", error.reason)

    except Exception as error:
        print("Could not send Telegram notification:", error)


print("Alert button monitoring system is now active.")
print("Press the physical button to send a Telegram alert.")
print("Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH and not button_pressed:
            print("Someone pressed the alert button!")
            button_pressed = True
            send_telegram_notification()

        elif GPIO.input(BUTTON_PIN) == GPIO.LOW:
            button_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    GPIO.cleanup()
