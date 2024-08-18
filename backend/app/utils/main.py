"""TODO"""

import os
import random
import urllib.request

from core.config import settings


def generate_file_id():
    """Generate file id"""

    file_id = random.getrandbits(settings.FILE_ID_BITS)
    return file_id


class utils:
    """Utils class"""

    def __init__(self, file):
        """TODO"""
        self.file = file
        self.file_extension = ""
        self.file_name = ""
        self.file_id = None
        self.final_result = {
            'summary': "",
            'transcript': []
        }

    def generate_file_name(self):
        """Generate file name"""

        self.file_id = generate_file_id()
        print(f"Id: {self.file_id}")
        self.file_extension = os.path.splitext(self.file)[1][1:]
        self.file_extension = self.file_extension.lower()
        self.file_name = f"{settings.FILE_NAME_PREFIX}-{self.file_id}.{self.file_extension}"

    def download_file(self):
        """Download file from URL"""

        self.generate_file_name()

        try:
            print(f"Downloading {self.file}")
            urllib.request.urlretrieve(self.file, self.file_name)
            print("File downloaded!")
        except Exception as e:
            print(e)
            print("Can't download audio file from provided location")
            return None
        return self.file_name, self.file_extension, self.file_id

    def compile_data(self, summary, summary_data, emotions_data, transcript_data):
        if summary is not None:
            self.final_result['summary'] = summary_data

        if len(emotions_data) > 0:
            size_transcript = len(transcript_data)
            for i in range(size_transcript):
                data = {**transcript_data[i], **emotions_data[i]}
                self.final_result['transcript'].append(data)
        else:
            self.final_result['transcript'] = transcript_data

        return self.final_result
