from pytube import Playlist, YouTube

url = input('Informe a URL do vídeo ou playlist: \n')

def validatePlaylist(url):
    return url.__contains__('/playlist?list=')

if (validatePlaylist(url)==False):
    try:
        video = YouTube(url)
    except Exception as e:
        print('Erro: ', e)
    else:
        print('Iniciando o download do vídeo: ', video.title, ...)
        stream = video.streams.get_by_itag(22)
        stream.download()
        print('Download concluído!!!')

else:
    try:
        playlist = Playlist(url)
    except Exception as e:
        print('Erro: ', e)
    else:
        print('Iniciando o download da Playlist: ', playlist.title, ...)
        for video in playlist.videos:
            video.streams.first().download()
        print('Downloads concluídos!!!')
