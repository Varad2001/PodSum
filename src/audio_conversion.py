import os
from typing import Optional
import whisper
from src.logger import logging
import src.config as config
import numba


def get_text_from_audio(audio_path : str) -> Optional[str]:
    """
    Extracts text from an audio file using the Whisper ASR model.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        Optional[str]: The extracted text if successful, otherwise None.

    """

    logging.info(f"\nAttempting to extract text from : {audio_path}")

    try :
        model = whisper.load_model(name='tiny', download_root=config.MODELS_DIR)
        results = model.transcribe(audio_path)

        logging.info("\nExtraction successful.")
        return results['text']
    except Exception as e:
        logging.info("\nExtraction failed.")
        logging.exception(e)
        return None



