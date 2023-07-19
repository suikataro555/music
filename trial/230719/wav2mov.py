#------------------------------------------------------------
# 音声→動画の変換
#------------------------------------------------------------
from scipy.io import wavfile
from moviepy.editor import ImageClip,AudioFileClip, concatenate_videoclips

# Waveファイルのパス
wave_file = "output.wav"
img_file = "pic/hoge.png"

# Waveファイルの読み込み
sample_rate, audio_data = wavfile.read(wave_file)

# 音声データをオーディオクリップとして作成
audio_clip = AudioFileClip(wave_file)

# 静止画像の作成（真っ黒）
duration = len(audio_data) / sample_rate  # 音声データの長さ（秒）
black_image = ImageClip(img_file, duration=duration)

# 音声と静止画像を結合して動画を作成
video = concatenate_videoclips([black_image.set_audio(audio_clip)])

# フレームレートを指定
video = video.set_fps(1)

# 動画をファイルに保存
output_file = 'output_video.mp4'
video.write_videofile(output_file, codec='libx264', audio_codec='aac')