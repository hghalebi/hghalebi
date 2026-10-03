"""Generate a self-contained SVG illustration; no runtime scripts or external assets."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
DURATION = 18
stages = [
    ('01', 'CONTRACT', 'Typed inputs', 'Rust / Axum'),
    ('02', 'CHECKPOINT', 'Durable jobs', 'PostgreSQL'),
    ('03', 'EXECUTE', 'Scoped tools', 'Rig / Mastra'),
    ('04', 'VERIFY', 'Rules + evaluation', 'Human oversight'),
    ('05', 'OPERATE', 'Trace + recover', 'OTel / CI/CD'),
]
logs = [
    (0, 2.4, 'CONTRACT', '#79c0ff', 'input      parse into validated domain types', 'boundary   malformed data never reaches a tool'),
    (2.4, 4.8, 'CHECKPOINT', '#79c0ff', 'state      persist the job before execution', 'storage    durable progress outside the model'),
    (4.8, 7.2, 'EXECUTE', '#79c0ff', 'policy     authorize a narrowly scoped tool call', 'control    human approval for sensitive actions'),
    (7.2, 9.3, 'TOOL TIMEOUT', '#ffb454', 'failure    upstream tool times out', 'decision   retry only a classified, retryable failure'),
    (9.3, 12.1, 'RECOVER', '#ffb454', 'resume     load the saved execution checkpoint', 'safety     bounded retry + the same idempotency key'),
    (12.1, 14.8, 'VERIFY', '#7ee787', 'validate   check output contracts and domain rules', 'release    evaluation evidence before promotion'),
    (14.8, 18, 'OPERATE', '#7ee787', 'observe    correlate model calls, tools and outcomes', 'handover   traces, runbooks and a recovery path'),
]

def animate_visible(start, end):
    # Discrete holds prevent blinking and make each state readable.
    if start == 0:
        times = f'0;{end/DURATION:.6f};1'
        vals = '1;0;0'
    elif end == DURATION:
        times = f'0;{start/DURATION:.6f};1'
        vals = '0;1;1'
    else:
        times = f'0;{start/DURATION:.6f};{end/DURATION:.6f};1'
        vals = '0;1;0;0'
    return f'<animate attributeName="opacity" values="{vals}" keyTimes="{times}" calcMode="discrete" dur="{DURATION}s" repeatCount="indefinite"/>'

parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="440" viewBox="0 0 960 440" role="img" aria-labelledby="title desc">
<title id="title">Hamze Ghalebi — engineering reliable AI workflows</title>
<desc id="desc">An illustrative workflow: validate typed inputs, persist a Postgres checkpoint, authorize scoped agent tools, recover from a tool timeout with bounded retries and idempotency keys, verify outcomes, and correlate traces. This is an architecture illustration, not live telemetry or a benchmark.</desc>
<style>
text{white-space:pre;font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
.head{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
@media(prefers-reduced-motion:reduce){.motion{display:none}}
</style>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1b2633" stroke-width=".65"/></pattern>
  <linearGradient id="surface" x2="1" y2="1"><stop stop-color="#111923"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
  <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#8b6840" stroke-width="1.2"/></marker>
</defs>
<rect x="1" y="1" width="958" height="438" rx="16" fill="url(#surface)" stroke="#303b48"/>
<rect x="2" y="2" width="956" height="296" rx="15" fill="url(#grid)" opacity=".55"/>
<path d="M28 24v16" stroke="#ff7b43" stroke-width="3"/>
<text x="41" y="37" fill="#a3adba" font-size="12" letter-spacing="1.2">HAMZE GHALEBI / FORWARD-DEPLOYED AI</text>
<rect x="774" y="21" width="159" height="24" rx="12" fill="#19212c" stroke="#364150"/>
<text x="853.5" y="37" text-anchor="middle" fill="#a3adba" font-size="10.5" letter-spacing=".6">ARCHITECTURE DEMO</text>
<text class="head" x="28" y="79" fill="#f0f6fc" font-size="29" font-weight="700" letter-spacing="-.7">Ship the workflow. Own the failure modes.</text>
<text x="29" y="105" fill="#9da9b8" font-size="13">Contracts. Durable state. Controlled tools. Evidence.</text>
<path d="M108 134H852" fill="none" stroke="#334252" stroke-width="2"/>
''']

active_windows = [[(0,2.4)],[(2.4,4.8),(9.3,10.7)],[(4.8,7.2),(10.7,12.1)],[(12.1,14.8)],[(14.8,18)]]
for i, (num,label,detail,tech) in enumerate(stages):
    x=24+i*186; cx=x+84
    parts.append(f'''<path d="M{cx} 134V150" stroke="#334252" stroke-width="2"/>
<circle cx="{cx}" cy="134" r="4" fill="#53677e"/>
<rect x="{x}" y="150" width="168" height="91" rx="9" fill="#101823" stroke="#334252"/>
''')
    for a,b in active_windows[i]:
        color='#7ee787' if i>=3 else '#79c0ff'
        parts.append(f'<g class="motion" opacity="0">{animate_visible(a,b)}<rect x="{x}" y="150" width="168" height="91" rx="9" fill="#142536" stroke="{color}"/><circle cx="{cx}" cy="134" r="5" fill="{color}"/></g>')
    if i==2:
        parts.append(f'<g class="motion" opacity="0">{animate_visible(7.2,9.3)}<rect x="{x}" y="150" width="168" height="91" rx="9" fill="#2b2016" stroke="#ffb454"/><circle cx="{cx}" cy="134" r="5" fill="#ffb454"/></g>')
    parts.append(f'''<text x="{x+13}" y="172" fill="#ff9b73" font-size="10">{num}</text>
<text x="{x+13}" y="193" fill="#e6edf3" font-size="14" font-weight="700">{label}</text>
<text x="{x+13}" y="212" fill="#abb9c9" font-size="11.5">{detail}</text>
<text x="{x+13}" y="229" fill="#829bb6" font-size="10.5">{tech}</text>''')

parts.append('''<path d="M480 241V263H294V243" fill="none" stroke="#8b6840" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow)"/>
<text x="29" y="282" fill="#8e9cac" font-size="11">FAILURE IS A STATE, NOT A SURPRISE.</text>
<text x="934" y="282" text-anchor="end" fill="#c8a278" font-size="11">checkpoint + bounded retry + idempotency</text>
<g class="motion"><circle cy="134" r="4" fill="#79c0ff"><animate attributeName="cx" values="108;108;294;294;480;480;666;666;852;852" keyTimes="0;.10;.133;.24;.267;.67;.71;.80;.85;1" dur="18s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" keyTimes="0;.4;.672222" calcMode="discrete" dur="18s" repeatCount="indefinite"/><animate attributeName="fill" values="#79c0ff;#7ee787" keyTimes="0;.672222" calcMode="discrete" dur="18s" repeatCount="indefinite"/></circle></g>
<g class="motion" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.516667;.594444;1" calcMode="discrete" dur="18s" repeatCount="indefinite"/><circle r="4" fill="#ffb454"><animateMotion path="M480 241V263H294V243" keyPoints="0;0;1;1" keyTimes="0;.516667;.594444;1" calcMode="linear" dur="18s" repeatCount="indefinite"/></circle></g>
<rect x="24" y="299" width="912" height="96" rx="9" fill="#090e15" stroke="#2c3745"/>
<path d="M24 327H936" stroke="#263241"/>
<circle cx="40" cy="313" r="3" fill="#ff9b73"/>
<circle cx="51" cy="313" r="3" fill="#7b8da3"/>
<circle cx="62" cy="313" r="3" fill="#7b8da3"/>
<text x="81" y="317" fill="#8395ab" font-size="11">remolab / illustrative workflow.trace</text>
<text x="39" y="352" fill="#79c0ff" font-size="12.5">input      parse into validated domain types</text>
<text x="39" y="378" fill="#9baabd" font-size="12.5">boundary   malformed data never reaches a tool</text>
''')
for a,b,status,color,line1,line2 in logs:
    parts.append(f'''<g class="motion" opacity="0">{animate_visible(a,b)}
<rect x="700" y="303" width="222" height="20" fill="#090e15"/>
<circle cx="{916-len(status)*7-12}" cy="313" r="3" fill="{color}"/>
<text x="918" y="317" text-anchor="end" fill="{color}" font-size="11">{escape(status)}</text>
<rect x="34" y="332" width="892" height="56" fill="#090e15"/>
<text x="39" y="352" fill="{color}" font-size="12.5">{escape(line1)}</text>
<text x="39" y="378" fill="#abb9c9" font-size="12.5">{escape(line2)}</text>
</g>''')
parts.append('''<text x="29" y="421" fill="#a3b3c7" font-size="11.5">RUST + TYPESCRIPT</text>
<text x="233" y="421" fill="#647892" font-size="11.5">/</text>
<text x="260" y="421" fill="#a3b3c7" font-size="11.5">RIG + MASTRA</text>
<text x="425" y="421" fill="#647892" font-size="11.5">/</text>
<text x="452" y="421" fill="#a3b3c7" font-size="11.5">POSTGRES</text>
<text x="574" y="421" fill="#647892" font-size="11.5">/</text>
<text x="601" y="421" fill="#a3b3c7" font-size="11.5">OPENTELEMETRY</text>
<text x="767" y="421" fill="#647892" font-size="11.5">/</text>
<text x="794" y="421" fill="#a3b3c7" font-size="11.5">NIXOS + CI/CD</text>
</svg>
''')
svg='\n'.join(parts)
(ROOT/'assets'/'production-ai.svg').write_text(svg)
# The static version is an explicit fallback and reduced-motion reference.
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
root=ET.fromstring(svg)
for parent in list(root.iter()):
    for child in list(parent):
        if 'motion' in child.attrib.get('class','').split():
            parent.remove(child)
static=ET.tostring(root,encoding='unicode')
(ROOT/'assets'/'production-ai-static.svg').write_text(static)
(ROOT/'preview.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Hamze — profile animation preview</title><style>body{margin:0;background:#0d1117;padding:24px;font-family:system-ui;color:#c9d1d9}main{max-width:960px;margin:auto}img{display:block;width:100%;height:auto}a{color:#79c0ff}p{font-size:14px;line-height:1.6}</style><main><picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/production-ai-static.svg"><img src="assets/production-ai.svg" alt="Animated production AI architecture illustration"></picture><p>This animation is an architecture illustration, not a live system or benchmark. <a href="assets/production-ai-static.svg">Static version</a></p></main></html>''')
print('SVG bytes', len(svg.encode()))
