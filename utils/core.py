import pandas as pd
from .config import TIMBRE_DIR
import torch
import librosa
import numpy as np
import time
import datetime
import webbrowser


class Utils:
    # 保存音色特征
    @staticmethod
    def save_timbre(config, name, type="csv"):
        try:
            df = pd.DataFrame(config)
            if type == "csv":
                csv_file = f"{TIMBRE_DIR}/{name}.csv"
                df.to_csv(csv_file, index=False, header=False, float_format="%.16f")
                print(f"音色特征已保存到 {csv_file}")
                return csv_file
            elif type == "pt":
                # 将DataFrame转换为NumPy数组
                numpy_array = df.values
                tensor = torch.tensor(numpy_array)
                pt_file = f"{TIMBRE_DIR}/{name}.pt"
                torch.save(tensor, pt_file)
                print(f"音色特征已保存到 {pt_file}")
                return pt_file
            else:
                print("请输入正确的类型")
                return None

        except Exception as e:
            print(e)

    # 根据音频生成音色特征
    @staticmethod
    def generate_timbre(audio_path, type="csv"):
        try:
            # 加载音频文件
            y, sr = librosa.load(audio_path, sr=None)
            # 提取音色特征
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)  # Chroma STFT 特征
            spectral_centroid = librosa.feature.spectral_centroid(
                y=y, sr=sr
            )  # 频谱质心
            spectral_bandwidth = librosa.feature.spectral_bandwidth(
                y=y, sr=sr
            )  # 频谱带宽
            spectral_contrast = librosa.feature.spectral_contrast(
                y=y, sr=sr
            )  # 频谱对比度
            spectral_rolloff = librosa.feature.spectral_rolloff(
                y=y, sr=sr
            )  # 频谱滚降点
            # 提取 MFCC（梅尔频率倒谱系数）
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            # 计算每个特征的统计值（均值和标准差）
            features = {
                "chroma_stft_mean": np.mean(chroma_stft),
                "chroma_stft_std": np.std(chroma_stft),
                "spectral_centroid_mean": np.mean(spectral_centroid),
                "spectral_centroid_std": np.std(spectral_centroid),
                "spectral_bandwidth_mean": np.mean(spectral_bandwidth),
                "spectral_bandwidth_std": np.std(spectral_bandwidth),
                "spectral_contrast_mean": np.mean(spectral_contrast),
                "spectral_contrast_std": np.std(spectral_contrast),
                "spectral_rolloff_mean": np.mean(spectral_rolloff),
                "spectral_rolloff_std": np.std(spectral_rolloff),
            }
            # 添加 MFCC 特征
            for i in range(1, 14):
                features[f"mfcc{i}_mean"] = np.mean(mfcc[i - 1])
                features[f"mfcc{i}_std"] = np.std(mfcc[i - 1])
            # 创建 DataFrame
            config = [features]
            filename = datetime.datetime.now().strftime("%Y%m%d%H%M")
            return Utils.save_timbre(config, filename, type)
        except Exception as e:
            print(e)

    # 打开浏览器
    @staticmethod
    def openweb(url):
        time.sleep(3)
        webbrowser.open(url)
