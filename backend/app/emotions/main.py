"""TODO"""

from core.config import settings
from transformers import pipeline


class emotions:
    """TODO"""

    def __init__(self, transcript_data, detected_language):
        """TODO"""
        self.transcript_data = transcript_data
        self.detected_language = detected_language
        self.emotions = []
        self.classifier = pipeline("text-classification", model=settings.EMOTIONS_MODEL,
                                   top_k=1, max_length=settings.EMOTIONS_EMBEDDINGS_MAX_LENGTH, truncation=True, device_map="auto")

    async def get_emotions(self):
        if self.detected_language == "en":
            print("Emotions:")
            for segment in self.transcript_data:
                emotion = self.classifier(segment['text'])
                emotion = emotion[0][0]
                emotion_label = emotion['label']
                emotion_score = emotion['score']
                print(emotion)

                self.emotions.append(
                    {
                        "emotion": emotion_label,
                        "emotion_score": emotion_score
                    }
                )

        return self.emotions
