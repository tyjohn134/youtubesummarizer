from yt import YTDownloader, get_video_id
from summarize import generate_summary
from celery import Celery
from nltk.tokenize import sent_tokenize
from celery.utils.log import get_task_logger  # Initialize celery
from textblob import TextBlob
import whisper
import os
# Create logger - enable to display messages on task logger

celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//',
                backend="redis://localhost:6379/0")
celery_log = get_task_logger(__name__)
# Create Order - Run Asynchronously with celery
# Example process of long running task


def post_process_text(text):
    sentences = []
    sents = TextBlob(text.strip()).sentences
    for sent in sents:
        sentences.append(str(sent).capitalize())
    return ' '.join(sentences)


@celery.task(bind=True)
def create_summarization(self, url):
    summary = None
    celery_log.info(f"Downloading Youtube video...")
    yt = YTDownloader(url)
    # Download youtube video
    output_path = yt.download_url(url)
    celery_log.info(f"Finished downloading Youtube video...")
    self.update_state(state="FINISHED_YOUTUBE_DOWNLOAD")
    if output_path != None:
        # Load model
        model = whisper.load_model("base", device="cuda", in_memory=True)
        celery_log.info(f"Finished loading whisper model...")
        self.update_state(state="FINISHED_LOADING_WHISPER")
        # Transcribe the audio using Whisper
        transcription = model.transcribe(output_path)
        celery_log.info(f"Finished transcribing Youtube video...")
        self.update_state(state="FINISHED_TRANSCRIPTION")
        # Remove the audio file
        os.remove(output_path)
        celery_log.info(f"Summarizing Youtube video...")
        self.update_state(state="STARTED_SUMMARIZATION")
        # Use a Hugging Face transformer model to summarize the transcription
        summary = generate_summary(transcription["text"])
        summary = post_process_text(summary)
        # Summarize Youtube Video
        celery_log.info(f"Finished summarizing Youtube video...")
        self.update_state(state="FINISHED_SUMMARIZATION")
        video_id = get_video_id(url) if get_video_id(
            url) != None else "audio"
        with open(f"{video_id}_summary.txt", "w+") as f:
            f.write(summary)
    else:
        print("Couldn't download youtube video")
    celery_log.info(f"Request Complete!")
    return {"summary": summary}
