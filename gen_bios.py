import json, re, html

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

def slug(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def esc(s):
    return html.escape(s, quote=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — {entity} | Government of Malta Structure Register</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{{--ink:#1a1f1c;--paper:#f7f5ef;--card:#ffffff;--line:#dcd8c8;--malta-red:#a3172e;--malta-red-deep:#7d1122;--gold:#a1893f;--muted:#6b6a5f;}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:'IBM Plex Sans',sans-serif;line-height:1.6;}}
.wrap{{max-width:720px;margin:0 auto;padding:40px 24px 80px;}}
.back{{display:inline-block;margin-bottom:24px;color:var(--malta-red);text-decoration:none;font-family:'IBM Plex Mono',monospace;font-size:12.5px;border-bottom:1px solid var(--malta-red);padding-bottom:2px;}}
.back:hover{{color:var(--malta-red-deep);border-color:var(--malta-red-deep);}}
.card{{background:var(--card);border:1px solid var(--line);padding:28px 30px;}}
.role-tag{{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--malta-red);border:1px solid var(--malta-red);padding:3px 8px;letter-spacing:.05em;margin-bottom:12px;}}
h1{{font-family:'Fraunces',serif;font-weight:700;font-size:30px;margin:0 0 6px;letter-spacing:-.01em;}}
.entity-line{{color:var(--muted);font-family:'IBM Plex Mono',monospace;font-size:12.5px;margin-bottom:20px;}}
.bio-text{{font-size:15px;line-height:1.7;margin-bottom:20px;}}
.source-block{{border-top:1px solid var(--line);padding-top:16px;font-size:12.5px;}}
.source-label{{font-family:'IBM Plex Mono',monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:6px;}}
.source-block a{{color:var(--gold);word-break:break-all;}}
footer{{text-align:center;color:var(--muted);font-size:11.5px;font-family:'IBM Plex Mono',monospace;margin-top:24px;}}
</style>
</head>
<body>
<div class="wrap">
<a class="back" href="../index.html">← Back to Government of Malta — Structure Register</a>
<div class="card">
<span class="role-tag">{role}</span>
<h1>{name}</h1>
<div class="entity-line">{entity}</div>
<div class="bio-text">{bio}</div>
<div class="source-block">
<div class="source-label">Source</div>
{sources}
</div>
</div>
<footer>Bio last checked {checked}.</footer>
</div>
</body>
</html>
"""

ROLE_LABELS = {
    'chairman':'Chairman','chairperson':'Chairperson','executive_chairman':'Executive Chairman',
    'ceo':'CEO','planning_board_chairman':'Planning Board Chairman','board_secretary':'Board Secretary',
    'deputy_chairman':'Deputy Chairman','deputy_chairperson':'Deputy Chairperson',
}

def role_for_person(chair, person):
    for key, label in ROLE_LABELS.items():
        if chair.get(key) == person:
            return label
    if person in (chair.get('board_members') or []):
        return 'Board Member'
    return 'Named individual'

count = 0
for entity, chair in data['chairs'].items():
    bios = chair.get('bios', {})
    bio_sources = chair.get('bio_sources', {})
    checked = chair.get('checked', 'n/a')
    for person, bio_text in bios.items():
        fname = f"bios/{slug(entity)}-{slug(person)}.html"
        role = role_for_person(chair, person)
        src_url = bio_sources.get(person)
        if src_url:
            sources_html = f'<a href="{esc(src_url)}" target="_blank" rel="noopener">{esc(src_url)}</a>'
        else:
            sources_html = '<span style="color:var(--muted)">No specific source URL recorded.</span>'
        page = TEMPLATE.format(
            name=esc(person), entity=esc(entity), role=esc(role),
            bio=esc(bio_text), sources=sources_html, checked=esc(checked)
        )
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(page)
        count += 1

print('Generated', count, 'bio pages')
