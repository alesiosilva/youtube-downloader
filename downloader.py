from pytube import YouTube

url = input('Informe a URL do vídeo ou playlist: \n')

def validatePlaylist(url):
    return url.__contains__('/playlist?list=')

youtube = YouTube(url)

if (validatePlaylist(url)==False):
    print('Iniciando o download do vídeo: ', youtube.title, ...)
    stream = youtube.streams.get_by_itag(22)
    stream.download()
else:
    print('Iniciando o download da Playlist: ', youtube.title, ...)
    for video in youtube.videos:
        video.streams.first().download()

print('Download concluído!!!')