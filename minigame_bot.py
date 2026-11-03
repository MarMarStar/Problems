"""
Minigame automation: rhythm lane -> frequency finder -> ring skill check.

Setup:   pip install mss opencv-python numpy pynput
Step 1:  python minigame_bot.py calibrate     (draw a box over each UI element)
Step 2:  python minigame_bot.py run           (F8 = start/pause, F9 = quit)

Run the game in windowed/borderless mode on the primary monitor, 100% display
scaling recommended (otherwise mouse coordinates may be offset).
"""
import json
import math
import sys
import time
from pathlib import Path

import cv2
import mss
import numpy as np
from pynput import keyboard, mouse

CONFIG_FILE = Path("bot_config.json")
NOTE_TEMPLATE = Path("note.png")  # optional: cropped image of a rhythm note

DEFAULTS = {
    "regions": {},                 # filled by calibrate: lane, hit_zone, freq_wave, freq_track, ring
    "rhythm_key": "space",         # "space", "mouse", or any single character
    "ring_key": "space",           # "space" or "mouse"
    "rhythm_diff_trigger": 0.06,   # fraction of hit-zone pixels that must change
    "rhythm_cooldown": 0.12,       # seconds between rhythm presses
    "ring_latency": 0.05,          # seconds of input/screen latency to compensate
    "ring_tolerance": 0.30,         # fraction of green arc half-width to accept
    "freq_step_px": 8,
    "freq_settle": 0.05,           # seconds to wait after each slider step
    "freq_hold_secs": 2.5,
    "fps": 60,
}

kb = keyboard.Controller()
ms = mouse.Controller()
running = False
quit_flag = False


# ───────────────────────── config / calibration ─────────────────────────
def load_config():
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        cfg.update(json.loads(CONFIG_FILE.read_text()))
    return cfg


def calibrate():
    cfg = load_config()
    with mss.mss() as sct:
        mon = sct.monitors[1]
        shot = np.array(sct.grab(mon))[:, :, :3]
    scale = 0.6 if shot.shape[1] > 1500 else 1.0
    view = cv2.resize(shot, None, fx=scale, fy=scale)
    prompts = {
        "lane": "Rhythm lane (whole staff incl. hit zone)",
        "hit_zone": "Rhythm HIT ZONE (the grey centre box)",
        "freq_wave": "Frequency: red waveform area",
        "freq_track": "Frequency: slider track (thin strip the handle moves along)",
        "ring": "Ring: tight square around the circle",
    }
    print("Show each UI element on screen (take a screenshot state per element if needed).")
    print("Draw a box, press ENTER/SPACE to confirm, 'c' to skip.")
    for key, text in prompts.items():
        input(f"\nPut the game in the state showing: {text}\nPress Enter here, then the capture is taken...")
        time.sleep(2)
        with mss.mss() as sct:
            shot = np.array(sct.grab(mon))[:, :, :3]
        view = cv2.resize(shot, None, fx=scale, fy=scale)
        x, y, w, h = cv2.selectROI(text, view, showCrosshair=True)
        cv2.destroyAllWindows()
        if w and h:
            cfg["regions"][key] = [
                int(x / scale) + mon["left"], int(y / scale) + mon["top"],
                int(w / scale), int(h / scale),
            ]
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
    print(f"Saved {CONFIG_FILE}")


# ───────────────────────────── helpers ─────────────────────────────
def grab(sct, region):
    x, y, w, h = region
    return np.array(sct.grab({"left": x, "top": y, "width": w, "height": h}))[:, :, :3]


def act(kind, down_time=0.02):
    """Perform the configured input: 'space', 'mouse', or a character."""
    if kind == "mouse":
        ms.press(mouse.Button.left)
        time.sleep(down_time)
        ms.release(mouse.Button.left)
    else:
        k = keyboard.Key.space if kind == "space" else kind
        kb.press(k)
        time.sleep(down_time)
        kb.release(k)


def wrap180(a):
    return (a + 180) % 360 - 180


# ───────────────────────── 1. rhythm lane ─────────────────────────
class Rhythm:
    def __init__(self, cfg):
        self.cfg = cfg
        self.baseline = None
        self.last = 0.0
        self.template = cv2.imread(str(NOTE_TEMPLATE), 0) if NOTE_TEMPLATE.exists() else None

    def lane_visible(self, sct):
        """Staff lines are long bright horizontal lines spanning the lane."""
        img = cv2.cvtColor(grab(sct, self.cfg["regions"]["lane"]), cv2.COLOR_BGR2GRAY)
        rows = (img > 200).mean(axis=1)
        return (rows > 0.6).sum() >= 2

    def step(self, sct):
        reg = self.cfg["regions"].get("hit_zone")
        if not reg:
            return
        zone = cv2.cvtColor(grab(sct, reg), cv2.COLOR_BGR2GRAY)
        now = time.time()
        if self.template is not None:
            res = cv2.matchTemplate(zone, self.template, cv2.TM_CCOEFF_NORMED)
            hit = res.max() > 0.7
        else:
            if self.baseline is None:
                self.baseline = zone.astype(np.float32)
            diff = np.abs(zone.astype(np.float32) - self.baseline) > 40
            hit = diff.mean() > self.cfg["rhythm_diff_trigger"]
            self.baseline = 0.9 * self.baseline + 0.1 * zone  # slow-adapting background
        if hit and now - self.last > self.cfg["rhythm_cooldown"]:
            act(self.cfg["rhythm_key"])
            self.last = now


