from pytube import YouTube
import argparse
import sys

def prog(stream,chunk,bytes_remaining):
    filesize = stream.filesize
    curr = filesize - bytes_remaining
    done = int(50*curr/filesize)
    sys.stdout.write("\r[{}{}]".format(">"*done," "*(50-done)))
    sys.stdout.flush()

class YtDownloader(YouTube):
    def __init__(self,url,output="."):
        self.out = output
        super().__init__(url,on_progress_callback=prog)

    def getMp3(self):
        self.streams.filter(only_audio=True).first().download(filename=f"{self.title}.mp3",output_path=self.out)

    def getOnlyAudio(self):
        self.streams.filter(only_audio=True).first().download(output_path=self.out)

    def getVideo(self):
        self.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc().first().download(output_path=self.out)

    @property
    def ttl(self): # title
        return self.title

parse = argparse.ArgumentParser(prog="python ytdl.py")

parse.add_argument(
    "-u","--url",
    nargs="?",
    help="Url Video Youtube",
    required=True
)
parse.add_argument(
    "-o","--output",
    help="Path To Save File",
    nargs="?"
)
parse.add_argument(
    "-m","--mp3",
    action="store_true",
    help="Format Mp3",
)
parse.add_argument(
    "-v","--video",
    action="store_true",
    help="Format Mp4"
)
parse.add_argument(
    "-a","--audio",
    action="store_true",
    help="Only Audio Format Mp4"
)


args = parse.parse_args()

yt = YtDownloader(args.url,output=args.output)
if args.mp3:
    yt.getMp3()
elif args.video:
    yt.getVideo()
elif args.audio:
    yt.getOnlyAudio()
else:
    print("Usage python file.py -h")

print(f"\nSuccess Download[√]\nTitle >>> {yt.ttl}")

