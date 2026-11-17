"""Reconstruct scalable packaging illustrations from the supplied brand photos."""
from pathlib import Path
from math import sin, cos, radians

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / 'assets/brand'
IMAGES = ROOT / 'assets/images'
BRAND.mkdir(parents=True, exist_ok=True)
IMAGES.mkdir(parents=True, exist_ok=True)

def seal(color='#f4edda', background='none', prefix='seal'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none">
    <defs><path id="{prefix}-top" d="M 17,62 A 43,43 0 0 1 103,62"/><path id="{prefix}-bottom" d="M 13,62 A 47,47 0 0 0 107,62"/></defs>
    <circle cx="60" cy="60" r="57" fill="{background}" stroke="{color}" stroke-width="2.1"/>
    <circle cx="60" cy="60" r="35" stroke="{color}" stroke-width="1.5"/>
    <g fill="{color}" font-family="Arial, sans-serif" font-weight="700" font-size="13.5" letter-spacing="2.1"><text><textPath href="#{prefix}-top" startOffset="50%" text-anchor="middle">COFFEE</textPath></text><text><textPath href="#{prefix}-bottom" startOffset="50%" text-anchor="middle">FACTORY</textPath></text></g>
    <g stroke="{color}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M42 59 Q60 65 78 59 L74 73 Q60 87 46 73 Z"/><path d="M78 60 C92 54 89 72 77 72"/><path d="M45 81 H78"/><path d="M52 53 C44 48 70 49 62 43 C53 37 70 37 67 31"/></g>
    <g fill="{color}" transform="rotate(-28 20 64)"><ellipse cx="20" cy="64" rx="3.1" ry="5.3"/><path d="M20 59 Q17 64 20 69" stroke="{background if background != 'none' else '#252620'}" stroke-width=".7"/></g>
    <g fill="{color}" transform="rotate(28 100 64)"><ellipse cx="100" cy="64" rx="3.1" ry="5.3"/><path d="M100 59 Q97 64 100 69" stroke="{background if background != 'none' else '#252620'}" stroke-width=".7"/></g></svg>'''

(BRAND / 'seal.svg').write_text(seal(), encoding='utf-8')
(BRAND / 'seal-dark.svg').write_text(seal('#252620', '#f4f0e7'), encoding='utf-8')
(BRAND / 'favicon.svg').write_text(seal('#f4edda', '#252620'), encoding='utf-8')
(BRAND / 'bean.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 44"><ellipse cx="18" cy="22" rx="14" ry="20" transform="rotate(30 18 22)" fill="#bc7955"/><path d="M25 6 C8 14 28 28 11 39" fill="none" stroke="#252620" stroke-width="2"/></svg>''', encoding='utf-8')

def botanical(accent):
    leaves = []
    for x, y, angle, scale in [(21,37,-55,.9),(39,24,-30,1),(55,17,-10,.9),(72,24,28,.9),(85,39,55,.85),(72,58,120,.8),(49,64,160,.9),(28,59,205,.8)]:
        leaves.append(f'''<g transform="translate({x} {y}) rotate({angle}) scale({scale})"><path d="M0 0 Q-12 -17 0 -30 Q12 -17 0 0" fill="url(#leaf)" stroke="{accent}" stroke-width=".65"/><path d="M0 -2 V-27 M0 -8 L-5 -14 M0 -15 L5 -21" stroke="{accent}" stroke-width=".6" fill="none"/></g>''')
    cherries = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#cherry)" stroke="{accent}" stroke-width=".6"/>' for x,y,r in [(41,39,7),(54,32,6),(62,44,7),(49,50,6),(35,51,5),(57,59,5)])
    return f'<g><path d="M20 73 Q45 46 82 19" stroke="{accent}" stroke-width="1.2" fill="none"/>{"".join(leaves)}{cherries}</g>'

def capsule(accent, uid):
    return f'''<g><path d="M13 17 L5 65 Q39 80 73 65 L65 17 Z" fill="url(#{uid})" stroke="{accent}" stroke-width="1"/><ellipse cx="39" cy="17" rx="26" ry="8" fill="url(#{uid})" stroke="{accent}" stroke-width="1.5"/><ellipse cx="39" cy="67" rx="36" ry="9" fill="url(#{uid})" stroke="{accent}" stroke-width="1"/><path d="M20 25 L15 60 M27 28 L24 65 M53 26 L57 61" stroke="#fff" opacity=".2" stroke-width="1.5"/></g>'''

