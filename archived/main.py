
from yt import YTDownloader
from summarize import generate_summary
import whisper
import torch
import os
import re


def main():

    url = "https://www.youtube.com/watch?v=iNZk-N6uDcg"
    print("YTDownload processing...")
    yt = YTDownloader(url)
    # Download youtube video
    output_path = yt.download_url(url)

    if output_path != None:
        # Load model
        model = whisper.load_model("base", device="cuda", in_memory=True)

        # Transcribe the audio using Whisper
        transcription = model.transcribe(output_path)

        # Remove the audio file
        os.remove(output_path)

        # Use a Hugging Face transformer model to summarize the transcription
        print(generate_summary(transcription["text"]))
    else:
        print("Couldn't download youtube video")


# Call the main function when the program runs
if __name__ == '__main__':
    main()
