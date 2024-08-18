"""TODO"""
import os
from faster_whisper import WhisperModel
from core.config import settings


class whisper:
    """TODO"""

    def __init__(self, file_name):
        """TODO"""
        self.file_name = file_name
        self.transcript_data = []
        self.detected_language = None
        self.detected_language_prob = None

    def transcript_audio(self):
        """TODO"""
        try:
            model_size = settings.WHISPER_MODEL_SIZE

            # TODO run on GPU

            # run on CPU
            model = WhisperModel(settings.WHISPER_MODEL_SIZE, device="cpu", compute_type="int8", local_files_only=True)
            segments, info = model.transcribe(self.file_name, beam_size=settings.WHISPER_BEAM_SIZE)
            self.detected_language = info.language
            self.detected_language_prob = info.language_probability
            print("Detected language '%s' with probability %f" % (self.detected_language, self.detected_language_prob))

            segments = list(segments)  # The transcription will actually run here.
            print("Transcript:")
            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
                self.transcript_data.append(
                    {
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment.text,
                    }
                )

            return self.transcript_data, self.detected_language, self.detected_language_prob

        except Exception as e:
            print("Error generating transcript")
            print(e)
            return None, None, None
