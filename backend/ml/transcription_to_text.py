
def json_to_md(transcription):
    lines = ""
    for data in transcription:
        start_ms = data['start_ms']
        transcription = data['transcription']
        minutes = start_ms / 3600
        seconds = start_ms / 60
        lines += f'**{minutes}:{seconds}** {transcription}\n'
        
    return lines
