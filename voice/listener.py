import torch
import torchaudio
import pyaudio
import numpy as np
from silero_vad import load_silero_vad
import tempfile
import whisper
import time

# Audio recording parameters - CRITICAL: CHUNK must be 512 for Silero VAD at 16kHz
CHUNK = 512  # Must be 512 for Silero VAD at 16kHz sampling rate
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# VAD parameters
SPEECH_THRESHOLD = 0.5
MAX_SILENCE_DURATION = 1.5  # Maximum silence duration before stopping recording

# Load the VAD model
model = load_silero_vad()

# Load the Whisper model
whisper_model = whisper.load_model("base")

def record_audio(max_duration=30):
    """Record audio from the default microphone with natural speech detection.

    Args:
        max_duration (int): Maximum recording duration in seconds. Defaults to 30.

    Returns:
        torch.Tensor: Recorded audio as a tensor, or None if no speech detected.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"🎤 Recording started (max {max_duration} seconds)...")

    frames = []
    has_speech = False
    last_speech_time = None
    start_time = time.time()
    
    try:
        while time.time() - start_time < max_duration:
            # Read audio chunk - EXACTLY 512 samples for Silero VAD
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                # Convert to tensor for VAD - must be exactly 512 samples for 16kHz
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                audio_tensor = torch.from_numpy(audio_chunk).float() / 32768.0
                
                # Run VAD on the audio chunk (single frame of exactly 512 samples)
                speech_prob = model(audio_tensor, RATE).item()
                
                # Check if we found speech
                if speech_prob > SPEECH_THRESHOLD:
                    has_speech = True
                    last_speech_time = time.time()
                    print("🔊", end="", flush=True)  # Visual indicator of speech
                else:
                    print(".", end="", flush=True)  # Visual indicator of silence
                
                # Check if we should stop recording due to silence
                current_time = time.time()
                if has_speech and last_speech_time and (current_time - last_speech_time > MAX_SILENCE_DURATION):
                    print("\n⏹️ Stopped recording: End of speech detected (silence)")
                    break
                    
            except IOError as e:
                print(f"\n⚠️ Audio input overflow: {e}")
                continue
            except Exception as e:
                print(f"\n⚠️ Recording error: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\n⏹️ Stopped recording: User interrupted")
    except Exception as e:
        print(f"\n❌ Recording error: {e}")
        return None
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("\nRecording stopped")

    # Convert frames to a single audio tensor
    if not frames or not has_speech:
        print("❌ No speech detected in recording")
        return None

    try:
        # Combine all recorded audio chunks
        audio_data = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])
        audio_tensor = torch.from_numpy(audio_data).float() / 32768.0
        
        # Check if the recording is too short
        if len(audio_data) < RATE * 0.5:  # Less than 500ms
            print("❌ Recording too short")
            return None
            
        return audio_tensor
        
    except Exception as e:
        print(f"❌ Audio processing error: {e}")
        return None

def listen(max_recording_time=30):
    """
    Listen and transcribe user speech with natural pause handling.
    
    Args:
        max_recording_time (int): Maximum recording duration in seconds. Defaults to 30.
    
    Returns:
        str: Transcribed text or error message
    """
    print(f"🎙️ Stella is listening... (max {max_recording_time} seconds)")

    try:
        # Record audio
        audio = record_audio(max_duration=max_recording_time)

        if audio is None or audio.numel() == 0:
            return "I couldn't hear any speech. Could you speak a bit louder or clearer?"

        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            torchaudio.save(f.name, audio.unsqueeze(0), RATE)
            temp_path = f.name

        # Transcribe the audio using Whisper
        print("🔍 Processing your speech...")
        result = whisper_model.transcribe(temp_path)
        transcription = result['text'].strip()

        if not transcription:
            return "I heard something, but I couldn't understand what you said. Could you repeat?"

        print(f"✨ Transcribed: {transcription}")
        return transcription

    except Exception as e:
        print(f"🚨 Error during listening: {e}")
        return "Sorry, there was an issue processing your speech."