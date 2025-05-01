from TTS.api import TTS

# Initialize the TTS model once (using a lightweight English model)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text: str):
    tts.tts_to_file(text=text, file_path="rima_output.wav")
    
    # Play it using ffplay or any media player
    import os
    os.system("ffplay -nodisp -autoexit rima_output.wav >/dev/null 2>&1")
