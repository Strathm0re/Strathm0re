#!/usr/bin/env python3
"""Generate closed-loop automation schema SVG (light + GitHub-dark variants)."""

W, H = 1400, 430

ICONS = {
    # each icon drawn in a local coord system centered at (0,0), scale ~1, stroke-based
    "models": '''
      <circle cx="-9" cy="-10" r="3.2"/><circle cx="-9" cy="0" r="3.2"/><circle cx="-9" cy="10" r="3.2"/>
      <circle cx="9" cy="-5" r="3.2"/><circle cx="9" cy="5" r="3.2"/>
      <path d="M-5.8,-10 L5.8,-5 M-5.8,0 L5.8,-5 M-5.8,0 L5.8,5 M-5.8,10 L5.8,5"/>
    ''',
    "arm": '''
      <rect x="-13" y="11" width="26" height="4" rx="1.5"/>
      <circle cx="0" cy="8" r="2.6"/>
      <path d="M0,8 L-8,-5 L9,-13"/>
      <path d="M9,-13 l6,-3 M9,-13 l7,2"/>
    ''',
    "ot2": '''
      <rect x="-14" y="4" width="28" height="9" rx="1.5"/>
      <path d="M-6,4 V-9 M6,4 V-9"/>
      <path d="M-6,-9 h4 M6,-9 h-4" stroke-width="1"/>
      <path d="M-4,7 h5 M-4,10 h5" stroke-width="0.9"/>
    ''',
    "scope": '''
      <rect x="-12" y="12" width="24" height="3.5" rx="1.5"/>
      <path d="M-5,12 C-10,4 -6,-5 3,-7"/>
      <path d="M3,-7 L11,-13 M11,-13 l3,-2" stroke-width="2"/>
      <path d="M-1,-2 L3,7" stroke-width="2"/>
      <path d="M-6,8 H6" stroke-width="1"/>
    ''',
    "data": '''
      <ellipse cx="0" cy="-9" rx="11" ry="4"/>
      <path d="M-11,-9 V8 a11,4 0 0 0 22,0 V-9"/>
      <path d="M-11,-1 a11,4 0 0 0 22,0 M-11,4 a11,4 0 0 0 22,0" stroke-width="0.9"/>
    ''',
}

ROLES = {
    # role: (stroke, fill, arrow_color)
    "model":  {"stroke": "#9B8AC4", "fill": "#F3EFFA"},
    "flow":   {"stroke": "#5B8DB8", "fill": "#EAF3FB"},
    "grow":   {"stroke": "#6BA368", "fill": "#EDF7EF"},
    "data":   {"stroke": "#C9862B", "fill": "#FDF6EA"},
}

DARK_ROLES = {
    "model":  {"stroke": "#B083F0", "fill": "#211A33"},
    "flow":   {"stroke": "#6CB6FF", "fill": "#16242F"},
    "grow":   {"stroke": "#4AC26B", "fill": "#122117"},
    "data":   {"stroke": "#DBB24C", "fill": "#2E2410"},
}

# card: (x, y, role, icon, label, sub)
CARDS = [
    (80,   167, "model", "models", "ML / QC Models",     "propose next experiments"),
    (520,  50,  "flow",  "arm",    "6-DoF Robot Arm",     "plate &amp; module handling"),
    (1120, 50,  "flow",  "ot2",    "OT-2 Liquid Handler", "automated synthesis"),
    (1120, 284, "grow",  "scope",  "Optical Microscope",  "real-time in-situ imaging"),
    (520,  284, "data",  "data",   "Experiment Data",     "images + measurements"),
]

CW, CH = 200, 100  # card size

def card(x, y, role, icon, label, sub, c):
    st, fl = c[role]["stroke"], c[role]["fill"]
    cx, cy = x + CW / 2, y + 36
    return f'''
  <g>
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="14" fill="{fl}" stroke="{st}" stroke-width="1.6"/>
    <circle cx="{cx}" cy="{cy}" r="24" fill="#FFFFFF" fill-opacity="0.85" stroke="{st}" stroke-width="1.2"/>
    <g transform="translate({cx},{cy})" stroke="{st}" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
    <text x="{cx}" y="{y+76}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="bold" fill="{T['text']}">{label}</text>
    <text x="{cx}" y="{y+92}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10.5" fill="{T['sub']}">{sub}</text>
  </g>'''

def arrow(d, color, dashed=False, width=2.2):
    da = ' stroke-dasharray="7 5"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} marker-end="url(#ah-{"g" if color==C["grow"]["stroke"] else "b"})"/>'

def build(c, t):
    global C, T
    C, T = c, t
    blue, green = c["flow"]["stroke"], c["grow"]["stroke"]
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="ah-b" markerWidth="9" markerHeight="8" refX="7.5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{blue}"/></marker>
    <marker id="ah-g" markerWidth="9" markerHeight="8" refX="7.5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{green}"/></marker>
  </defs>
  <rect width="{W}" height="{H}" fill="{t['bg']}"/>
  <text x="80" y="27" font-family="Helvetica,Arial,sans-serif" font-size="15" font-weight="bold" fill="{t['text']}">Closed-Loop Autonomous Experimentation</text>''']

    # arrows: models -> arm -> ot2 -> scope -> data -> (feedback) models
    parts.append(arrow("M 302,192 L 512,116", blue))                       # models -> arm
    parts.append(arrow("M 722,100 L 1112,100", blue))                      # arm -> ot2
    parts.append(arrow("M 1220,152 L 1220,276", blue))                     # ot2 -> scope
    parts.append(arrow("M 1118,334 L 728,334", blue))                      # scope -> data
    parts.append(arrow("M 518,318 L 308,242", green, dashed=True, width=2.6))  # data -> models

    lbl = lambda x, y, s, fill, anchor="middle", size=11: f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" font-weight="bold" fill="{fill}">{s}</text>'
    parts.append(lbl(382, 138, "experiment proposal", t["albl"]))
    parts.append(lbl(920, 90, "load &amp; transfer", t["albl"]))
    parts.append(lbl(1234, 218, "reaction observed", t["albl"], anchor="start"))
    parts.append(lbl(920, 324, "images &amp; metrics", t["albl"]))
    parts.append(lbl(430, 262, "closed-loop learning", green))

    for x, y, role, icon, label, sub in CARDS:
        parts.append(card(x, y, role, icon, label, sub, c))

    # legend
    lx, ly = 80, 414
    parts.append(f'<path d="M {lx},{ly-4} h 34" stroke="{blue}" stroke-width="2.2" marker-end="url(#ah-b)"/>')
    parts.append(lbl(lx+44, ly, "automation flow", t["sub"], anchor="start", size=10.5))
    parts.append(f'<path d="M {lx+200},{ly-4} h 34" stroke="{green}" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#ah-g)"/>')
    parts.append(lbl(lx+244, ly, "data feedback (loop closes)", t["sub"], anchor="start", size=10.5))

    parts.append("</svg>")
    return "\n".join(parts)

LIGHT_T = {"bg": "#FFFFFF", "text": "#333333", "sub": "#666666", "albl": "#555555"}
DARK_T  = {"bg": "#0D1117", "text": "#E6EDF3", "sub": "#8B949E", "albl": "#A8B3BF"}

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "closed-loop-light.svg"), "w").write(build(ROLES, LIGHT_T))
open(os.path.join(out, "closed-loop-dark.svg"), "w").write(build(DARK_ROLES, DARK_T))
print("written:", os.listdir(out))
