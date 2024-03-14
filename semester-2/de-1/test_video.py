import requests
from tqdm import tqdm

video_length = 100000

url = 'https://streaming.cast.switch.ch/hls/p/111/sp/11100/serveFlavor/entryId/0_p5pbzy2c/v/12/flavorId/0_oaw6uwmo/name/a.mp4/seg-%NUM%-v1-a1.ts'
video_content = b''

video_iter = tqdm(range(1, video_length))

for i in video_iter:
    video_iter.set_description('Downloading video')
    url = url.replace("%NUM%", f"{i:d}")
    response = requests.get(url)
    if response.status_code != 200:
        break
    video_content += response.content

with open('test.mp4', 'wb') as f:
    f.write(video_content)
