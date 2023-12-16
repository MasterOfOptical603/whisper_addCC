import whisper
import ffmpeg as ff
from whisper.utils import get_writer
import shutil
import os


class audio_convert():
    def __init__(self, file_path, model) -> None:
        self.file = file_path
        self.model = model
        self.dir = file_path.rsplit("/", 1)[0]
        self.file_name = file_path.rsplit("/", 1)[1]
        self.srt_writer = get_writer("srt", self.dir)

    def Convert_mp4_to_mp3(self):
        if self.file.split(".")[1] == "mp4":
            input_file = self.file
            output_file = self.file.split(".")[0] + ".mp3"
            stream = ff.input(input_file)
            stream = ff.output(stream, output_file)
            ff.run(stream, overwrite_output=True)
        return 0

    def Bulid_srt(self, word_options):
        mp3_file = self.file.split(".")[0] + ".mp3"
        input_file = mp3_file
        output_file = self.file_name.split(".")[0] + ".srt"
        result = whisper.transcribe(self.model, input_file)
        self.srt_writer(result, output_file, word_options)
        return 0

    def add_srt_to_mp4(self):
        mp4_file = self.file
        srt_file = self.file.split(".")[0] + ".srt"
        output_file = self.file.split(".")[0] + "_CC.mp4"
        stream = ff.input(mp4_file)
        #提取出音频，不然添加字幕后没有音频
        audio = stream.audio
        stream = ff.filter(stream, "subtitles", srt_file)
        #将音频添加回去
        stream = ff.concat(stream, audio, v=1, a=1)
        stream = ff.output(stream, output_file)
        ff.run(stream)
        print("####\nDone" + output_file + "\n####")
        return 0

if __name__ == "__main__":
    model = whisper.load_model("base")
    Ori_dir = "Silicon Photonics Design, Fabrication and Data Analysis"
    Tar_dir = "CC_in_videos"

    #配置字幕输出
    word_options = {
    "highlight_words": True,
    "max_line_count": 2000,
    "max_line_width": 3
    }

    for root, dir, files in os.walk(Ori_dir):
        for file in files:
            if file.split(".")[1] == "mp4":
                file_path = os.path.join(root, file)
                MP4_add_CC = audio_convert(file_path, model)
                MP4_add_CC.Convert_mp4_to_mp3()
                MP4_add_CC.Bulid_srt(word_options)
                MP4_add_CC.add_srt_to_mp4()
                shutil.copy(MP4_add_CC.file.split(".")[0] + "_CC.mp4", Tar_dir + "/" + file.split(".")[0].split("/")[-1] + "_CC.mp4")
        