def box(name, base, top, side, accent, roast, flavors):
    logo = seal('#e9dfc0' if name != 'CREMA' else '#33352d', 'none', name.lower()).replace('<svg ', '<svg x="18" y="12" width="61" height="61" ')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="460" viewBox="0 0 620 460">
    <defs><linearGradient id="front" x1="0" y1="0" x2="0.2" y2="1"><stop stop-color="{base}"/><stop offset="1" stop-color="{side}"/></linearGradient><linearGradient id="leaf"><stop stop-color="{accent}" stop-opacity=".35"/><stop offset=".5" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".3"/></linearGradient><radialGradient id="cherry" cx="32%" cy="28%"><stop stop-color="#f6d7ac"/><stop offset=".28" stop-color="{accent}"/><stop offset="1" stop-color="{side}"/></radialGradient><linearGradient id="metal"><stop stop-color="{side}"/><stop offset=".22" stop-color="{accent}"/><stop offset=".42" stop-color="#efd3ac"/><stop offset=".61" stop-color="{accent}"/><stop offset="1" stop-color="{side}"/></linearGradient><filter id="shadow" x="-35%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="12"/></filter><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".65" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".07"/></feComponentTransfer><feBlend in="SourceGraphic" mode="multiply"/></filter></defs>
    <ellipse cx="327" cy="326" rx="210" ry="18" transform="rotate(-23 327 326)" fill="#28251b" opacity=".19" filter="url(#shadow)"/>
    <g transform="translate(69 210) rotate(-23 220 42)">
      <path d="M0 0 L22 -21 H462 L440 0 Z" fill="{top}"/>
      <path d="M440 0 L462 -21 V63 L440 84 Z" fill="{side}"/>
      <path d="M0 0 H440 V84 H0 Z" fill="url(#front)"/>
      <path d="M0 .7 H440" stroke="#fff" opacity=".25"/>
      <path d="M0 83.3 H440" stroke="#000" opacity=".2"/>
      {logo}
      <path d="M91 13 V70" stroke="{accent}" stroke-width=".7" opacity=".7"/>
      <g font-family="Arial, sans-serif"><text x="103" y="35" font-size="22" fill="{accent}">{name}</text><text x="104" y="49" font-size="7.5" fill="{'#e9dfc0' if name != 'CREMA' else '#33352d'}">{roast.upper()} ROAST</text><text x="104" y="66" font-size="6.8" fill="{'#e9dfc0' if name != 'CREMA' else '#33352d'}">{flavors}</text></g>
      <g transform="translate(242 2) scale(.91)">{botanical(accent)}</g>
      <g transform="translate(309 24) scale(.57)">{capsule(accent, 'metal')}</g>
      <path d="M366 13 V70" stroke="{accent}" stroke-width=".7" opacity=".7"/>
      <g fill="{'#e9dfc0' if name != 'CREMA' else '#33352d'}" font-family="Arial, sans-serif"><text x="377" y="35" font-size="22">10</text><text x="377" y="49" font-size="6">ALUMINUM</text><text x="377" y="59" font-size="6">COFFEE CAPSULES</text><text x="378" y="70" font-size="4.5">COFFEE FACTORY</text></g>
      <path d="M440 0 L462 -21 V63 L440 84 Z" fill="{accent}" opacity=".5"/>
      <path d="M0 0 H440 V84 H0 Z" fill="none" stroke="#000" stroke-opacity=".1"/>
      <g font-family="Arial, sans-serif" font-size="5.5" fill="{'#e9dfc0' if name != 'CREMA' else '#33352d'}" transform="translate(173 -8) skewX(-44)"><text>COFFEE FACTORY · GOOD COFFEE CREATES A BRIGHTER DAY</text></g>
    </g>
    <ellipse cx="162" cy="359" rx="51" ry="12" fill="#28251b" opacity=".12" filter="url(#shadow)"/>
    <g transform="translate(118 272) rotate(13 39 40) scale(1.05)">{capsule(accent, 'metal')}</g>
    </svg>'''

for args in [('CREMA','#f3ead4','#fff5de','#d7c6a3','#b7803c','medium','Smooth · Creamy · Balanced'),('CLASSICO','#323631','#4a4d44','#232621','#c58a5d','medium','Balanced · Smooth · Aromatic'),('INTENSO','#2a302c','#3a413a','#1d2420','#a74e5a','dark','Bold · Rich · Full bodied')]:
    (IMAGES / (args[0].lower()+'.svg')).write_text(box(*args),encoding='utf-8')

def bag(large=False):
    body = '#c3b18d' if large else '#e6dbc1'
    logo = seal('#e9dfc0','none','bag-large' if large else 'bag-small').replace('<svg ','<svg x="-37" y="-10" width="74" height="74" ')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="460" viewBox="0 0 620 460"><defs><linearGradient id="bag" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{body}"/><stop offset=".4" stop-color="{'#d4c3a1' if large else '#f3ead5'}"/><stop offset="1" stop-color="{body}"/></linearGradient><filter id="shadow"><feGaussianBlur stdDeviation="12"/></filter></defs><ellipse cx="310" cy="386" rx="95" ry="15" fill="#29291e" opacity=".17" filter="url(#shadow)"/><g transform="translate(310 228) rotate({'-7' if large else '7'}) scale({'1.13' if large else '.96'})"><path d="M-72 -140 H72 L84 -119 L79 -95 L90 130 Q0 147 -90 130 L-79 -95 L-84 -119 Z" fill="url(#bag)" stroke="#ad9c7d" stroke-width=".6"/><path d="M-72 -140 H72 L80 -119 H-80 Z" fill="{body}"/><path d="M-78 -118 H78 M-78 -113 H78" stroke="#aa9978" stroke-width="1"/><path d="M-79 -95 L-64 -80 L-68 119 L-88 131 M79 -95 L64 -80 L68 119 L88 131" fill="none" stroke="#aa9978" stroke-opacity=".55"/><path d="M-68 119 Q0 132 68 119" stroke="#ad9c7d" fill="none"/><rect x="-64" y="-72" width="128" height="173" fill="#2b302a"/>{logo}<g font-family="Arial, sans-serif" text-anchor="middle"><text y="-49" font-size="6" letter-spacing="1.6" fill="#e9dfc0">COFFEE FACTORY</text><text y="82" font-size="7.5" letter-spacing="1.5" fill="#c88f64">{'MORE GOOD TO SHARE' if large else 'YOUR DAILY RITUAL'}</text><text y="123" font-size="5.3" letter-spacing=".9" fill="#484c3b">GOOD COFFEE. BRIGHTER DAYS.</text></g><circle cx="0" cy="-92" r="6" fill="#b1a080"/><circle cx="0" cy="-92" r="3" fill="#9e8f72"/></g></svg>'''

(IMAGES / 'small-bag.svg').write_text(bag(),encoding='utf-8')
(IMAGES / 'large-bag.svg').write_text(bag(True),encoding='utf-8')
print('Prepared 4 brand assets and 5 packaging illustrations.')
