from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
import helpers
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from pytube import YouTube 
import sys, time
from functools import partial
from kivy.uix.label import Label

class MyApp(MDApp):
	def build(self):
		self.theme_cls.primary_palette="Blue"
		screen = Screen()
		self.url = Builder.load_string(helpers.url_input)
		label = Label(text="Youtube Video Downloader",pos_hint={'center_x':0.5, 'center_y':0.7},color=[0,0,0,1])
		button = MDRectangleFlatButton(text='Download',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       on_release=self.download_video)
		screen.add_widget(self.url)
		screen.add_widget(label)
		screen.add_widget(button)
		return screen
	previousprogress = 0
	def on_progress(stream, chunk, bytes_remaining):
	    global previousprogress
	    total_size = stream.filesize
	    bytes_downloaded = total_size - bytes_remaining
	    liveprogress = (int)(bytes_downloaded / total_size * 100)
	    if liveprogress > previousprogress:
	          previousprogress = liveprogress
	          time.sleep(1)
	          sys.stdout.write("\r%d%%" % liveprogress)
	          sys.stdout.flush()
	def get_video(self, stream):
		if self.image_loaded == True:
			stream.download()
			# kivymd.toast("video is downloading...", 1)
	
	def download_video(self, obj):
		if self.url.text is not "":
			url_error = YouTube(self.url.text)
			self.image_loaded = True
			self.url_error.register_on_progress_callback(on_progress)
			self.get_video(url_error.streams.first())
		
		else:
			url_error = "Please enter a url"
		self.dialog = MDDialog(title='Url check',
                               text=url_error, size_hint=(0.9, 1),
                               buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)
                                      ])
		self.dialog.open()

	def close_dialog(self, obj):
		self.dialog.dismiss()
	def pasteURL(self):
		self.ids.txt_input.text = Clipboard.paste()

if __name__ == '__main__':
	MyApp().run()
