import sys
import os 
from utils import audio_convert
import whisper
import shutil

model = whisper.load_model("base")
Ori_dir = "Silicon Photonics Design, Fabrication and Data Analysis"
Tar_dir = "CC_in_videos"

#配置字幕输出
word_options = {
"highlight_words": True,
"max_line_count": sys.maxsize, 
"max_line_width": 3,
}

for root, dir, files in os.walk(Ori_dir):
    for file in files:
        try:
            if file.split(".")[1] == "mp4" and file.split(".")[0] + ".srt" not in files:
                file_path = os.path.join(root, file)
                MP4_add_CC = audio_convert(file_path, model)
                MP4_add_CC.Convert_mp4_to_mp3()
                MP4_add_CC.Bulid_srt(word_options)
                MP4_add_CC.add_srt_to_mp4()
                os.makedirs(Tar_dir + f"/{root}", exist_ok=True)
                src_file = MP4_add_CC.file.split(".")[0] + "_CC.mp4"
                shutil.move(src_file, Tar_dir + f"/{src_file}")
        except:
            print(f"Error: {file}",  file=sys.stderr)
