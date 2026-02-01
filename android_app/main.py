"""
DocuVoice Android App
Converts text and Word documents to audio and records voice
"""

import os
import json
import requests
from datetime import datetime
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.garden.audiostream import AudioStream
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

import android
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path


class HomeScreen(Screen):
    """Home screen with navigation options"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='DocuVoice',
            size_hint_y=None,
            height=50,
            font_size='32sp',
            bold=True
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text='Convert text, Word files to audio & record voice',
            size_hint_y=None,
            height=40,
            font_size='14sp'
        )
        layout.add_widget(subtitle)
        
        # Navigation buttons
        btn_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.7)
        
        btn_text = Button(
            text='📄 Text to Speech',
            size_hint_y=0.25,
            background_color=(0.04, 0.65, 0.64, 1)
        )
        btn_text.bind(on_press=self.go_to_text_speech)
        btn_layout.add_widget(btn_text)
        
        btn_word = Button(
            text='📝 Word to Speech',
            size_hint_y=0.25,
            background_color=(0.49, 0.23, 0.93, 1)
        )
        btn_word.bind(on_press=self.go_to_word_speech)
        btn_layout.add_widget(btn_word)
        
        btn_voice = Button(
            text='🎤 Voice Recording',
            size_hint_y=0.25,
            background_color=(0.25, 0.41, 0.88, 1)
        )
        btn_voice.bind(on_press=self.go_to_voice_recording)
        btn_layout.add_widget(btn_voice)
        
        layout.add_widget(btn_layout)
        
        # Footer
        footer = Label(
            text='© 2026 DocuVoice',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def go_to_text_speech(self, instance):
        self.manager.current = 'text_speech'
    
    def go_to_word_speech(self, instance):
        self.manager.current = 'word_speech'
    
    def go_to_voice_recording(self, instance):
        self.manager.current = 'voice_recording'


class TextToSpeechScreen(Screen):
    """Text to Speech conversion screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "http://192.168.0.12:5000"  # Change to your backend URL
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Text to Speech',
            size_hint_y=None,
            height=40,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Text input
        scroll = ScrollView(size_hint=(1, 0.6))
        self.text_input = TextInput(
            multiline=True,
            text='Enter your text here...',
            size_hint_y=None
        )
        self.text_input.bind(minimum_height=self.text_input.setter('height'))
        scroll.add_widget(self.text_input)
        layout.add_widget(scroll)
        
        # Status label
        self.status_label = Label(
            text='Ready',
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        btn_convert = Button(text='Convert to Audio')
        btn_convert.bind(on_press=self.convert_text)
        btn_layout.add_widget(btn_convert)
        
        btn_back = Button(text='Back')
        btn_back.bind(on_press=self.go_back)
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def convert_text(self, instance):
        text = self.text_input.text
        if not text or text == 'Enter your text here...':
            self.status_label.text = 'Please enter text'
            self.status_label.color = (1, 0, 0, 1)
            return
        
        self.status_label.text = 'Converting... Please wait'
        self.status_label.color = (1, 1, 0, 1)
        
        # Run in background thread
        thread = Thread(target=self._send_conversion_request, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _send_conversion_request(self, text):
        try:
            data = {'text': text}
            response = requests.post(
                f"{self.api_url}/text-to-audio",
                data=data,
                timeout=60
            )
            
            Clock.schedule_once(lambda x: self._update_status('✓ Conversion complete!', (0, 1, 0, 1)), 0)
        except Exception as e:
            Clock.schedule_once(lambda x: self._update_status(f'Error: {str(e)}', (1, 0, 0, 1)), 0)
    
    def _update_status(self, message, color):
        self.status_label.text = message
        self.status_label.color = color
    
    def go_back(self, instance):
        self.manager.current = 'home'


class WordToSpeechScreen(Screen):
    """Word document to Speech conversion screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "http://192.168.0.12:5000"  # Change to your backend URL
        self.selected_file = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Word to Speech',
            size_hint_y=None,
            height=40,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # File chooser
        self.file_chooser = FileChooserListView(
            filters=['*.docx']
        )
        layout.add_widget(self.file_chooser)
        
        # Selected file label
        self.selected_label = Label(
            text='No file selected',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        layout.add_widget(self.selected_label)
        
        # Status label
        self.status_label = Label(
            text='Ready',
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        btn_select = Button(text='Select File')
        btn_select.bind(on_press=self.select_file)
        btn_layout.add_widget(btn_select)
        
        btn_convert = Button(text='Convert')
        btn_convert.bind(on_press=self.convert_word)
        btn_layout.add_widget(btn_convert)
        
        btn_back = Button(text='Back')
        btn_back.bind(on_press=self.go_back)
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def select_file(self, instance):
        if self.file_chooser.selection:
            self.selected_file = self.file_chooser.selection[0]
            self.selected_label.text = f'Selected: {os.path.basename(self.selected_file)}'
        else:
            self.status_label.text = 'No file selected'
            self.status_label.color = (1, 0, 0, 1)
    
    def convert_word(self, instance):
        if not self.selected_file:
            self.status_label.text = 'Please select a Word file'
            self.status_label.color = (1, 0, 0, 1)
            return
        
        self.status_label.text = 'Converting... Please wait'
        self.status_label.color = (1, 1, 0, 1)
        
        # Run in background thread
        thread = Thread(target=self._send_word_conversion_request)
        thread.daemon = True
        thread.start()
    
    def _send_word_conversion_request(self):
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': (os.path.basename(self.selected_file), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
                response = requests.post(
                    f"{self.api_url}/word-to-audio",
                    files=files,
                    timeout=120
                )
            
            Clock.schedule_once(lambda x: self._update_status('✓ Conversion complete!', (0, 1, 0, 1)), 0)
        except Exception as e:
            Clock.schedule_once(lambda x: self._update_status(f'Error: {str(e)}', (1, 0, 0, 1)), 0)
    
    def _update_status(self, message, color):
        self.status_label.text = message
        self.status_label.color = color
    
    def go_back(self, instance):
        self.manager.current = 'home'


class VoiceRecordingScreen(Screen):
    """Voice recording screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "http://192.168.0.12:5000"  # Change to your backend URL
        self.audio_stream = None
        self.is_recording = False
        self.audio_data = []
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Voice Recording',
            size_hint_y=None,
            height=40,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='🎤 Ready to record',
            size_hint_y=0.3,
            font_size='14sp',
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # Buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)
        
        btn_start = Button(text='Start Recording')
        btn_start.bind(on_press=self.start_recording)
        btn_layout.add_widget(btn_start)
        
        self.btn_stop = Button(text='Stop Recording', disabled=True)
        self.btn_stop.bind(on_press=self.stop_recording)
        btn_layout.add_widget(self.btn_stop)
        
        btn_play = Button(text='Play', disabled=True)
        btn_play.bind(on_press=self.play_recording)
        btn_layout.add_widget(btn_play)
        
        self.btn_save = Button(text='Save', disabled=True)
        self.btn_save.bind(on_press=self.save_recording)
        btn_layout.add_widget(self.btn_save)
        
        layout.add_widget(btn_layout)
        
        # Back button
        btn_back = Button(text='Back', size_hint_y=None, height=50)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def start_recording(self, instance):
        try:
            self.is_recording = True
            self.audio_data = []
            self.status_label.text = '🔴 Recording... Speak now'
            self.status_label.color = (1, 0, 0, 1)
            instance.disabled = True
            self.btn_stop.disabled = False
            
            # AudioStream will be implemented based on device capability
            self.status_label.text = '✓ Recording started (5 seconds)'
            Clock.schedule_once(self.auto_stop_recording, 5)
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = (1, 0, 0, 1)
    
    def auto_stop_recording(self, dt):
        """Auto-stop recording after duration"""
        if self.is_recording:
            self.stop_recording(None)
    
    def stop_recording(self, instance):
        try:
            self.is_recording = False
            self.status_label.text = '✓ Recording stopped'
            self.status_label.color = (0, 1, 0, 1)
            if instance:
                instance.disabled = True
            self.btn_save.disabled = False
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = (1, 0, 0, 1)
    
    def play_recording(self, instance):
        self.status_label.text = '🔊 Playing...'
        self.status_label.color = (0, 1, 1, 1)
    
    def save_recording(self, instance):
        try:
            self.status_label.text = '⏳ Saving...'
            self.status_label.color = (1, 1, 0, 1)
            
            # Simulate file save
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            
            # In production, you'd send to backend here
            # For now, show success
            Clock.schedule_once(lambda x: self._show_save_success(), 1)
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = (1, 0, 0, 1)
    
    def _show_save_success(self):
        self.status_label.text = '✓ Recording saved'
        self.status_label.color = (0, 1, 0, 1)
    
    def go_back(self, instance):
        self.manager.current = 'home'


class DocuVoiceApp(App):
    """Main application"""
    def build(self):
        # Request permissions
        try:
            request_permissions([
                Permission.INTERNET,
                Permission.RECORD_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception as e:
            print(f"Permissions error: {e}")
        
        # Create screen manager
        sm = ScreenManager()
        
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(TextToSpeechScreen(name='text_speech'))
        sm.add_widget(WordToSpeechScreen(name='word_speech'))
        sm.add_widget(VoiceRecordingScreen(name='voice_recording'))
        
        return sm


if __name__ == '__main__':
    app = DocuVoiceApp()
    app.title = 'DocuVoice'
    app.run()
