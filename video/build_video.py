"""Build the narrated exposition video from frames/ and narration.py.

Steps: TTS each sentence (edge-tts) -> decode to WAV -> assemble one track with
pauses -> draw subtitles onto slide frames -> concat stills + audio with ffmpeg.
"""
import asyncio
import os
import subprocess
import wave

import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

from narration import SLIDES

VOICE = "en-US-AndrewNeural"
RATE = "-4%"
SR = 24000
LEAD, GAP, TAIL = 0.5, 0.35, 0.9
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(HERE, "tts")
SEG_DIR = os.path.join(HERE, "segments")
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 40)


def sentences():
    for si, slide in enumerate(SLIDES, 1):
        for ki, s in enumerate(slide, 1):
            sub, spoken = (s, s) if isinstance(s, str) else s
            yield si, ki, sub, spoken


async def tts_all():
    os.makedirs(TTS_DIR, exist_ok=True)
    sem = asyncio.Semaphore(2)

    async def one(si, ki, spoken):
        mp3 = os.path.join(TTS_DIR, f"{si:02d}_{ki:02d}.mp3")
        if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            return
        async with sem:
            for attempt in range(6):
                try:
                    await edge_tts.Communicate(spoken, VOICE, rate=RATE).save(mp3 + ".part")
                    break
                except edge_tts.exceptions.NoAudioReceived:
                    if attempt == 5:
                        raise RuntimeError(f"TTS failed for {si:02d}_{ki:02d}: {spoken!r}")
                    await asyncio.sleep(3 * (attempt + 1))
        os.replace(mp3 + ".part", mp3)

    await asyncio.gather(*(one(si, ki, sp) for si, ki, _, sp in sentences()))


def decode(mp3):
    wav = mp3[:-4] + ".wav"
    if not os.path.exists(wav):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", str(SR),
                        "-sample_fmt", "s16", wav], check=True)
    with wave.open(wav) as w:
        return w.readframes(w.getnframes())


def wrap(text, width=1760):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if FONT.getlength(trial) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def subtitle_frame(slide_png, text, out_png):
    im = Image.open(slide_png).convert("RGB")
    if text:
        d = ImageDraw.Draw(im)
        lines = wrap(text)
        lh = 50
        top = 1080 - 132 + (132 - lh * len(lines)) // 2 - 4
        # The title slide is plain, so draw the band everywhere; grow it for 3+ lines.
        d.rectangle([0, min(top - 10, 1080 - 132), 1920, 1080], fill=(27, 42, 65))
        for i, line in enumerate(lines):
            x = (1920 - FONT.getlength(line)) / 2
            d.text((x, top + i * lh), line, font=FONT, fill=(255, 255, 255),
                   stroke_width=2, stroke_fill=(10, 18, 30))
    im.save(out_png)


def main():
    asyncio.run(tts_all())
    os.makedirs(SEG_DIR, exist_ok=True)
    silence = lambda sec: b"\x00\x00" * int(SR * sec)
    audio = bytearray()
    concat = ["ffconcat version 1.0"]
    srt, n = [], 0
    t = 0.0

    def add_still(png, dur):
        concat.append(f"file '{png.replace(os.sep, '/')}'")
        concat.append(f"duration {dur:.3f}")

    for si, slide in enumerate(SLIDES, 1):
        frame = os.path.join(HERE, "frames", f"s{si:02d}.png")
        audio += silence(LEAD)
        add_still(frame, LEAD)
        t += LEAD
        for ki, s in enumerate(slide, 1):
            sub = s if isinstance(s, str) else s[0]
            pcm = decode(os.path.join(TTS_DIR, f"{si:02d}_{ki:02d}.mp3"))
            dur = len(pcm) / 2 / SR
            pause = GAP if ki < len(slide) else TAIL
            audio += pcm + silence(pause)
            png = os.path.join(SEG_DIR, f"{si:02d}_{ki:02d}.png")
            subtitle_frame(frame, sub, png)
            add_still(png, dur + pause)
            n += 1
            srt.append((n, t, t + dur, sub))
            t += dur + pause
    concat.append(f"file '{concat[-2].split(chr(39))[1]}'")  # concat demuxer needs the last file twice

    with wave.open(os.path.join(HERE, "narration.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(audio))
    with open(os.path.join(HERE, "stills.ffconcat"), "w", encoding="utf-8") as f:
        f.write("\n".join(concat) + "\n")

    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

    with open(os.path.join(HERE, "ns_exposition_video.srt"), "w", encoding="utf-8") as f:
        for i, a, b, s in srt:
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n")

    out = os.path.join(HERE, "ns_exposition_video.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(HERE, "stills.ffconcat"), "-i", os.path.join(HERE, "narration.wav"),
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
                    "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                    out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    print(f"sentences={n} duration={t / 60:.2f} min -> {out}")


if __name__ == "__main__":
    main()
