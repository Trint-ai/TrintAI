"""TODO"""

import os
import subprocess
import json
from core.config import settings


class whisper:
    """TODO"""

    def __init__(self, file_name):
        """TODO"""
        self.file_name = file_name
        self.transcript_data = []
        self.detected_language = None

    def transcript_audio(self):
        """TODO"""
        try:
            command = f"/tmp/{settings.WHISPER_MODEL}.llamafile -f {self.file_name} -di -oj -l auto"
            subprocess.run(command, shell=True, capture_output=True)

            # Check if transcription was generated
            print(f"{self.file_name}.json")
            if os.path.exists(f"{self.file_name}.json"):
                print("transcription file was generated")
                with open(f"{self.file_name}.json", 'r') as file:
                    data = json.load(file)

                    self.detected_language = data['result']['language']
                    transcription = data['transcription']

                    # Remove odd prefixes from string
                    for i in range(len(transcription)):
                        data = transcription[i]
                        print(f"[{data['timestamps']['from']}] --> [{data['timestamps']['to']}]  (speaker {data['speaker']}) {data['text']}")
                        self.transcript_data.append(data)

            else:
                print("Error generating transcript")
                return None, None

            return self.transcript_data, self.detected_language

        except Exception as e:
            print("Error generating transcript")
            print(e)
            return None, None
