#!/usr/bin/env python3
"""World in One Day: 23 November 2026.

Draws a newspaper front page summing up the world news of
Monday 23 November 2026, using only the Python 3 standard library,
and writes it deterministically to entry.png (1024x1024, < 1 MiB).

News (checked 24 Nov 2026 against Principia, Daily Summary of
World, Broadcast Prism, The Brief, UN News, CASRAI, via web search
this session). Every story below happened, or was first reported,
on Monday 23 November 2026:
 1. WAR AT SEA: Ukraine says seven sea drones sank the Russian
    corvette Merkury at Benghazi, Libya, and hit the cargo ship
    MV Angara. A second Russian cargo ship, Sparta II, was hit
    in the Baltic Sea. Zelensky confirmed it on Monday.
 2. MARKETS: Nvidia's board reinstated Jensen Huang as chief
    executive on Monday 23 Nov; Nvidia shares surged about 30%
    (31.5% on Wall Street), leading an AI-stock rally.
 3. UKRAINE: Russian missile and drone strikes on the Kyiv
    region killed at least 15 people; a boy was pulled alive
    from the rubble. NATO was set to meet on Monday.
 4. USA-IRAN: the US Treasury imposed new sanctions on Iran's
    shadow banking network (more than two dozen exchange houses,
    front companies and key personnel). Iran vowed to counter
    the US naval blockade of Hormuz.
 5. INDONESIA: a fire at a sweets factory in Cikande, Banten
    killed 24 people; about 30 are still missing. The death
    toll was confirmed on Monday (the fire itself was Saturday).
 6. ALSO: Anthropic says AI helped prove the Riemann
    hypothesis; the EU proposed new Russia sanctions (60 banks,
    crypto platforms, sports); Bitcoin fell to about $55,100,
    its lowest since September 2024.
 Deliberately NOT included: COP31 in Antalya ended on SUNDAY
 22 November 2026 (UN News, CASRAI), so it is not 23 Nov news.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (or /output in the grader)
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (16, 32, 64)
NAVY2 = (24, 48, 92)
GOLD = (198, 158, 40)
RED = (178, 34, 34)
DARKRED = (120, 20, 20)
ORANGE = (230, 120, 30)
YELLOW = (240, 200, 40)
GREY = (110, 110, 105)
LIGHTGREY = (225, 220, 208)
BLUE = (30, 90, 160)
SKY = (120, 180, 220)
GREEN = (28, 110, 55)
WHITE = (255, 255, 255)
SEA = (40, 110, 150)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 integers, one per row, 5 bits (bit 4 = leftmost pixel).
# Standard 5x7 letterforms, written out for this entry.
_FONT = {
    'A': (14, 17, 17, 31, 17, 17, 17),
    'B': (30, 17, 17, 30, 17, 17, 30),
    'C': (14, 17, 16, 16, 16, 17, 14),
    'D': (30, 17, 17, 17, 17, 17, 30),
    'E': (31, 16, 16, 30, 16, 16, 31),
    'F': (31, 16, 16, 30, 16, 16, 16),
    'G': (14, 17, 16, 23, 17, 17, 15),
    'H': (17, 17, 17, 31, 17, 17, 17),
    'I': (14, 4, 4, 4, 4, 4, 14),
    'J': (7, 2, 2, 2, 2, 18, 12),
    'K': (17, 18, 20, 24, 20, 18, 17),
    'L': (16, 16, 16, 16, 16, 16, 31),
    'M': (17, 27, 21, 21, 17, 17, 17),
    'N': (17, 25, 21, 19, 17, 17, 17),
    'O': (14, 17, 17, 17, 17, 17, 14),
    'P': (30, 17, 17, 30, 16, 16, 16),
    'Q': (14, 17, 17, 17, 21, 18, 13),
    'R': (30, 17, 17, 30, 20, 18, 17),
    'S': (15, 16, 16, 14, 1, 1, 30),
    'T': (31, 4, 4, 4, 4, 4, 4),
    'U': (17, 17, 17, 17, 17, 17, 14),
    'V': (17, 17, 17, 17, 17, 10, 4),
    'W': (17, 17, 17, 21, 21, 27, 17),
    'X': (17, 17, 10, 4, 10, 17, 17),
    'Y': (17, 17, 10, 4, 4, 4, 4),
    'Z': (31, 1, 2, 4, 8, 16, 31),
    '0': (14, 17, 19, 21, 25, 17, 14),
    '1': (4, 12, 4, 4, 4, 4, 14),
    '2': (14, 17, 1, 6, 8, 16, 31),
    '3': (31, 2, 4, 2, 1, 17, 14),
    '4': (2, 6, 10, 18, 31, 2, 2),
    '5': (31, 16, 30, 1, 1, 17, 14),
    '6': (6, 8, 16, 30, 17, 17, 14),
    '7': (31, 1, 2, 4, 8, 8, 8),
    '8': (14, 17, 17, 14, 17, 17, 14),
    '9': (14, 17, 17, 15, 1, 2, 12),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 12, 12),
    ',': (0, 0, 0, 0, 12, 4, 8),
    ':': (0, 12, 12, 0, 12, 12, 0),
    ';': (0, 12, 12, 0, 12, 4, 8),
    '-': (0, 0, 0, 14, 0, 0, 0),
    '!': (4, 4, 4, 4, 4, 0, 4),
    '?': (14, 17, 1, 6, 4, 0, 4),
    '%': (25, 26, 2, 4, 8, 11, 19),
    '+': (0, 4, 4, 31, 4, 4, 0),
    '/': (1, 2, 2, 4, 8, 8, 16),
    '(': (2, 4, 8, 8, 8, 4, 2),
    ')': (8, 4, 2, 2, 2, 4, 8),
    '&': (12, 18, 20, 8, 21, 18, 13),
    '$': (4, 15, 20, 14, 5, 30, 4),
    "'": (4, 4, 8, 0, 0, 0, 0),
    '"': (10, 10, 10, 0, 0, 0, 0),
    '=': (0, 0, 31, 0, 31, 0, 0),
    '>': (8, 4, 2, 1, 2, 4, 8),
    '<': (2, 4, 8, 16, 8, 4, 2),
    '*': (0, 21, 14, 31, 14, 21, 0),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            span = min(self.w, x + w) - max(0, x)
            if span > 0:
                self.buf[base:base + span * 3] = bytes(color) * span

    def frame(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, t=2):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, t, 1, color)
            self.rect(cx + dx - t + 1, cy + dy, t, 1, color)

    def poly(self, pts, color):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.rect(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), 1, color)

    def text(self, x, y, s, scale, color):
        for ci, ch in enumerate(s):
            glyph = _FONT.get(ch, _FONT[' '])
            ox = x + ci * 6 * scale
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits >> (4 - col) & 1:
                        self.rect(ox + col * scale, y + row * scale,
                                  scale, scale, color)

    def text_c(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def para(self, x, y, lines, scale, color, lh):
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, scale, color)
        return y + len(lines) * lh


# ---------------------------------------------------------------- PNG encode
def encode_png(c):
    raw = bytearray()
    stride = c.w * 3
    for y in range(c.h):
        raw.append(0)
        raw += c.buf[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack('>I', len(data)) + kind + data
        return out + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = bytearray(b'\x89PNG\r\n\x1a\n')
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', c.w, c.h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    return bytes(png)

# ---------------------------------------------------------------- art
def draw_ship(c, x, y, w, hull, deck):
    # Warship silhouette on the sea; x,y = top-left of hull box.
    c.poly([(x, y), (x + w, y), (x + w - 12, y + 18), (x + 12, y + 18)], hull)
    c.rect(x + w // 3, y - 16, w // 3, 16, deck)
    c.rect(x + w // 2 - 2, y - 30, 4, 16, deck)
    c.line(x + 6, y + 24, x + w - 6, y + 24, SEA, 2)
    c.line(x + 20, y + 30, x + w - 20, y + 30, SEA, 2)


def draw_blast(c, cx, cy, r):
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r // 2
        pts.append((cx + int(rr * math.cos(ang)), cy + int(rr * math.sin(ang))))
    c.poly(pts, ORANGE)
    c.disc(cx, cy, r // 2, YELLOW)
    c.disc(cx, cy, r // 4, WHITE)


def draw_chart(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, LIGHTGREY, 1)
    c.line(x + 8, y + h - 8, x + w - 8, y + h - 8, GREY, 1)
    c.line(x + 8, y + 8, x + 8, y + h - 8, GREY, 1)
    pts = [(x + 14, y + h - 20), (x + 60, y + h - 28), (x + 110, y + h - 24),
           (x + 160, y + h - 38), (x + 210, y + h - 44), (x + 260, y + h - 52),
           (x + w - 16, y + 10)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], GREEN, 3)
    tip = pts[-1]
    c.poly([(tip[0], tip[1] - 2), (tip[0] - 12, tip[1] + 2),
            (tip[0] - 2, tip[1] + 12)], GREEN)
    c.text(x + 16, y + 10, '+30%', 3, GREEN)


def draw_bank(c, x, y, w, h):
    # A bank facade (roof, columns, steps) crossed by a red sanction bar.
    c.poly([(x, y + 18), (x + w // 2, y), (x + w, y + 18)], NAVY2)
    c.rect(x + 6, y + 18, w - 12, h - 30, NAVY)
    for i in range(4):
        cx = x + 18 + i * ((w - 36) // 3)
        c.rect(cx, y + 26, 10, h - 46, WHITE)
    c.rect(x, y + h - 12, w, 6, NAVY2)
    c.rect(x - 4, y + h - 6, w + 8, 6, NAVY2)
    c.line(x + 4, y + 6, x + w - 4, y + h - 10, RED, 5)


def draw_flame(c, cx, cy, s):
    # A simple flame: outer orange tongue, inner yellow core.
    c.poly([(cx, cy - 30 * s), (cx + 12 * s, cy - 8 * s),
            (cx + 8 * s, cy + 10 * s), (cx - 8 * s, cy + 10 * s),
            (cx - 12 * s, cy - 8 * s)], ORANGE)
    c.poly([(cx, cy - 14 * s), (cx + 6 * s, cy - 2 * s),
            (cx + 4 * s, cy + 10 * s), (cx - 4 * s, cy + 10 * s),
            (cx - 6 * s, cy - 2 * s)], YELLOW)
    c.disc(cx, cy + 6 * s, 3 * s, WHITE)


def draw_building_hit(c, x, y, w, h):
    # A shelled apartment block: broken top, dark windows, blast above.
    c.rect(x, y + 20, w, h - 20, NAVY2)
    c.poly([(x, y + 20), (x + w // 4, y), (x + w // 2, y + 20),
            (x + 3 * w // 4, y + 6), (x + w, y + 20)], NAVY2)
    for row in range(3):
        for col in range(4):
            wx = x + 12 + col * ((w - 24) // 4)
            wy = y + 34 + row * ((h - 54) // 3)
            c.rect(wx, wy, 12, 14, GOLD if (row + col) % 3 == 0 else WHITE)


# ---------------------------------------------------------------- panels
def panel(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, INK, 2)


def kicker(c, x, y, s, color):
    c.text(x, y, s, 2, color)


def draw_masthead(c):
    c.rect(0, 0, W, 116, NAVY)
    c.text_c(W // 2, 16, 'THE WORLD IN ONE DAY', 5, WHITE)
    c.text_c(W // 2, 62, 'MONDAY 23 NOVEMBER 2026', 3, GOLD)
    c.hline(0, 112, W, GOLD, 4)
    c.text_c(W // 2, 126, 'SIX STORIES THAT DEFINED MONDAY - FROM BENGHAZI TO WALL STREET',
             2, NAVY)


def draw_lead_merkury(c):
    x, y, w, h = 16, 152, 600, 288
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'WAR AT SEA - CONFIRMED MONDAY', RED)
    c.text(x + 16, y + 38, 'UKRAINE SINKS', 4, NAVY)
    c.text(x + 16, y + 70, 'RUSSIAN WARSHIP', 4, NAVY)
    c.text(x + 16, y + 102, 'OFF LIBYA', 4, NAVY)
    body = [
        'SEVEN SEA DRONES SANK',
        'THE RUSSIAN CORVETTE',
        'MERKURY AT BENGHAZI,',
        'LIBYA, ZELENSKY SAID.',
        'THE CARGO SHIP MV',
        'ANGARA WAS HIT TOO.',
        'A SECOND RUSSIAN SHIP',
        'WAS HIT IN THE BALTIC.',
    ]
    c.para(x + 16, y + 146, body, 2, INK, 15)
    # art, right column: a burning warship on the sea
    draw_ship(c, x + 420, y + 190, 150, NAVY, NAVY2)
    draw_blast(c, x + 495, y + 168, 28)
    c.line(x + 410, y + 236, x + 580, y + 236, SEA, 2)
    c.line(x + 430, y + 244, x + 560, y + 244, SEA, 2)


def draw_nvidia(c):
    x, y, w, h = 628, 152, 380, 288
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'MARKETS - MONDAY', RED)
    c.text(x + 16, y + 38, 'HUANG IS BACK,', 3, NAVY)
    c.text(x + 16, y + 62, 'NVIDIA SOARS 30%', 3, NAVY)
    body = [
        'NVIDIA REINSTATED',
        'JENSEN HUANG AS CHIEF',
        'EXECUTIVE ON MONDAY.',
        'SHARES SOARED 30%.',
        'WALL STREET CHEERED',
        'THE AI COMEBACK: THE',
        'NASDAQ ROSE WITH IT.',
    ]
    c.para(x + 16, y + 96, body, 2, INK, 15)
    draw_chart(c, x + 16, y + 208, w - 32, 64)


def draw_kyiv(c):
    x, y, w, h = 16, 452, 484, 248
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'UKRAINE - MONDAY', RED)
    c.text(x + 16, y + 38, '15 KILLED AS RUSSIA', 3, NAVY)
    c.text(x + 16, y + 62, 'STRIKES KYIV REGION', 3, NAVY)
    body = [
        'RUSSIAN MISSILES AND',
        'DRONES HIT THE KYIV',
        'REGION. AT LEAST 15',
        'PEOPLE WERE KILLED. A',
        'BOY WAS PULLED ALIVE',
        'FROM THE RUBBLE. NATO',
        'WILL MEET ON MONDAY.',
    ]
    c.para(x + 16, y + 94, body, 2, INK, 15)
    # art, right column: a shelled block under a blast
    draw_building_hit(c, x + 350, y + 140, 110, 84)
    draw_blast(c, x + 405, y + 128, 20)


def draw_iran(c):
    x, y, w, h = 512, 452, 496, 248
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'USA - IRAN', RED)
    c.text(x + 16, y + 38, "US SANCTIONS IRAN'S", 3, NAVY)
    c.text(x + 16, y + 62, 'SHADOW BANKS', 3, NAVY)
    body = [
        'THE US TREASURY HIT',
        "IRAN'S SHADOW BANKING",
        'NETWORK: MORE THAN 20',
        'EXCHANGE HOUSES AND',
        'FRONT COMPANIES. TEHRAN',
        'VOWED TO COUNTER THE US',
        'BLOCKADE OF HORMUZ.',
    ]
    c.para(x + 16, y + 94, body, 2, INK, 15)
    # art, right column: a bank crossed by a red sanction bar
    draw_bank(c, x + 340, y + 130, 130, 92)


def draw_indonesia(c):
    x, y, w, h = 16, 712, 600, 168
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'INDONESIA - TOLL CONFIRMED MONDAY', RED)
    c.text(x + 16, y + 38, '24 DEAD IN FACTORY FIRE', 3, NAVY)
    body = [
        'A SWEETS FACTORY FIRE IN',
        'CIKANDE, BANTEN, KILLED 24.',
        'ABOUT 30 ARE STILL MISSING.',
        'THE TOLL WAS CONFIRMED MONDAY.',
    ]
    c.para(x + 16, y + 72, body, 2, INK, 15)
    draw_flame(c, x + 540, y + 96, 2)


def draw_also(c):
    x, y, w, h = 628, 712, 380, 168
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'ALSO TODAY', RED)
    items = [
        ['AI PROVES RIEMANN',
         'HYPOTHESIS, SAYS ANTHROPIC.'],
        ['EU PROPOSES NEW RUSSIA',
         'SANCTIONS: BANKS, CRYPTO.'],
        ['BITCOIN FALLS TO $55,100,',
         'LOWEST SINCE SEPT 2024.'],
    ]
    yy = y + 40
    for it in items:
        c.rect(x + 16, yy + 2, 8, 8, RED)
        c.para(x + 32, yy, it, 2, INK, 14)
        yy += 42


def draw_footer(c):
    c.hline(16, 892, W - 32, GOLD, 3)
    c.text_c(W // 2, 906, 'SOURCES: REUTERS, BBC, CNN, AP, WSJ, THE TIMES', 2, NAVY)
    c.text_c(W // 2, 928, 'ALL STORIES AS REPORTED ON MONDAY 23 NOVEMBER 2026', 2, INK)
    c.text_c(W // 2, 950, 'DRAWN FROM REPORTS PUBLISHED ON THE DAY.', 2, GREY)


def main():
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    draw_lead_merkury(c)
    draw_nvidia(c)
    draw_kyiv(c)
    draw_iran(c)
    draw_indonesia(c)
    draw_also(c)
    draw_footer(c)
    out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'entry.png'), 'wb') as f:
        f.write(encode_png(c))


if __name__ == '__main__':
    main()
