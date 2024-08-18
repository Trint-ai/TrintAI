"""TrintAi core application """

from utils.main import utils
from prepping.main import audioPreprocessing
from whisper.main import whisper
from emotions.main import emotions
from summarization.main import summarization


class core:
    """Main core class"""

    def __init__(self, file):
        """Initialize for core application"""
        self.file = file

    def start(self):
        """Start the application"""
        print("Starting TrintAI")

        # Download file
        util = utils(self.file)
        file_name, file_extension, file_id = util.download_file()

        # Audio preprocessing
        audio = audioPreprocessing(file_name, file_extension, file_id)
        result, file_name, audio_length, audio_size_mb = audio.start_preprocessing()

        if result is None:
            print("Error while preprocessing audio")
            return None

        # Speech to text
        transcript = whisper(file_name)
        transcript_data, detected_language, detected_language_prob = transcript.transcript_audio()

        if transcript_data is None:
            print("Error while transcript audio")
            return None

        # Detect emotions
        emotion = emotions(transcript_data, detected_language)
        emotions_data = emotion.get_emotions()

        # Generate summary
        summary = summarization(transcript_data)
        summary_data = summary.generate_summary()

        # Compile data to return
        final_result = util.compile_data(summary, summary_data, emotions_data, transcript_data)
        return final_result
