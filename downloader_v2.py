import time
from pytube import Playlist, YouTube
from pytube.cli import on_progress
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk

# System Settings
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

# App Frames
app = ctk.CTk()
app.title('Youtube Downloader -by Alésio Torres!')
app.geometry('800x600')
app.resizable(width=False, height=False)
app.attributes('-alpha', 0.98)

# UI Elements

entry = StringVar()
itag = StringVar()

label = ctk.CTkLabel(app, text='Insira a URL do YouTube: ')
entry = ctk.CTkEntry(app, width=550, height=40)
audioLabel = ctk.CTkLabel(app, text='Áudio: ')
videoLabel = ctk.CTkLabel(app, text='Resolução do Vídeo: ')
percentLabel = ctk.CTkLabel(app, text='0%')

abr128 = ctk.CTkRadioButton(app, text='128kbps / mp4', variable=itag, value='140')
abr48 = ctk.CTkRadioButton(app, text='48kbps / mp4', variable=itag, value='139')
res144 = ctk.CTkRadioButton(app, text='144p / mp4', variable=itag, value='160')
res360 = ctk.CTkRadioButton(app, text='360p / mp4', variable=itag, value='18')
res720 = ctk.CTkRadioButton(app, text='720p / mp4', variable=itag, value='22')
res1080 = ctk.CTkRadioButton(app, text='1080p / mp4', variable=itag, value='137')

progBar = ctk.CTkProgressBar(app, width=560)
progBar.set(0)
outText = ctk.CTkTextbox(app, width=800)

label.pack(padx=10, pady=10)
entry.pack()
percentLabel.pack(padx=10, pady=10)
progBar.pack(padx=10, pady=10)
videoLabel.pack(padx=10, pady=10)
res360.pack(padx=10, pady=10)
res720.pack(padx=10, pady=10)
outText.pack(padx=10, pady=10)

# Funções

def isPlaylist(url):
    return url.__contains__('&list=')

def getStream(filtered_stream: str, video: YouTube):
    itag = filtered_stream.get()
    if itag:
        return video.streams.get_by_itag(itag)
    else:
        return video.streams.get_highest_resolution()

def barLoading():
    progBar['value'] = 0
    for i in range(10):
        time.sleep(0.5)
        progBar['value'] += 10
        app.update_idletasks()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100
    percentage_str = str(int(percentage))
    percentLabel.configure(text=percentage_str + '%')
    percentLabel.update()
    progBar.set(float(percentage) / 100)

def completed(a, b):
    print('Completed!')

def videoDownload(url: str, dirname: str):
    video = YouTube(url, on_progress_callback=on_progress, on_complete_callback=completed)
    #barLoading()

    stream = getStream(itag, video)
    message = videoMessage(video, stream)
    outText.insert('end', message)
    outText.update()
    stream.download(dirname)
    
def videoMessage(video: YouTube, stream):
    message = '\nEfetuando download do vídeo!\n'
    message += 'Title: ' + stream.title
    message += '\nFile Size: ' + str(stream.filesize/1000000)
    message += ' MB\nLength: ' + str(video.length / 60) + ' Minutes'
    message += '\nAuthor: ' + video.author + '\n'
    return message

def download():
    url = entry.get()
    if (isPlaylist(url)==False):
        try:
            dirname=filedialog.askdirectory()
            if(dirname):
                videoDownload(url, dirname)              
                messagebox.showinfo(title='Download concluído:', message=url)
            else:
                messagebox.showwarning(title='Download Cancelado', message='Selecione o diretório para o download')
        except Exception as e:
            messagebox.showerror(title='Erro no download do vídeo: ', message=e)
    else:
        try:
            playlist = Playlist(url)
            progress = '\nIniciando o download da Playlist:\n' + playlist.title + '\n'
            outText.insert('end', progress)
            dirname = filedialog.askdirectory()
            if(dirname):
                for url in playlist.video_urls:
                    try: 
                        videoDownload(url, dirname)
                    except Exception as e:
                        messagebox.showerror(title='Erro no download do vídeo: ', message=e)
                messagebox.showinfo(title='Download concluído:', message=playlist.title)
                dirname = None
            else:
                messagebox.showwarning(title='Download Cancelado', message='Selecione o diretório para o download')
                                        
        except Exception as e:
            messagebox.showerror(title='Erro na URL da Playlist:', message=e)

# Button
button = ctk.CTkButton(app, text='Download', command=download)
button.pack(padx=10, pady=10)

# Run App
app.mainloop()