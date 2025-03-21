import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import pyautogui
import random
import time
import pyperclip
from pynput import keyboard
from pynput.keyboard import Controller, Key, Listener
import google.generativeai as genai
import platform
from typing import Optional
import json
import os
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Set theme and default color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

os_name = platform.system()

keyboard_controller = Controller()

class CodeTypingBot:

    def __init__(self):
        self.stop_typing = False
        self.previous_clipboard_content = "" 
        self.humantype = False
        self.speed_frame: Optional[ctk.CTkFrame] = None
        self.keyboard_controller = Controller()
        self.os_name = platform.system()
        
        # Load preferences
        self.preferences = self.load_preferences()
        
        self.setup_ui()
        self.setup_keyboard_listener()

    def load_preferences(self):
        try:
            if os.path.exists('preferences.json'):
                with open('preferences.json', 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            'model': 'gemini-1.5-flash',
            'language': 'python',
            'prefix_prompt': '',
            'human_typing': False,
            'typing_speed': 0.15
        }

    def save_preferences(self):
        preferences = {
            'model': self.model_var.get(),
            'language': self.lang_var.get(),
            'prefix_prompt': self.prefix_var.get(),
            'human_typing': bool(self.checkbox_var.get()),
            'typing_speed': self.speed_var.get()
        }
        try:
            with open('preferences.json', 'w') as f:
                json.dump(preferences, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {str(e)}")

    def setup_ui(self):
        self.root = ctk.CTk()
        self.root.title("God Mod")
        self.root.geometry("800x900")
        self.root.minsize(800, 900)
        
        # Variables
        self.model_var = ctk.StringVar(value=self.preferences['model'])
        self.lang_var = ctk.StringVar(value=self.preferences['language'])
        self.checkbox_var = ctk.BooleanVar(value=self.preferences['human_typing'])
        self.speed_var = ctk.DoubleVar(value=self.preferences['typing_speed'])
        self.prefix_var = ctk.StringVar(value=self.preferences['prefix_prompt'])
        
        self.create_widgets()

    def create_widgets(self):
        # Main container with scrollbar
        self.main_container = ctk.CTkScrollableFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title with custom styling
        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            title_frame,
            text="GOD MOD",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="AI-Powered Code Generation",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        subtitle_label.pack()

        # API Keys Frame
        api_frame = ctk.CTkFrame(self.main_container)
        api_frame.pack(fill="x", pady=(0, 20))

        api_label = ctk.CTkLabel(
            api_frame,
            text="API Keys",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        api_label.pack(pady=(10, 5))

        self.api_text = ctk.CTkTextbox(
            api_frame,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.api_text.pack(fill="x", padx=20, pady=(0, 10))
        self.api_text.insert('1.0', self.load_api_keys())

        save_api_btn = ctk.CTkButton(
            api_frame,
            text="Save API Keys",
            command=self.save_api_keys,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        save_api_btn.pack(pady=(0, 10))

        # Settings Frame
        settings_frame = ctk.CTkFrame(self.main_container)
        settings_frame.pack(fill="x", pady=(0, 20))

        settings_label = ctk.CTkLabel(
            settings_frame,
            text="Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        settings_label.pack(pady=(10, 5))

        # Model Selection
        model_label = ctk.CTkLabel(
            settings_frame,
            text="Select Model:",
            font=ctk.CTkFont(size=12)
        )
        model_label.pack(anchor="w", padx=20, pady=(10, 5))

        model_combo = ctk.CTkComboBox(
            settings_frame,
            values=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
            variable=self.model_var,
            font=ctk.CTkFont(size=12)
        )
        model_combo.pack(fill="x", padx=20, pady=(0, 10))

        # Add model description
        model_desc = ctk.CTkLabel(
            settings_frame,
            text="• Gemini 1.5 Flash: Fast and efficient\n• Gemini 1.5 Pro: More accurate but slower\n• Gemini 2.0 Flash: Latest model with improved performance",
            font=ctk.CTkFont(size=10),
            text_color="#888888",
            justify="left"
        )
        model_desc.pack(anchor="w", padx=20, pady=(0, 10))

        # Language Input
        lang_label = ctk.CTkLabel(
            settings_frame,
            text="Programming Language:",
            font=ctk.CTkFont(size=12)
        )
        lang_label.pack(anchor="w", padx=20, pady=(10, 5))

        lang_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.lang_var,
            font=ctk.CTkFont(size=12)
        )
        lang_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Prefix Prompt
        prefix_label = ctk.CTkLabel(
            settings_frame,
            text="Prefix Prompt (Optional):",
            font=ctk.CTkFont(size=12)
        )
        prefix_label.pack(anchor="w", padx=20, pady=(10, 5))

        prefix_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.prefix_var,
            font=ctk.CTkFont(size=12)
        )
        prefix_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Human-like Typing Option
        self.human_type_checkbox = ctk.CTkCheckBox(
            settings_frame,
            text="Enable Human-like Typing",
            variable=self.checkbox_var,
            command=self.toggle_human_typing,
            font=ctk.CTkFont(size=12)
        )
        self.human_type_checkbox.pack(pady=10)

        # Speed Control Frame
        self.speed_frame = ctk.CTkFrame(settings_frame)
        self.speed_label = ctk.CTkLabel(
            self.speed_frame,
            text="Typing Speed:",
            font=ctk.CTkFont(size=12)
        )
        self.speed_slider = ctk.CTkSlider(
            self.speed_frame,
            from_=0.01,
            to=0.25,
            variable=self.speed_var
        )
        self.speed_labels = ctk.CTkLabel(
            self.speed_frame,
            text="Fast                   Medium                   Slow",
            font=ctk.CTkFont(size=10)
        )

        # Control Buttons
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=20)

        start_btn = ctk.CTkButton(
            button_frame,
            text="Start",
            command=self.start_monitoring,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=40
        )
        start_btn.pack(side="left", padx=10)

        stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop",
            command=self.quit_program,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=40,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        stop_btn.pack(side="left", padx=10)

        # Instructions Frame
        instructions_frame = ctk.CTkFrame(self.main_container)
        instructions_frame.pack(fill="both", expand=True, pady=(0, 20))

        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text="Instructions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        instructions_label.pack(pady=(10, 5))

        instructions = '''1. Open your code editor/IDE
2. Copy the question (Ctrl+C)
3. The code will be typed automatically
4. Press 'Shift' to stop typing at any time

Note: Restart the program if you encounter any errors'''

        instructions_text = ctk.CTkTextbox(
            instructions_frame,
            wrap="word",
            height=150,
            font=ctk.CTkFont(size=12)
        )
        instructions_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        instructions_text.insert('1.0', instructions)
        instructions_text.configure(state="disabled")

        # Show speed frame if human typing was enabled
        if self.checkbox_var.get():
            self.toggle_human_typing()

    def save_api_keys(self):
        api_keys = self.api_text.get('1.0', ctk.END).strip().split('\n')
        api_keys = [key.strip() for key in api_keys if key.strip()]
        
        try:
            # Generate a key from a password
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"your-secret-password"))
            f = Fernet(key)
            
            # Encrypt and save API keys
            encrypted_keys = [f.encrypt(key.encode()).decode() for key in api_keys]
            with open('api_keys.enc', 'w') as f:
                json.dump({'salt': base64.b64encode(salt).decode(), 'keys': encrypted_keys}, f)
            
            messagebox.showinfo("Success", "API keys saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API keys: {str(e)}")

    def load_api_keys(self):
        try:
            if os.path.exists('api_keys.enc'):
                with open('api_keys.enc', 'r') as f:
                    data = json.load(f)
                    salt = base64.b64decode(data['salt'])
                    encrypted_keys = data['keys']
                    
                    # Generate key from password
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    key = base64.urlsafe_b64encode(kdf.derive(b"your-secret-password"))
                    f = Fernet(key)
                    
                    # Decrypt API keys
                    return '\n'.join(f.decrypt(ek.encode()).decode() for ek in encrypted_keys)
        except Exception:
            pass
        return ""

    def selectApi(self):
        api_keys = self.api_text.get('1.0', ctk.END).strip().split('\n')
        api_keys = [key.strip() for key in api_keys if key.strip()]
        if not api_keys:
            raise ValueError("No API keys found. Please add your API keys first.")
        return random.choice(api_keys)

    def quit_program(self):
        self.stop_typing = True
        self.save_preferences()
        self.root.quit()
        self.root.destroy()

    def toggle_human_typing(self):
        if self.checkbox_var.get():
            self.speed_frame.pack(fill="x", padx=20, pady=10)
            self.speed_label.pack()
            self.speed_slider.pack(pady=5)
            self.speed_labels.pack()
            self.humantype = True
        else:
            self.speed_frame.pack_forget()
            self.humantype = False

    def setup_keyboard_listener(self):
        listener = Listener(on_press=self.on_press)
        listener.start()

    def set_humantype(self):
        self.humantype = self.checkbox_var.get() == 1

    def fast_type(self, text):
        for char in text:
            if self.stop_typing:
                return
            if char == '\n':
                keyboard_controller.press(Key.enter)
                keyboard_controller.release(Key.enter)
            else:
                keyboard_controller.press(char)
                keyboard_controller.release(char)
            time.sleep(0.01)

    def type_text_human_like(self, text: str) -> None:
        speed_factor = self.speed_var.get()
        base_delay = 0.05
        
        for char in text:
            if self.stop_typing:
                return
            pyautogui.typewrite(char, 0.01)
            delay = speed_factor + random.uniform(0, 0.1)
            time.sleep(delay)

    def remove_indents(self, text):
        return "\n".join(line.lstrip() for line in text.splitlines())

    def monitor_clipboard_and_type(self) -> None:
        try:
            genai.configure(api_key=self.selectApi())
            model = genai.GenerativeModel(model_name=self.model_var.get())
            generation_config = {
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            base_prompt = f"""Output ONLY {self.lang_var.get()} code without comments. Add new lines where necessary.
If the input contains 'solve():', create a complete function implementation.
For input/output handling:
- Use appropriate input methods for the language
- Include all necessary imports
- Handle the input parsing inside the function
{self.prefix_var.get()}"""

            pyperclip.copy("")
            while not self.stop_typing:
                current_clipboard_content = pyperclip.paste()
                if current_clipboard_content != self.previous_clipboard_content:
                    try:
                        # Format the input if it's a solve() pattern
                        if "solve():" in current_clipboard_content:
                            prompt = f"{base_prompt}\nImplement the following function:\n{current_clipboard_content}"
                        else:
                            prompt = f"{base_prompt}\n{current_clipboard_content}"
                            
                        response = model.generate_content(prompt, generation_config=generation_config)
                        no_indent_text = self.remove_indents(response.text)
                        
                        # Prepare editor
                        self.prepare_editor()
                        
                        # Type the code
                        if self.humantype:
                            self.type_text_human_like(no_indent_text)
                        else:
                            self.fast_type(no_indent_text)
                        
                        self.previous_clipboard_content = current_clipboard_content
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")
                time.sleep(0.5)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize AI model: {str(e)}")

    def prepare_editor(self) -> None:
        """Prepare the editor for code input"""
        keyboard_controller.press(Key.tab)
        keyboard_controller.release(Key.tab)
        time.sleep(0.5)
        
        modifier_key = 'command' if self.os_name == 'Darwin' else 'ctrl'
        pyautogui.hotkey(modifier_key, 'a')
        time.sleep(1)
        
        if self.os_name == 'Darwin':
            pyautogui.hotkey('command', 'shift', 'down')
        else:
            keyboard_controller.press(Key.ctrl)
            keyboard_controller.press(Key.shift)
            keyboard_controller.press(Key.end)
            keyboard_controller.release(Key.end)
            keyboard_controller.release(Key.shift)
            keyboard_controller.release(Key.ctrl)
        
        time.sleep(0.5)
        pyautogui.press('backspace')

    def start_monitoring(self):
        self.stop_typing = False
        monitor_thread = threading.Thread(target=self.monitor_clipboard_and_type)
        monitor_thread.daemon = True
        monitor_thread.start()

    def stop_typing_text(self):
        self.stop_typing = True
        time.sleep(1)
        self.stop_typing = False

    def on_press(self, key):
        if key == Key.shift:
            self.stop_typing_text()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    bot = CodeTypingBot()
    bot.run()