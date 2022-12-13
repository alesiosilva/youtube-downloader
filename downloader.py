from pytube import YouTube

video = YouTube(input('Informe a URL do vídeo ou playlist: \n'))

print('Iniciando o download do vídeo ', video.title, ...)

stream = video.streams.get_by_itag(22)

stream.download()

print('Download concluído! \n\n\n')