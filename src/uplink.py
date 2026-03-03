import os
import threading
import telebot

class RemoteTether:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.token or not self.chat_id:
            print("\n>> [UPLINK WARNING] Credentials missing in .env. Mobile Uplink offline.")
            return

        try:
            self.bot = telebot.TeleBot(self.token)
            self.setup_handlers()
            
            # Start polling in a background daemon thread
            t = threading.Thread(target=self.bot.infinity_polling, daemon=True)
            t.start()
            print(">> [UPLINK] Remote Tether Online. Awaiting secure mobile transmissions.")
            
            # Send a boot message to your phone
            self.bot.send_message(self.chat_id, "📱 System Zero: Mobile Uplink Established. Awaiting remote orders.")
        except Exception as e:
            print(f">> [UPLINK ERROR] Failed to initialize: {e}")

    def setup_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            # SECURITY VAULT: Only listen to YOUR exact phone
            if str(message.chat.id) != str(self.chat_id):
                print(f"\n>> [SECURITY] Blocked unauthorized mobile access from ID: {message.chat.id}")
                return
            
            print(f"\n>> [INCOMING MOBILE TRANSMISSION]: {message.text}")
            
            # Formulate the agentic prompt so Zero knows to reply to your phone
            agentic_prompt = f"[MOBILE UPLINK FROM OPERATOR]: {message.text}\n(Note: Process this request, then use the 'send_mobile_alert' tool to send the final answer back to my phone before completing the task.)"
            
            # Push it into the same queue the GUI uses!
            self.command_queue.put(agentic_prompt)