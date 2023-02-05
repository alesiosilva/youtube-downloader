from pytube import Playlist, YouTube
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

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

entry = StringVar()
stream = StringVar()

label = Label(panel1, text='URL: ', font=('', 12))
entry = Entry(panel1, width=80)
audioLabel = Label(panel2, text='Áudio: ')
videoLabel = Label(panel2, text='Vídeo: ')

abr128 = ttk.Radiobutton(panel2, text='128kbps / mp4', variable=stream, value='140')
abr48 = ttk.Radiobutton(panel2, text='48kbps / mp4', variable=stream, value='139')
res144 = ttk.Radiobutton(panel2, text='144p / mp4', variable=stream, value='160')
res360 = ttk.Radiobutton(panel2, text='360p / mp4', variable=stream, value='18')
res720 = ttk.Radiobutton(panel2, text='720p / mp4', variable=stream, value='22')
res1080 = ttk.Radiobutton(panel2, text='1080p / mp4', variable=stream, value='137')

progBar = ttk.Progressbar(panel3, orient=HORIZONTAL, length=560, mode='determinate')
outText = Text(panel3, width=70)

label.place(x=5, y=40, height=30)
entry.place(x=80, y=40, height=30)
outText.place(x=5, y=60, height=220)
progBar.place(x=5, y=20, height=20)
#audioLabel.place(x=5, y=20)
#abr128.place(x=5, y=60)
#abr48.place(x=5, y=80)
videoLabel.place(x=5, y=30)
#res144.place(x=150, y=60)
res360.place(x=5, y=60)
res720.place(x=5, y=80)
#res1080.place(x=250, y=80)

#url = input('Informe a URL do vídeo ou playlist: \n')

# Funções

def validatePlaylist(url):
    return url.__contains__('&list=')

def getStream(stream: str, video: YouTube, dirname: str):
    itag = stream.get()
    if itag:
        return video.streams.get_by_itag(itag).download(dirname)
    else:
        return video.streams.last().download(dirname)

def download():
    url = entry.get()
    if (validatePlaylist(url)==False):
        try:
            video = YouTube(url)
        except Exception as e:
            messagebox.showerror(title='Erro na URL do vídeo: ', message=e)
        else:
            progress = '\n Iniciando o download do vídeo: \n'
            progress += video.title
            outText.insert('1.0', progress)

            #mp4 = video.streams.filter(progressive=True, file_extension='mp4')
            #outText.insert('1.0', mp4)
            getStream(stream, video, dirname=filedialog.askdirectory())
            messagebox.showinfo(title='Download concluído:', message='Download concluído com sucesso!')

    else:
        try:
            playlist = Playlist(url)
        except Exception as e:
            messagebox.showerror(title='Erro na URL da Playlist:', message=e)
        else:
            progress = '\nIniciando o download da Playlist:\n'
            progress += playlist.title
            outText.insert('1.0', progress)

            for url in playlist.video_urls:
                try: 
                    video = YouTube(url)
                except Exception as e:
                    messagebox.showerror(title='Erro no download do vídeo: ', message=e)
                else:
                    progress += '\n\n Baixando o vídeo: '
                    progress += video.title
                    outText.insert('1.0', progress)

                    getStream(stream, video, dirname = filedialog.askdirectory())
                    
            messagebox.showinfo('Downloads concluídos: ', message='Downloads concluídos com sucesso!')

# Botões
button = Button(panel2, text='Download', width=10, command=download)
button.place(x=250, y=60, height=25)

jan.mainloop()