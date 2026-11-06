from pathlib import Path
import re,base64
from PIL import Image
from io import BytesIO
p=Path(__file__).resolve().parent
s=(p/'playme.html').read_text(encoding='utf-8')
results=[]
for m in re.finditer(r'"(assets/[^"\n]+)":"data:image/png;base64,([A-Za-z0-9+/=]+)"',s):
 k,b64=m.groups();raw=base64.b64decode(b64,validate=True);Image.open(BytesIO(raw)).load();assert raw==(p/k).read_bytes(),k;results.append(k)
assert len(results)==104,len(results)
for n,m in zip(('charlie_rescate.mp3','ritual_of_stone.mp3'),re.finditer(r'data:audio/mpeg;base64,([A-Za-z0-9+/=]+)',s)):
 assert base64.b64decode(m.group(1),validate=True)==(p/'assets/audio'/n).read_bytes(),n
import json
sfxmatch=re.search(r'const SFX_DATA=(\{.+?\});',s)
assert sfxmatch, 'SFX_DATA ausente'
sfx=json.loads(sfxmatch.group(1))
assert len(sfx)==12,len(sfx)
for name,b64 in sfx.items():
 assert base64.b64decode(b64,validate=True)==(p/'assets/audio'/f'{name}.wav').read_bytes(),name
print('Correcto: 104 PNG, 2 MP3 y 12 WAV coinciden exactamente con playme.html')
