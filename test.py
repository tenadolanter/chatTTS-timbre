from utils import Utils
from utils.config import ROOT_DIR

audio_path = f"{ROOT_DIR}/static/assets/your_audio_file.wav"

Utils.generate_timbre(audio_path, "csv")
