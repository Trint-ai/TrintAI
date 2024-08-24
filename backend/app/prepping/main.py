"""Audio preprocessing techniques"""

import os
import subprocess
import mutagen

from core.config import settings
from pydub import AudioSegment
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS


class audioPreprocessing:
    """Main audio preprocessing class"""

    def __init__(self, file_name, file_extension, file_id):
        """Initialize for audio preprocessing"""
        self.file_name = file_name
        self.file_extension = file_extension
        self.file_id = file_id
        self.normalize_db = settings.NORMALIZE_DB
        self.audio_length = None
        self.audio_size_mb = None
        self.chunk = None

    def start_preprocessing(self):
        result = self.audio_precheck()
        if result is None:
            return None

        result = self.remove_silence()
        if result is None:
            return None

        result = self.convert_to_wav()
        if result is None:
            return None

        return result, self.file_name, self.audio_length, self.audio_size_mb

    def normalize_chunk(self):
        return self.chunk.apply_gain(settings.NORMALIZE_DB - self.chunk.dBFS)

    def get_audio_codec(self):
        """Get and return the audio codec of a given audio file."""
        try:
            audio = mutagen.File(self.file_name)
            codec = type(audio).__name__
            return codec
        except Exception as e:
            print("Error getting audio codec")
            print(e)
            return None

    def audio_precheck(self):
        """TODO"""
        audio_codec = self.get_audio_codec()

        if audio_codec is None:
            return None

        print(f'Audio codec: {audio_codec}')

        if self.file_extension in settings.SUPPORTED_AUDIO_FORMATS:
            if (self.file_extension == "mp4" or self.file_extension == "m4a") and audio_codec == "MP4":
                print(f"converting audio file from {self.file_extension}, codec: {audio_codec}")
                audio = AudioSegment.from_file(self.file_name, "mp4")
                file_name_converted = f"{settings.FILE_NAME_PREFIX}-converted.mp3"
                audio.export(file_name_converted, format="mp3")
                os.remove(self.file_name)  # remove previous file from local disk
                self.file_name = file_name_converted
                audio = AudioSegment.from_file(self.file_name)
            else:
                print(f'audio file extension: {self.file_extension}')
                audio = AudioSegment.from_file(self.file_name)

        else:
            print("Error: audio format not supported")
            return None

        self.audio_length = audio.duration_seconds
        print(f'audio length: {self.audio_length}')

        # Check size of audio file
        file_stats = os.stat(self.file_name)
        self.audio_size_mb = file_stats.st_size / (1024 * 1024)
        print(f'audio size: {self.audio_size_mb}')

        if self.audio_size_mb >= settings.MAX_AUDIO_MB:
            print("Error: audio file bigger than 25MB")
            return None

        if self.audio_length < settings.MIN_AUDIO_LENGTH_SECONDS:
            print("Error: audio too short")
            return None

        return "OK"

    def remove_silence(self):
        """Remove silence fom given audio file"""

        [fs, x] = aIO.read_audio_file(self.file_name)

        try:
            segments = aS.silence_removal(x, fs, settings.AUDIO_REMOVE_SILENCE_ST_WIN,
                                          settings.AUDIO_REMOVE_SILENCE_ST_STEP,
                                          smooth_window=settings.AUDIO_REMOVE_SILENCE_SMOOTH_WINDOW,
                                          weight=settings.AUDIO_REMOVE_SILENCE_WEIGHT,
                                          plot=settings.AUDIO_REMOVE_SILENCE_PLOT)
        except:
            print("Error: during silence removal with pyAudioAnalysis")
            return None

        audio = AudioSegment.from_file(self.file_name)
        merged_audio = AudioSegment.empty()
        ms_of_silence = AudioSegment.silent(duration=10)
        ms_of_silence = ms_of_silence.apply_gain(-20.0 - ms_of_silence.dBFS)

        for s in segments:
            start_audio = s[0] * 1000
            stop_audio = s[1] * 1000
            self.chunk = audio[start_audio:stop_audio]
            combined = self.normalize_chunk()
            merged_audio += combined + ms_of_silence

        os.remove(self.file_name) # remove previous file from local disk
        self.file_name = f"{settings.FILE_NAME_PREFIX}-{self.file_id}-without-silence.mp3"
        merged_audio.export(self.file_name, format="mp3")

        print(f"Silence Removal Complete")
        return "OK"

    def convert_to_wav(self):
        file_name = os.path.splitext(self.file_name)[0][0:]
        file_name = f"{file_name}.wav"
        subprocess.run(["ffmpeg",
                        "-hide_banner",
                        "-loglevel", "error",
                        "-i", self.file_name,
                        "-acodec", "pcm_s16le",
                        "-ar", "16000",
                        file_name])
        os.remove(self.file_name)
        self.file_name = file_name
        return "OK"
