"""TrintAi core application """

import asyncio
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

    async def start(self):
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
        transcript_data, detected_language = transcript.transcript_audio()

        # Detect emotions
        emotion = emotions(transcript_data, detected_language)

        # Generate summary
        summary = summarization(transcript_data)

        if transcript_data is None:
            print("Error while transcript audio")
            return None

        emotions_data, summary_data = await asyncio.gather(
            asyncio.create_task(emotion.get_emotions()),
            asyncio.create_task(summary.generate_summary()),
        )

        # Compile data to return
        final_result = util.compile_data(summary, summary_data, emotions_data, transcript_data)
        return final_result
