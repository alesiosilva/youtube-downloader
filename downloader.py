import time
import os
from pytube import Playlist, YouTube
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Janela
jan = Tk()
jan.title('Youtube Downloader -by Alésio Torres!')
jan.geometry('800x600')
jan.configure(background='white')
jan.resizable(width=False, height=False)
jan.attributes('-alpha', 0.98)

# Widgets
leftFrame = Frame(jan, width=200, height=600, bg='GRAY', relief='raise')
leftFrame.pack(side=LEFT)
rightFrame = Frame(jan, width=595, height=600, bg='WHITE', relief='raise')
rightFrame.pack(side=RIGHT)

# Campos
label = Label(rightFrame, text='URL: ', font=('', 12), bg='WHITE', fg='BLACK', anchor=E)
label.place(x=5, y=200, height=30)
entry = Entry(rightFrame, width=80)
entry.place(x=80, y=200, height=30)
progLabel = Label(rightFrame, text='Progresso:', bg='WHITE', fg='BLACK')
progLabel.place(x=5, y=300, height=20)
outText = Text(rightFrame, width=70)
outText.place(x=5, y=320, height=250) 

#url = input('Informe a URL do vídeo ou playlist: \n')

# Funções

def validatePlaylist(url):
    return url.__contains__('&list=')

def download():
    url = entry.get()
    if (validatePlaylist(url)==False):
        try:
            video = YouTube(url)
        except Exception as e:
            messagebox.showerror(title='Erro na URL do vídeo: ', message=e)
        else:
            progress = 'Iniciando o download do vídeo: \n'
            progress += video.title
            progress += '...\n\n'
            outText.insert('1.0', progress)

            dirname = filedialog.askdirectory()
            stream = video.streams.get_by_itag(22)
            time.sleep(1)
            stream.download(dirname)
            messagebox.showinfo(title='Download concluído:', message='Download concluído com sucesso!')

    else:
        try:
            playlist = Playlist(url)
        except Exception as e:
            messagebox.showerror(title='Erro na URL da Playlist:', message=e)
        else:
            progress = 'Iniciando o download da Playlist: \n'
            progress += playlist.title
            progress += '...\n\n'
            outText.insert('1.0', progress)
            for url in playlist.video_urls:
                try: 
                    video = YouTube(url)
                except Exception as e:
                    messagebox.showerror(title='Erro no download do vídeo: ', message=e)
                else:
                    progress += 'Baixando o vídeo: '
                    progress += video.title
                    progress += '...\n\n'
                    outText.insert('1.0', progress)

                    dirname = filedialog.askdirectory()
                    time.sleep(1)
                    video.streams.first().download(dirname)
            messagebox.showinfo('Downloads concluídos: ', message='Downloads concluídos com sucesso!')

# Botões
button = Button(rightFrame, text='Download', width=10, command=download)
button.place(x=280, y=250, height=25)

jan.mainloop()