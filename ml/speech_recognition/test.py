from asrecognition import ASREngine

asr = ASREngine("ru", model_path="jonatasgrosman/wav2vec2-large-xlsr-53-russian")

audio_paths = ["/home/user/Downloads/запись.mp3"]
transcriptions = asr.transcribe(audio_paths)
for transcription in transcriptions:
    print(transcription['transcription'])
