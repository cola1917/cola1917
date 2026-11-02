"""Original profile artwork, guided by frontend-design. All methods are schematics."""
from html import escape
from textwrap import wrap

ACTIVE_DESIGN = 'research'
DESIGNS = {
    'research': {
        'light': dict(bg='#ffffff', ink='#20212b', muted='#626574', accent='#6846bd', line='#dadce5', wash='#f6f3fc'),
        'dark': dict(bg='#0d1117', ink='#eef0f7', muted='#a8adbd', accent='#bea4ff', line='#303642', wash='#1d1929'),
    },
    'studio': {
        'light': dict(bg='#ffffff', ink='#24242a', muted='#66656d', accent='#a84539', line='#e2dbd8', wash='#fff4f1'),
        'dark': dict(bg='#0d1117', ink='#f5efed', muted='#b8aba7', accent='#efb0a4', line='#413332', wash='#251b1b'),
    },
    'upstream': {
        'light': dict(bg='#ffffff', ink='#1d2926', muted='#5c6d66', accent='#2a6b57', line='#d8e3dd', wash='#f2f7f4'),
        'dark': dict(bg='#0d1117', ink='#edf4f0', muted='#a5b7ad', accent='#91cfb1', line='#2b3c33', wash='#16231c'),
    },
}
PALETTES = DESIGNS[ACTIVE_DESIGN]
CARDS = {
    'Newton': ('newton', ['IK, autodiff and cloth assembly', 'Articulation trees and solver correctness'], None),
    'MuJoCo Warp': ('mujoco-warp', ['Signed contact-sensor reductions', 'Correctness with GPU performance preserved'], None),
    'PyPose': ('pypose', ['Lie-group input broadcasting', 'Expanded views and GPU memory efficiency'], None),
    'COLMAP': ('colmap', ['Bundle-adjustment solver controls', 'C++ / CLI / Python and CUDA diagnostics'], None),
}
PROJECTS = {
    'retargeting': [('Reconstruct', 'DaID egocentric reconstruction', 'hand'),
                    ('Retarget', 'Hand and object motion', 'robot'),
                    ('Search & control', 'MPPI search + PPO feedback', 'paths')],
    'reconstruction': [('Observe', 'RGB-D geometry and depth', 'depth'),
                       ('Reconstruct', '3DGS and mesh geometry', 'mesh'),
                       ('Prepare assets', 'Collision proxies + PBR materials', 'asset')],
    'sim2real': [('Plan', 'SIMPLE / CuRobo planning', 'paths'),
                 ('Collect', 'G1 + O6/O7 physical demonstrations', 'dataset'),
                 ('Learn & evaluate', 'GR00T + closed-loop Sim2Real', 'loop')],
}


def text(x, y, value, size, fill, weight=400, anchor=None, extra=''):
    align = f' text-anchor="{anchor}"' if anchor else ''
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}"{align}{extra}>{escape(str(value))}</text>')


def svg(w, h, title, description, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc">\n<title id="title">{escape(title)}</title>\n'
            f'<desc id="desc">{escape(description)}</desc>\n'
            '<g font-family="Segoe UI, Arial, sans-serif">\n' + '\n'.join(body) + '\n</g>\n</svg>\n')


