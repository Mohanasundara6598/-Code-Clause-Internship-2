import tkinter as tk
from tkinter import filedialog, messagebox, Scale, HORIZONTAL, Listbox
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import pygame
import os


pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("SM Music Player")
        self.root.geometry("600x400")
        self.is_playing = False
        self.is_paused = False
        self.current_track_index = None
        self.playlist = []
        self.album_art_label = tk.Label(self.root, text="Welcom", width=20, height=10)
        self.album_art_label.pack(pady=10)
        self.playlist_box = Listbox(self.root, selectmode=tk.SINGLE, width=50, height=10)
        self.playlist_box.pack(pady=10)
        self.playlist_box.bind("<<ListboxSelect>>", self.select_track)

        self.load_button = tk.Button(self.root, text="Load Music", command=self.load_music)
        self.load_button.pack(pady=5)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_music)
        self.resume_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_track)
        self.next_button.pack(pady=5)

        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_track)
        self.previous_button.pack(pady=5)

        self.volume_scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, label="Volume")
        self.volume_scale.set(100)
        self.volume_scale.pack(pady=10)
        self.volume_scale.bind("<Motion>", self.change_volume)

        self.track_label = tk.Label(self.root, text="No track loaded")
        self.track_label.pack(pady=10)

    def load_music(self):
        files = filedialog.askopenfilenames(title="Select Music Files",filetypes=(("MP3 Files", "*.mp3"),("WAV Files", "*.wav")))
        if files:
            for file_path in files:
                self.playlist.append(file_path)
                self.playlist_box.insert(tk.END, os.path.basename(file_path))
            self.update_album_art()

    def get_track_duration(self, track):
        audio = MP3(track)
        return audio.info.length

    def select_track(self, event):
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.current_track_index = selected_index[0]
            self.update_album_art()
            self.track_label.config(text=os.path.basename(self.playlist[self.current_track_index]))

    def update_album_art(self):
        if self.current_track_index is not None and self.current_track_index < len(self.playlist):
            track = self.playlist[self.current_track_index]
            try:
                audio = MP3(track, ID3=ID3)
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        album_art = Image.open(tag.data)
                        album_art = album_art.resize((200, 200), Image.ANTIALIAS)
                        album_art = ImageTk.PhotoImage(album_art)
                        self.album_art_label.config(image=album_art)
                        self.album_art_label.image = album_art
                        return
            except Exception:
                pass
        self.album_art_label.config(image='', text="No Album Art")

    def play_music(self):
        if self.current_track_index is None:
            self.current_track_index = 0
        if self.playlist:
            track = self.playlist[self.current_track_index]
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.track_label.config(text=os.path.basename(track))
            self.update_album_art()
        else:
            messagebox.showwarning("Warning", "Playlist is empty.")

    def pause_music(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_music(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False

    def next_track(self):
        if self.current_track_index is not None and self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self.play_music()

    def previous_track(self):
        if self.current_track_index is not None and self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_music()

    def change_volume(self, event):
        volume = self.volume_scale.get() / 100
        pygame.mixer.music.set_volume(volume)


if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
