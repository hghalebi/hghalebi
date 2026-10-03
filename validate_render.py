from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import io, json, hashlib, base64
ROOT=Path(__file__).resolve().parent
results={}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':960,'height':440},device_scale_factor=1)
    svg=(ROOT/'assets/production-ai.svg').read_text()
    page.set_content('<html><head><style>html,body{margin:0}</style></head><body>'+svg+'</body></html>')
    page.evaluate("document.querySelector('svg').pauseAnimations()")
    for t in [0,5.5,8,10,13,16]:
        page.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',t)
        page.screenshot(path=str(ROOT/f'frame-{t}.png'))
    frames=[]
    for k in range(72):
        page.evaluate('(t)=>document.querySelector("svg").setCurrentTime(t)',k/4)
        b=page.screenshot()
        frames.append(Image.open(io.BytesIO(b)).convert('RGB'))
    # One global palette avoids flashing colors between frames.
    swatches=Image.new('RGB',(960,440*6))
    for i,k in enumerate([0,22,32,40,52,64]): swatches.paste(frames[k],(0,440*i))
    palette=swatches.quantize(colors=64)
    quantized=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    quantized[0].save(ROOT/'assets/production-ai.gif',save_all=True,append_images=quantized[1:],duration=250,loop=0,optimize=True,disposal=1)
    results['gif']={'frames':len(quantized),'duration_seconds':18,'bytes':(ROOT/'assets/production-ai.gif').stat().st_size}
    # Verify the image actually animates through a plain <img>, not just an inline SVG.
    page.set_viewport_size({'width':1008,'height':545})
    preview=(ROOT/'preview.html').read_text().replace('assets/production-ai.svg','data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()).replace('assets/production-ai-static.svg','data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/production-ai-static.svg').read_bytes()).decode())
    page.set_content(preview)
    a=page.locator('img').screenshot()
    page.wait_for_timeout(3200)
    b=page.locator('img').screenshot()
    results['html_img_animated']=hashlib.sha256(a).digest()!=hashlib.sha256(b).digest()
    page.screenshot(path=str(ROOT/'preview-desktop.png'))
    page.set_viewport_size({'width':390,'height':270})
    page.set_content(preview)
    page.screenshot(path=str(ROOT/'preview-mobile.png'))
    results['mobile_no_horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.emulate_media(reduced_motion='reduce')
    page.set_content(preview)
    a=page.locator('img').screenshot()
    page.wait_for_timeout(3200)
    b=page.locator('img').screenshot()
    results['reduced_motion_static']=hashlib.sha256(a).digest()==hashlib.sha256(b).digest()
    browser.close()
(ROOT/'validation.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