def line(d, p, width=2, faint=False):
    return f'<path d="{d}" fill="none" stroke="{p["line"] if faint else p["accent"]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def drawing(kind, x, y, p, scale=1):
    parts = []
    if kind == 'hand':
        parts += [line('M25 113l-16-27q-5-10 4-8l18 15V40q0-12 9-9v48-59q5-11 11 0v57-47q7-10 11 2v49-34q7-9 11 2v41q0 30-30 35z', p),
                  line('M111 58l27-16 28 16-28 17zM111 58v36l27 17 28-17V58M138 75v36', p, faint=True)]
        for cx, cy in [(31, 79), (40, 40), (51, 22), (62, 35), (73, 51), (43, 111)]:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{p["accent"]}"/>')
    elif kind == 'robot':
        parts += [line('M12 122h46M35 122V96l43-48 40 25 28-43M138 25l18 11m-10-7 20-13 10 9', p, 3),
                  line('M120 100l23-13 24 13-24 13zM120 100v28l23 12 24-12v-28M143 113v27', p, faint=True)]
        for cx, cy in [(35, 96), (78, 48), (118, 73)]:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/>')
    elif kind == 'paths':
        for i in range(7):
            parts.append(line(f'M12 120 C{25+i*13} {16+i*12}, {90+i*7} {10+i*12}, 171 29', p, 1.2, faint=i != 3))
        parts += [f'<circle cx="12" cy="120" r="4" fill="{p["accent"]}"/>',
                  f'<circle cx="171" cy="29" r="8" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/>']
    elif kind == 'depth':
        parts.append(line('M15 23h134v99H15zM15 49h134M15 74h134M15 98h134M49 23v99M82 23v99M116 23v99', p, 1, True))
        parts.append(line('M25 105l24-21 26 7 35-40 27 7', p, 3))
        parts.append(line('M156 39v65m-5-60 5-5 5 5m-10 55 5 5 5-5', p, 1.5))
    elif kind == 'mesh':
        nodes = [(17, 92), (44, 30), (98, 17), (159, 56), (144, 118), (77, 140), (88, 75)]
        for a, b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(1,6),(2,6),(3,6),(4,6),(5,6)]:
            parts.append(line(f'M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}', p, 1.4))
        for cx, cy in nodes:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{p["accent"]}"/>')
    elif kind == 'asset':
        parts.append(line('M18 37l53-26 55 26-55 28zM18 37v79l53 27 55-27V37M71 65v78', p, 1.2, True))
        parts.append(f'<rect x="48" y="49" width="46" height="63" rx="7" fill="{p["wash"]}" stroke="{p["accent"]}" stroke-width="2"/>')
        parts.append(f'<ellipse cx="71" cy="49" rx="23" ry="7" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/>')
        parts.append(line('M141 37h35M158 20v34', p, 1, True))
        for cy in [75, 105, 135]:
            parts.append(f'<circle cx="159" cy="{cy}" r="9" fill="{p["wash"]}" stroke="{p["accent"]}" stroke-width="1.2"/>')
    elif kind == 'dataset':
        for dx, dy in [(28, 12), (14, 23), (0, 34)]:
            parts.append(f'<rect x="{22+dx}" y="{dy}" width="113" height="88" rx="3" fill="{p["bg"]}" stroke="{p["line"]}"/>')
        for row in range(4):
            parts.append(line(f'M36 {53+row*15}h65m9 0h10', p, 1.4, row != 1))
        parts.append(line('M56 134h85', p, 2))
    elif kind == 'loop':
        parts += [line('M39 30a62 62 0 0 1 112 47m0-12v14h-15M131 121A62 62 0 0 1 22 82m0 13V81h14', p, 1.6),
                  line('M65 55l23-15 24 15v40l-24 15-23-15zM65 55l47 40M112 55L65 95M88 40v70', p, 1.5)]
    return f'<g transform="translate({x} {y}) scale({scale})">' + ''.join(parts) + '</g>'


def banner(theme, mobile=False, design=ACTIVE_DESIGN):
    p = DESIGNS[design][theme]
    w, h = ((600, 232) if mobile else (1000, 212))
    if design == 'research':
        body = [text(12, 80, 'Jiangtao Wang', 54 if mobile else 68, p['ink'], extra=' font-family="Georgia, Times New Roman, serif"'),
                text(14, 128, 'Robotics simulation & learning', 26, p['ink'], 500),
                text(14, 175, 'Physical AI / Sim2Real', 21, p['accent'])]
        if mobile:
            body.append(text(14, 215, 'Python / C++   ·   MuJoCo / Newton / Warp', 22, p['muted']))
        else:
            body.append(drawing('paths', 724, 35, p, 1.1))
            body.append(text(14, 202, 'Python / C++   ·   MuJoCo / Newton / Warp', 17, p['muted']))
    elif design == 'studio':
        h = 298 if mobile else 268
        body = [text(22, 40, 'Jiangtao Wang', 24, p['ink'], 500),
                text(20, 116, 'Geometry. Physics.', 45 if mobile else 58, p['ink'], 600),
                text(20, 181, 'Robot learning.', 45 if mobile else 58, p['ink'], 600),
                text(22, 232, 'Robotics simulation / Physical AI / Sim2Real', 20, p['accent'])]
        if mobile:
            body.append(text(22, 275, 'Python / C++   ·   MuJoCo / Newton / Warp', 22, p['muted']))
        else:
            body.append(drawing('mesh', 766, 43, p, 1.1))
    else:
        h = 180 if mobile else 144
        body = [text(12, 58, 'Jiangtao Wang', 44, p['ink'], 600),
                text(14, 103, 'Robotics simulation / Physical AI / Sim2Real', 22, p['accent'])]
        if mobile:
            body += [text(14, 141, 'Algorithm correctness, GPU efficiency,', 22, p['muted']),
                     text(14, 172, 'reproducible tests.', 22, p['muted'])]
        else:
            body.append(text(14, 136, 'Algorithm correctness, GPU efficiency, reproducible tests.', 18, p['muted']))
    return svg(w, h, 'Jiangtao Wang — Robotics Simulation, Physical AI, Sim2Real',
               'Personal identity. Technical linework is schematic, not experimental imagery.', body)


