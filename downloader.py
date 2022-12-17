from pytube import Playlist, YouTube

url = input('Informe a URL do vídeo ou playlist: \n')

def validatePlaylist(url):
    return url.__contains__('/playlist?list=')

try:
    if (validatePlaylist(url)==False):
        video = YouTube(url)
    else:
        playlist = Playlist(url)

except:
    print('Erro: URL incompatível ou bloqueada para download!')

else:
    if (validatePlaylist(url)==False):
        print('Iniciando o download do vídeo: ', video.title, ...)
        stream = video.streams.get_by_itag(22)
        stream.download()
    else:
        print('Iniciando o download da Playlist: ', playlist.title, ...)
        for video in playlist.videos:
            video.streams.first().download()

print('Download concluído!!!')