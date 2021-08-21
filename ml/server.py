if __name__ == "__main__":
    # loading your model and preparing the input data
    from werkzeug.utils import secure_filename
    from flask import Flask, flash, request, redirect, url_for
    
    from threading import Thread
    import os
    import subprocess
    import nemo
    import os
    import torch
    import nemo.collections.asr as nemo_asr
    import pathlib
    import json

    
    golos = nemo_asr.models.EncDecCTCModel.restore_from("QuartzNet15x5_golos.nemo")
    vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                  model='silero_vad')
    (get_speech_ts,
     get_speech_ts_adaptive,
     save_audio,
     read_audio,
     state_generator,
     single_audio_stream,
     collect_chunks) = utils
    # ...
    
    ### MODEL CREATION AND DATA PREPROCESSING ###
    # Create a function or functions for preprocessing the input data
    # This can be normalizing price data, augmenting images, etc.
    def preprocess_file(path):
        pre,ext = os.path.splitext(path)
        wav_path = f'{pre}.wav'
        subprocess.call(f'ffmpeg -i path -acodec pcm_s16le -ac 1 -ar 16000 {wav_path}', shell=True)
        pathlib.Path(pre).mkdir(parents=True, exist_ok=True)
        print(f'Created file {pre}')

        wav = read_audio(wav_path)
        speech_timestamps =  get_speech_ts_adaptive(wav, vad_model)
        audio_files = []
        for i,region in enumerate(speech_timestamps):
            start_sample = region['start']
            end_sample = region['end']
            start_ms = start_sample / 16
            file  = f'{pre}/regioni_{i}.wav'
            
            audio_files.append({'start_ms' : start_ms, 'file': file}) 
            save_audio(file, wav[start_sample:end_sample])
        return audio_files 
    
    def transcribe_audio_files(audio_files):
        results = []
        files = []
        for audio in audio_files:
            file = audio['file']
            files.append(file)
    
        transcriptions = golos.transcribe(files)    
        for file, transcription in zip(audio_files,transcriptions):
            results.append({'transcription': transcription, 'start_ms':file['start_ms']})
    
        return results
    
    
    ### SETTING UP FLASK APP AND FLAKS ENDPOINTS ###
    # Create the flaks App
    UPLOAD_FOLDER = 'uploads/'
    RESULTS_FOLDER = 'results/'
    app = Flask(__name__)
    
    pathlib.Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    pathlib.Path(RESULTS_FOLDER).mkdir(parents=True, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
    def run_background(path, file_id):
        audio_files = preprocess_file(path)
        transcribed = transcribe_audio_files(audio_files)
        results_folder = app.config['RESULTS_FOLDER']

        output_file = os.path.join(results_folder, f'{file_id}.json')
        with open(output_file,"w") as f:
            json.dump(transcribed,f,ensure_ascii=False)


        
    def get_file_id_path(file_id):
        results_folder = app.config['RESULTS_FOLDER']
        return os.path.join(results_folder, f'{file_id}.json')

    
    # Define an endpoint for calling the predict function based on your ml library/framework
    @app.route("/status", methods=["GET"])
    def status():
        file_id = request.args.get('file_id')
        file_exist = os.path.exists(get_file_id_path(file_id))
        if file_exist:
            with open(get_file_id_path(file_id)) as json_file:
                data = json.load(json_file)
                return {'status': 'transcription complete', 'data': data } 
        else:
            return {'status': 'transcribing'}




    @app.route("/transcribe", methods=["POST"])
    def predict():
        # Load the Input
        data = request.files['file'] # file input 
        
        if data.filename == '':
            flash('No selected file')
    
        filename = secure_filename(data.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        data.save(path)
        pathObject = pathlib.Path(path)
        filename = pathObject.name
        file_id,ext = os.path.splitext(filename)

        if os.path.exists(get_file_id_path(file_id)):
            os.remove(get_file_id_path(file_id))
        thread = Thread(target=run_background, args=(path,file_id))
        thread.daemon = True
        thread.start()
    
        return json.dumps({'status': 'transciption started', 'file_id': file_id},ensure_ascii=False).encode('utf8')
      
      
    # Start the flask app and allow remote connections
    app.run(host='0.0.0.0', port = 9090)



