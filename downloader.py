from pytube import Playlist, YouTube

url = input('Informe a URL do vídeo ou playlist: \n')

def validatePlaylist(url):
    return url.__contains__('&list=')

if (validatePlaylist(url)==False):
    try:
        video = YouTube(url)
    except Exception as e:
        print('Erro: ', e)
    else:
        print('Iniciando o download do vídeo: ', video.title, '...')
        stream = video.streams.get_by_itag(22)
        stream.download()
        print('Download concluído!!!')

else:
    try:
        playlist = Playlist(url)
    except Exception as e:
        print('Erro: ', e)
    else:
        print('Iniciando o download da Playlist: ', playlist.title, '...')
        for url in playlist.video_urls:
            try: 
                video = YouTube(url)
            except Exception as e:
                print('Error: ', e)
            else:
                print('Baixando o vídeo: ', video.title, '...')
                video.streams.first().download()
        print('Downloads concluídos!!!')
