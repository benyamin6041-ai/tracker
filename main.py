from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from plyer import gps
import requests
import json

# لینک اختصاصی تو که فرستادی
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzgKqdp_pGrujIdOb8re3MEJiNbGacKmJnodh9x3jiiHgJQr0BRmIJHWfJhP1frHxpY/exec"

class TrackerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.status = Label(text="آماده دریافت دستور", font_size="24sp")
        self.add_widget(self.status)
        btn = Button(text="شروع ردیابی (Start)", size_hint=(1, 0.3))
        btn.bind(on_press=self.start)
        self.add_widget(btn)

    def start(self, btn):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=10000, minDistance=0)
            self.status.text = "ردیابی فعال است..."
        except Exception as e:
            self.status.text = f"خطا در GPS: {str(e)}"

    def on_location(self, **kwargs):
        lat = kwargs.get("lat")
        lon = kwargs.get("lon")
        acc = kwargs.get("accuracy", 0)
        self.send(lat, lon, acc)

    def on_status(self, stype, status):
        pass

    def send(self, lat, lon, acc):
        try:
            payload = json.dumps({"lat": lat, "lon": lon, "acc": acc})
            # ارسال به گوگل شیت
            requests.post(WEBHOOK_URL, data=payload, timeout=10)
            self.status.text = "موقعیت ارسال شد ✅"
        except Exception:
            self.status.text = "خطا در ارسال ❌"

    def on_pause(self):
        return True

class TrackerApp(App):
    def build(self):
        return TrackerLayout()

if __name__ == "__main__":
    TrackerApp().run()
