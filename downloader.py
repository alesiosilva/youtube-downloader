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

# Painéis
panel1 = PanedWindow(rightFrame, orient=VERTICAL)
panel2 = PanedWindow(rightFrame, orient=VERTICAL)
panel3 = PanedWindow(rightFrame, orient=VERTICAL)

labelFrame1 = LabelFrame(panel1, text='Download: ', width=580, height=100)
labelFrame2 = LabelFrame(panel2, text='Opções: ', width=580, height=150)
labelFrame3 = LabelFrame(panel3, text='Progresso: ', width=580, height=300)

panel1.add(labelFrame1)
panel2.add(labelFrame2)
panel3.add(labelFrame3)

panel1.place(x=5, y=5)
panel2.place(x=5, y=115)
panel3.place(x=5, y=275)

# Campos
label = Label(panel1, text='URL: ', font=('', 12))
entry = Entry(panel1, width=80)
outText = Text(panel3, width=70)

label.place(x=5, y=20, height=30)
entry.place(x=80, y=20, height=30)
outText.place(x=5, y=20, height=250) 

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
                    video.streams.first().download(dirname)
            messagebox.showinfo('Downloads concluídos: ', message='Downloads concluídos com sucesso!')

# Botões
button = Button(panel1, text='Download', width=10, command=download)
button.place(x=280, y=60, height=25)

jan.mainloop()