def eligible_groups(data, editorial):
    records = {f'{p["repository"]}#{p["number"]}': p for p in data['pull_requests']}
    result = []
    for group in editorial['selected']:
        selected = [records[k] for k in group['prs'] if k in records and
                    records[k]['repository_category'] == 'verified_upstream' and
                    records[k]['evidence']['summary_review_status'] == 'diff_and_discussion_reviewed']
        if selected and len(selected) == len(group['prs']):
            count = sum(p['repository'] == selected[0]['repository'] and p['repository_category'] == 'verified_upstream'
                        for p in data['pull_requests'])
            result.append((group, selected, count))
    return result


def card(label, count, theme, design=ACTIVE_DESIGN):
    p = DESIGNS[design][theme]
    descriptions = CARDS[label][1]
    h = 152 if design == 'studio' else 124
    body = []
    if design == 'studio':
        body.append(f'<rect width="390" height="152" rx="5" fill="{p["wash"]}"/>')
    body += [text(16, 36, label, 27, p['ink'], 600),
             text(374, 34, f'{count} merged PR' + ('s' if count != 1 else ''), 13, p['accent'], 500, 'end'),
             text(16, 72, descriptions[0], 16, p['muted']),
             text(16, 97, descriptions[1], 15, p['muted'])]
    if design == 'studio':
        body.append(text(16, 134, 'Verified upstream contributions', 12, p['accent']))
    else:
        body.append(line('M16 119h358', p, 1, True))
    return svg(390, h, f'{label}: {count} verified upstream merged PRs',
               '; '.join(descriptions) + '. Count derived from verified public PR records.', body)


def project_diagram(name, theme, mobile=False, design=ACTIVE_DESIGN):
    p = DESIGNS[design][theme]
    w, h = (600, 558) if mobile else (1000, 302)
    body = [text(18, 27, 'Method schematic', 17 if mobile else 14, p['muted'])]
    if design == 'studio':
        body.insert(0, f'<rect width="{w}" height="{h}" rx="5" fill="{p["wash"]}"/>')
    for i, (label, subtitle, kind) in enumerate(PROJECTS[name]):
        if mobile:
            y = 46 + i * 166
            body += [drawing(kind, 22, y, p, .88), text(230, y + 48, label, 25, p['ink'], 600)]
            body += [text(230, y + 85 + j*26, phrase, 21, p['muted'])
                     for j, phrase in enumerate(wrap(subtitle, width=25))]
            if i < 2:
                body.append(line(f'M18 {y+153}h564', p, 1, True))
        else:
            x = 32 + i * 334
            body += [drawing(kind, x + 50, 52, p),
                     text(x, 244, label, 24, p['ink'], 600),
                     text(x, 276, subtitle, 16, p['muted'])]
            if i < 2:
                body.append(line(f'M{x+235} 125h38m-6-6 6 6-6 6', p, 1.5, True))
    return svg(w, h, f'{name.title()} — method schematic',
               'Conceptual workflow: ' + ' → '.join(s[0] for s in PROJECTS[name]) +
               '. This is not an experiment screenshot or a measured performance plot.', body)


def picture(stem, alt, width='100%', mobile=False):
    result = ['<picture>']
    if mobile:
        result += [f'  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/{stem}-mobile-dark.svg">',
                   f'  <source media="(max-width: 600px)" srcset="assets/{stem}-mobile-light.svg">']
    result += [f'  <source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg">',
               f'  <img src="assets/{stem}-light.svg" alt="{escape(alt, quote=True)}" width="{width}">', '</picture>']
    return '\n'.join(result)


def build_assets(data, editorial, design=ACTIVE_DESIGN):
    output = {}
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            suffix = f'{"mobile-" if mobile else ""}{theme}.svg'
            output[f'assets/banner-{suffix}'] = banner(theme, mobile, design)
            for name in PROJECTS:
                output[f'assets/project-{name}-{suffix}'] = project_diagram(name, theme, mobile, design)
        for group, _, count in eligible_groups(data, editorial):
            slug = CARDS[group['label']][0]
            output[f'assets/contribution-{slug}-{theme}.svg'] = card(group['label'], count, theme, design)
    return output
