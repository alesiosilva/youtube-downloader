import time
from pytube import Playlist, YouTube
from pytube.cli import on_progress
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
itag = StringVar()

label = Label(panel1, text='URL: ', font=('', 12))
entry = Entry(panel1, width=80)
audioLabel = Label(panel2, text='Áudio: ')
videoLabel = Label(panel2, text='Resolução do Vídeo: ')
percentLabel = Label(panel3, text='0%')

abr128 = ttk.Radiobutton(panel2, text='128kbps / mp4', variable=itag, value='140')
abr48 = ttk.Radiobutton(panel2, text='48kbps / mp4', variable=itag, value='139')
res144 = ttk.Radiobutton(panel2, text='144p / mp4', variable=itag, value='160')
res360 = ttk.Radiobutton(panel2, text='360p / mp4', variable=itag, value='18')
res720 = ttk.Radiobutton(panel2, text='720p / mp4', variable=itag, value='22')
res1080 = ttk.Radiobutton(panel2, text='1080p / mp4', variable=itag, value='137')

progBar = ttk.Progressbar(panel3, orient=HORIZONTAL, length=560, maximum=100, mode='determinate')
outText = Text(panel3, width=70)

label.place(x=5, y=40, height=30)
entry.place(x=80, y=40, height=30)
percentLabel.place(x=5, y=20, height=20)
progBar.place(x=5, y=40, height=20)
outText.place(x=5, y=70, height=225)
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
        jan.update_idletasks()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100
    percentage_str = str(int(percentage))
    percentLabel.configure(text=percentage_str + '%')
    percentLabel.update()
    progBar['value'] = (float(percentage))
    progBar.update()

def completed(a, b):
    print('Completed!')

def videoDownload(url: str, dirname: str):
    progBar['value'] = 0.0
    time.sleep(0.3)

    video = YouTube(url, on_progress_callback=on_progress, on_complete_callback=completed)
    #mp4 = video.streams.filter(progressive=True, file_extension='mp4')
    #outText.insert('1.0', mp4)
    #barLoading()

    stream = getStream(itag, video)
    message = videoMessage(video, stream)
    outText.insert('end', message)
    outText.update()
    stream.download(dirname)
    
def videoMessage(video: YouTube, stream):
    message = '\nDownload do vídeo concluído com sucesso!\n'
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
            while(dirname):
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
            while(dirname):
                for url in playlist.video_urls:
                    try: 
                        videoDownload(url, dirname)
                    except Exception as e:
                        messagebox.showerror(title='Erro no download do vídeo: ', message=e)
                messagebox.showinfo(title='Download concluído:', message=playlist.title)
            else:
                messagebox.showwarning(title='Download Cancelado', message='Selecione o diretório para o download')
                                        
        except Exception as e:
            messagebox.showerror(title='Erro na URL da Playlist:', message=e)

# Botões
button = Button(panel2, text='Download', width=10, command=download)
button.place(x=250, y=60, height=25)

jan.mainloop()