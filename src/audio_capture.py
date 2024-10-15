import pyaudio
import numpy as np
import wave


class AudioCapture:

    def __init__(self, sample_rate = 16000, chunk_size = 1024):
        """Initialize the class"""
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.pyaudio_instance = pyaudio.PyAudio()
        self.available_mics = self._detect_mics()
        self.streams = self._initialize_streams()
        self.active_mics = [0] if self.available_mics else []
        self.frames = []

    def _detect_mics(self):
        """Detect available microphones"""
        available_mics = []
        num_devices = self.pyaudio_instance.get_device_count()
        for i in range(num_devices):
            device_info = self.pyaudio_instance.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                available_mics.append((i, device_info['name']))
        return available_mics

    def _is_sample_rate_supported(self, mic_index, sample_rate):
        """Check if the microphone supports the specified sample rate"""
        try:
            device_info = self.pyaudio_instance.get_device_info_by_index(mic_index)
            supported_rate = self.pyaudio_instance.is_format_supported(
                sample_rate,
                input_device=device_info['index'],
                input_channels=1,
                input_format=pyaudio.paInt16
            )
            return supported_rate
        except ValueError:
            return False

    def _initialize_streams(self):
        """Initialize audio streams for all available microphones"""
        streams = {}
        for mic_index, mic_name in self.available_mics:
            if not self._is_sample_rate_supported(mic_index, self.sample_rate):
                print(f"Microphone '{mic_name}' (Index {mic_index}) does not support {self.sample_rate} Hz. Skipping.")
                continue
            try:
                stream = self.pyaudio_instance.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=mic_index,
                    frames_per_buffer=self.chunk_size
                )
                streams[mic_index] = stream
                print(f"Microphone '{mic_name}' initialized successfully (Index {mic_index}).")
            except IOError as e:
                print(f"Error initializing microphone '{mic_name}' (Index {mic_index}): {e}")
                raise
        return streams

    def set_active_mics(self, mic_indices):
        """Set active microphones by their indices"""
        self.active_mics = mic_indices
        active_names = [self.available_mics[i][1] for i in mic_indices]
        print(f"Active microphones set to: {active_names}")

    def capture(self, record_duration=5):
        """Capture audio from the active microphones for a specified duration"""
        active_streams = [self.streams[mic] for mic in self.active_mics]
        self.frames = []
        num_chunks = int(self.sample_rate / self.chunk_size * record_duration)
        print(f"Recording audio for {record_duration} seconds...")
        for _ in range(num_chunks):
            if len(self.active_mics) == 1:
                audio_data = active_streams[0].read(self.chunk_size)
                self.frames.append(audio_data)
            else:
                multi_channel_data = []
                for stream in active_streams:
                    audio_data = stream.read(self.chunk_size)
                    multi_channel_data.append(audio_data)
                self.frames.append(b''.join(multi_channel_data))
        print("Recording finished.")

    def save_to_wav(self, filename="output.wav"):
        """Save the recorded audio frames to a .wav file"""
        if not self.frames:
            print("No audio captured.")
            return
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        print(f"Audio saved to {filename}")

    def close(self):
        """Close all streams and terminate PyAudio"""
        for stream in self.streams.values():
            stream.stop_stream()
            stream.close()
        self.pyaudio_instance.terminate()
        print("All audio streams are closed.")