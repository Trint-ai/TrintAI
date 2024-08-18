"""TODO"""

from openai import OpenAI
from core.config import settings


class summarization:
    """TODO"""

    def __init__(self, transcript_data):
        """TODO"""
        self.transcript_data = transcript_data
        self.summary = None
        self.openai_client = OpenAI()

    def generate_summary(self):
        """TODO"""
        print("Summary:")
        text = ""
        for segment in self.transcript_data:
            text += segment["text"] + ". "

        response = self.openai_client.chat.completions.create(
            model=settings.SUMMARIZATION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Write a concise summary from the content you are provided (in the original language)"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=settings.SUMMARIZATION_MODEL_TEMP,
            top_p=1
        )

        summary = response.choices[0].message.content
        summary = summary.lstrip()

        self.summary = {'summary': summary}
        print(summary)
        return self.summary
