import os
import sys
import threading
import time
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# Mobil ekran piksellarining avto-scaling sozlamasi
Window.softinput_mode = "below_target"

# =========================================================
# GLOBAL SOZLAMALAR
# =========================================================
APP_CONFIG = {
    "AQ.Ab8RN6IttWv1V_pZYeIwDLDGE5KxT__7IzecMvm_zs3GGF2KPw": "",
    "8650802431:AAGE0vB6w-CV4PrNECB0xp-RMTT4j3gEUcU": "",
    "8601259351": "",
    "TARGET_COINS": 5000,
    "TARGET_DP": 500,
    "TIMER_HOURS": 0,
    "TIMER_MINUTES": 0,
}

bot_running = False


# =========================================================
# 1. SPLASH SCREEN (FLEX Style)
# =========================================================
class SplashScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    root = RelativeLayout()

    with root.canvas.before:
      Color(0.04, 0.07, 0.15, 1)  # FLEX Deep Blue
      self.bg = RoundedRectangle(size=Window.size, pos=(0, 0))

    box = BoxLayout(
        orientation="vertical",
        spacing=10,
        size_hint=(0.8, 0.3),
        pos_hint={"center_x": 0.5, "center_y": 0.5},
    )

    flex_label = Label(
        text="FLEX",
        font_size="56sp",
        bold=True,
        color=(0.95, 0.95, 1, 1),
        halign="center",
    )
    sub_label = Label(
        text="Flex & Subaru DLS Auto Controller",
        font_size="14sp",
        color=(0.5, 0.6, 0.8, 1),
        halign="center",
    )

    box.add_widget(flex_label)
    box.add_widget(sub_label)
    root.add_widget(box)
    self.add_widget(root)

    Clock.schedule_once(self.goto_login, 2.5)

  def goto_login(self, dt):
    self.manager.current = "login"


# =========================================================
# 2. LOGIN SCREEN (Glassmorphism Style)
# =========================================================
class LoginScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    root = RelativeLayout()

    with root.canvas.before:
      Color(0.04, 0.07, 0.15, 1)
      RoundedRectangle(size=Window.size, pos=(0, 0))

    # Glass Card Container
    card = RelativeLayout(
        size_hint=(0.85, 0.55), pos_hint={"center_x": 0.5, "center_y": 0.5}
    )

    with card.canvas.before:
      Color(0.12, 0.18, 0.3, 0.75)  # Glassmorphism effect
      self.card_bg = RoundedRectangle(
          size=(Window.width * 0.85, Window.height * 0.55),
          pos=(0, 0),
          radius=[20],
      )

    layout = BoxLayout(
        orientation="vertical",
        padding=25,
        spacing=12,
        pos_hint={"x": 0, "y": 0},
    )

    title = Label(
        text="Login",
        font_size="26sp",
        bold=True,
        color=(1, 1, 1, 1),
        size_hint_y=None,
        height=35,
    )
    subtitle = Label(
        text="Welcome back, please login",
        font_size="12sp",
        color=(0.7, 0.75, 0.85, 1),
        size_hint_y=None,
        height=20,
    )

    self.username = TextInput(
        hint_text="User Name",
        multiline=False,
        size_hint_y=None,
        height=45,
        background_color=(0.08, 0.12, 0.22, 0.8),
        foreground_color=(1, 1, 1, 1),
        hint_text_color=(0.5, 0.5, 0.6, 1),
        padding=[12, 12],
    )

    self.password = TextInput(
        hint_text="Password",
        password=True,
        multiline=False,
        size_hint_y=None,
        height=45,
        background_color=(0.08, 0.12, 0.22, 0.8),
        foreground_color=(1, 1, 1, 1),
        hint_text_color=(0.5, 0.5, 0.6, 1),
        padding=[12, 12],
    )

    login_btn = Button(
        text="Login",
        size_hint_y=None,
        height=45,
        background_color=(0.15, 0.75, 0.35, 1),
        color=(1, 1, 1, 1),
        bold=True,
    )
    login_btn.bind(on_press=self.do_login)

    self.error_msg = Label(
        text="", font_size="11sp", color=(1, 0.3, 0.3, 1), size_hint_y=None, height=20
    )

    layout.add_widget(title)
    layout.add_widget(subtitle)
    layout.add_widget(self.username)
    layout.add_widget(self.password)
    layout.add_widget(login_btn)
    layout.add_widget(self.error_msg)

    card.add_widget(layout)
    root.add_widget(card)
    self.add_widget(root)

  def do_login(self, instance):
    if self.username.text == "admin" and self.password.text == "1234":
      self.manager.current = "dashboard"
    else:
      self.error_msg.text = "Maxfiy login yoki parol xato!"