# ───────────────────────── 2. frequency finder ─────────────────────────
def red_mask(img):
    b, g, r = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
    return (r > 200) & (g < 130) & (b < 130)


def waveform_present(img):
    return red_mask(img).sum() > 150


def roughness(img):
    """Mean absolute jitter of the red curve (low = closer to correct frequency)."""
    m = red_mask(img)
    cols = np.where(m.any(axis=0))[0]
    if len(cols) < 20:
        return float("inf")
    ys = np.array([np.where(m[:, c])[0].mean() for c in cols])
    return float(np.abs(np.diff(ys, n=2)).mean())


def solve_frequency(sct, cfg):
    tx, ty, tw, th = cfg["regions"]["freq_track"]
    wave = cfg["regions"]["freq_wave"]
    yc = ty + th // 2
    xs = list(range(tx, tx + tw, cfg["freq_step_px"]))

    ms.position = (xs[0], yc)
    time.sleep(0.05)
    ms.press(mouse.Button.left)
    scores = []
    try:
        for x in xs:                         # sweep while holding
            ms.position = (x, yc)
            time.sleep(cfg["freq_settle"])
            scores.append(roughness(grab(sct, wave)))
        s = np.convolve(np.nan_to_num(scores, posinf=1e9), np.ones(3) / 3, mode="same")
        best = xs[int(np.argmin(s))]
        print(f"[freq] best x={best} roughness={s.min():.2f}")
        ms.position = (best, yc)             # go to the sweet spot and hold
        end = time.time() + cfg["freq_hold_secs"]
        while time.time() < end and waveform_present(grab(sct, wave)):
            time.sleep(0.03)
    finally:
        ms.release(mouse.Button.left)


# ───────────────────────── 3. ring skill check ─────────────────────────
class Ring:
    def __init__(self, cfg):
        self.cfg = cfg
        self.prev = None          # (angle, time)
        self.last_press = 0.0

    @staticmethod
    def polar_scores(img):
        h, w = img.shape[:2]
        cx, cy = w / 2, h / 2
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green = ((hsv[:, :, 0] > 30) & (hsv[:, :, 0] < 90) &
                 (hsv[:, :, 1] > 120) & (hsv[:, :, 2] > 120))
        white = (hsv[:, :, 1] < 70) & (hsv[:, :, 2] > 215)
        gs, ws = np.zeros(360), np.zeros(360)
        R = min(w, h) / 2
        for a in range(360):
            rad = math.radians(a)
            for f in (0.70, 0.78, 0.86, 0.94):     # sample across the ring thickness
                x = int(cx + math.sin(rad) * R * f)
                y = int(cy - math.cos(rad) * R * f)
                if 0 <= x < w and 0 <= y < h:
                    gs[a] += green[y, x]
                    ws[a] += white[y, x]
        return gs, ws

    def active(self, img):
        gs, _ = self.polar_scores(img)
        return (gs > 0).sum() > 10

    def step(self, img):
        gs, ws = self.polar_scores(img)
        green_idx = np.where(gs > 0)[0]
        if len(green_idx) < 8 or ws.max() == 0:
            return
        # circular mean of the green arc = sweet-spot centre; half-width from spread
        ang = np.radians(green_idx)
        target = math.degrees(math.atan2(np.sin(ang).mean(), np.cos(ang).mean())) % 360
        half = max(abs(wrap180(a - target)) for a in green_idx)
        needle = float(np.argmax(ws))
        now = time.time()
        if self.prev is not None:
            pa, pt = self.prev
            dt = max(now - pt, 1e-3)
            omega = wrap180(needle - pa) / dt
            predicted = needle + omega * self.cfg["ring_latency"]
            if (abs(wrap180(predicted - target)) <= half * self.cfg["ring_tolerance"]
                    and now - self.last_press > 1.0):
                act(self.cfg["ring_key"])
                self.last_press = now
                print(f"[ring] pressed needle={needle:.0f} target={target:.0f}")
        self.prev = (needle, now)


# ───────────────────────────── main loop ─────────────────────────────
def on_key(k):
    global running, quit_flag
    if k == keyboard.Key.f8:
        running = not running
        print("RUNNING" if running else "PAUSED")
    elif k == keyboard.Key.f9:
        quit_flag = True
        return False


def run():
    cfg = load_config()
    need = {"lane", "hit_zone", "freq_wave", "freq_track", "ring"}
    if not need <= set(cfg["regions"]):
        sys.exit("Missing regions - run: python minigame_bot.py calibrate")

    rhythm, ring = Rhythm(cfg), Ring(cfg)
    keyboard.Listener(on_press=on_key).start()
    print("Ready. F8 = start/pause, F9 = quit.")
    frame = 1 / cfg["fps"]

    with mss.mss() as sct:
        while not quit_flag:
            t0 = time.time()
            if running:
                if waveform_present(grab(sct, cfg["regions"]["freq_wave"])):
                    print("[state] FREQUENCY")
                    solve_frequency(sct, cfg)
                else:
                    ring_img = grab(sct, cfg["regions"]["ring"])
                    if ring.active(ring_img):
                        ring.step(ring_img)
                    elif rhythm.lane_visible(sct):
                        rhythm.step(sct)
                    else:
                        rhythm.baseline = None
                        ring.prev = None
            time.sleep(max(0, frame - (time.time() - t0)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "calibrate":
        calibrate()
    else:
        run()