# =========================================================
# 3. DASHBOARD SCREEN (Full Control Panel)
# =========================================================
class DashboardScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    root = RelativeLayout()

    with root.canvas.before:
      Color(0.04, 0.07, 0.15, 1)
      RoundedRectangle(size=Window.size, pos=(0, 0))

    scroll = ScrollView(size_hint=(1, 0.9), pos_hint={"x": 0, "top": 1})
    layout = BoxLayout(
        orientation="vertical",
        padding=20,
        spacing=12,
        size_hint_y=None,
    )
    layout.bind(minimum_height=layout.setter("height"))

    layout.add_widget(
        Label(
            text="DLS AI Auto Bot Controller",
            font_size="20sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=30,
        )
    )

    # Inputs
    layout.add_widget(
        Label(
            text="Target Coins:",
            color=(0.8, 0.85, 0.95, 1),
            size_hint_y=None,
            height=20,
            halign="left",
        )
    )
    self.coins_input = TextInput(
        text="1000",
        multiline=False,
        size_hint_y=None,
        height=40,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    layout.add_widget(self.coins_input)

    layout.add_widget(
        Label(
            text="Target Prize Ladder (DP):",
            color=(0.8, 0.85, 0.95, 1),
            size_hint_y=None,
            height=20,
        )
    )
    self.dp_input = TextInput(
        text="500",
        multiline=False,
        size_hint_y=None,
        height=40,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    layout.add_widget(self.dp_input)

    # Timer inputs
    layout.add_widget(
        Label(
            text="Taymer Sozlamasi (Soat va Daqiqa):",
            color=(0.8, 0.85, 0.95, 1),
            size_hint_y=None,
            height=20,
        )
    )
    timer_box = BoxLayout(
        orientation="horizontal", spacing=10, size_hint_y=None, height=40
    )
    self.hours_input = TextInput(
        hint_text="Soat (masalan: 7)",
        multiline=False,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.mins_input = TextInput(
        hint_text="Daqiqa (masalan: 45)",
        multiline=False,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    timer_box.add_widget(self.hours_input)
    timer_box.add_widget(self.mins_input)
    layout.add_widget(timer_box)

    # AI Key
    layout.add_widget(
        Label(
            text="AI API Token (DeepSeek / OpenAI / Claude):",
            color=(0.8, 0.85, 0.95, 1),
            size_hint_y=None,
            height=20,
        )
    )
    self.ai_token = TextInput(
        password=True,
        multiline=False,
        size_hint_y=None,
        height=40,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    layout.add_widget(self.ai_token)

    # Telegram Tokens
    layout.add_widget(
        Label(
            text="Telegram Bot Token & Chat ID:",
            color=(0.8, 0.85, 0.95, 1),
            size_hint_y=None,
            height=20,
        )
    )
    self.tg_token = TextInput(
        hint_text="Bot Token",
        multiline=False,
        size_hint_y=None,
        height=40,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.tg_chat = TextInput(
        hint_text="Chat ID",
        multiline=False,
        size_hint_y=None,
        height=40,
        background_color=(0.1, 0.15, 0.25, 1),
        foreground_color=(1, 1, 1, 1),
    )
    layout.add_widget(self.tg_token)
    layout.add_widget(self.tg_chat)

    # Status
    self.status_lbl = Label(
        text="Holat: To'xtatilgan",
        font_size="13sp",
        color=(1, 0.4, 0.4, 1),
        size_hint_y=None,
        height=30,
    )
    layout.add_widget(self.status_lbl)

    scroll.add_widget(layout)
    root.add_widget(scroll)

    # Fixed Bottom Buttons
    btn_bar = BoxLayout(
        orientation="horizontal",
        spacing=10,
        size_hint=(1, 0.1),
        pos_hint={"x": 0, "y": 0},
        padding=[15, 10],
    )
    start_btn = Button(
        text="START BOT", background_color=(0.1, 0.8, 0.3, 1), bold=True
    )
    start_btn.bind(on_press=self.start_bot)

    stop_btn = Button(
        text="STOP BOT", background_color=(0.8, 0.2, 0.2, 1), bold=True
    )
    stop_btn.bind(on_press=self.stop_bot)

    btn_bar.add_widget(start_btn)
    btn_bar.add_widget(stop_btn)
    root.add_widget(btn_bar)

    self.add_widget(root)

  def start_bot(self, instance):
    global bot_running
    if not bot_running:
      bot_running = True
      APP_CONFIG["TARGET_COINS"] = int(self.coins_input.text or 1000)
      APP_CONFIG["TARGET_DP"] = int(self.dp_input.text or 500)
      APP_CONFIG["TIMER_HOURS"] = int(self.hours_input.text or 0)
      APP_CONFIG["TIMER_MINUTES"] = int(self.mins_input.text or 0)
      APP_CONFIG["AI_API_KEY"] = self.ai_token.text
      APP_CONFIG["TELEGRAM_BOT_TOKEN"] = self.tg_token.text
      APP_CONFIG["TELEGRAM_CHAT_ID"] = self.tg_chat.text

      self.status_lbl.text = "Holat: Bot Ishga Tushdi (AI & ADB faol)..."
      self.status_lbl.color = (0.2, 1, 0.3, 1)

      threading.Thread(target=run_dls_bot_engine, daemon=True).start()

  def stop_bot(self, instance):
    global bot_running
    bot_running = False
    self.status_lbl.text = "Holat: To'xtatildi"
    self.status_lbl.color = (1, 0.4, 0.4, 1)


# =========================================================
# 4. BOT ENGINE & AUTOMATION LOGIC
# =========================================================
def tap(x, y):
  os.system(f"adb shell input tap {x} {y}")


def send_telegram(message):
  token = APP_CONFIG["TELEGRAM_BOT_TOKEN"]
  chat_id = APP_CONFIG["TELEGRAM_CHAT_ID"]
  if token and chat_id:
    try:
      url = f"https://api.telegram.org/bot{token}/sendMessage"
      requests.post(url, data={"chat_id": chat_id, "text": message})
    except Exception as e:
      print(f"Telegram error: {e}")


def run_dls_bot_engine():
  global bot_running
  start_time = time.time()

  # Taymer vaqtini sekundlarga aylantirish
  total_timer_seconds = (APP_CONFIG["TIMER_HOURS"] * 3600) + (
      APP_CONFIG["TIMER_MINUTES"] * 60
  )

  collected_coins = 0
  collected_dp = 0

  while bot_running:
    elapsed_seconds = time.time() - start_time

    # Shartlarni tekshirish (Tanga, DP yoki Taymer tugaganda)
    if (
        collected_coins >= APP_CONFIG["TARGET_COINS"]
        or collected_dp >= APP_CONFIG["TARGET_DP"]
        or (total_timer_seconds > 0 and elapsed_seconds >= total_timer_seconds)
    ):

      send_telegram(
          "Sizning vazifangiz bajarildi! 1-level akkauntda kiritilgan"
          f" miqdorda tanga ({collected_coins}) va DP ({collected_dp}) yig'ildi."
          " Kirib tekshirib olishingiz mumkin."
      )
      bot_running = False
      break

    # 1. Matchni boshlash (Division -> Uzbekistan -> Play)
    tap(850, 250)  # Career / Legendary Division
    time.sleep(2)
    tap(850, 250)  # Uzbekistan / Division match
    time.sleep(2)
    tap(880, 500)  # Play Match button
    time.sleep(10)

    # 2. Match davomidagi harakatlar va Auto-Resume (7.5 daqiqa)
    match_start = time.time()
    while (time.time() - match_start) < 450 and bot_running:
      tap(850, 480)  # Pass / Attack tap
      time.sleep(1.5)

      # Pauza menyusini Resume qilish
      tap(70, 50)  # Pause Icon
      time.sleep(0.5)
      tap(700, 420)  # RESUME button
      time.sleep(1)

    # 3. Match Tugagach Mukofotlarni yig'ish (Claim & Ads)
    time.sleep(3)
    tap(350, 440)  # Bonus Reward CLAIM
    time.sleep(2)
    tap(550, 440)  # DP Prize Ladder CLAIM
    time.sleep(2)

    # Reklama ko'rish va X tugmasini bosish
    time.sleep(35)  # Reklama tugashi
    tap(940, 50)  # Reklama X (yuqori o'ng burchak)
    time.sleep(2)

    tap(880, 520)  # CONTINUE button
    time.sleep(3)

    # 4. Best Team (Jamoani yangilash)
    tap(330, 520)  # TEAM button
    time.sleep(2)
    tap(730, 140)  # BEST TEAM button
    time.sleep(2)
    tap(70, 50)  # Back to Main Menu
    time.sleep(2)

    collected_coins += 150
    collected_dp += 30


# =========================================================
# APP ENTRY
# =========================================================
class MainDLSApp(App):

  def build(self):
    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(SplashScreen(name="splash"))
    sm.add_widget(LoginScreen(name="login"))
    sm.add_widget(DashboardScreen(name="dashboard"))
    return sm


if __name__ == "__main__":
  MainDLSApp().run()
