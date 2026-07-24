"""
Background Music Generator & Manager
-------------------------------------
Provides background music tracks for video rendering.
Generates procedural ambient background tracks using FFmpeg if local MP3/WAV files are missing.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

STORAGE_MUSIC = Path(__file__).parent.parent.parent.parent / "storage" / "music"


class MusicManager:
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg = ffmpeg_path
        STORAGE_MUSIC.mkdir(parents=True, exist_ok=True)

    def get_music_track(self, preset: str = "ambient", duration: float = 60.0) -> str:
        """Returns the file path to a background music track for the given preset."""
        preset_clean = (preset or "none").lower()
        if preset_clean in ["none", "", "off"]:
            return ""

        track_path = STORAGE_MUSIC / f"{preset_clean}.wav"
        if track_path.exists():
            return str(track_path)

        # Generate a procedural ambient audio track using FFmpeg synthesis
        try:
            self._generate_procedural_track(preset_clean, str(track_path), duration)
            return str(track_path)
        except Exception:
            return ""

    def _generate_procedural_track(self, preset: str, output_path: str, duration: float):
        """Generates a pleasant procedural background audio track using FFmpeg lavfi."""
        dur_str = str(max(10, int(duration)))

        if preset == "cinematic":
            # Deep atmospheric synth pad
            filter_str = f"sine=f=110:r=44100[s1];sine=f=164.81:r=44100[s2];sine=f=220:r=44100[s3];[s1][s2][s3]amix=inputs=3,volume=0.1,lowpass=f=400,afade=t=in:ss=0:d=2,afade=t=out:st={int(duration)-2}:d=2"
        elif preset == "lofi":
            # Chill warm tone pad
            filter_str = f"sine=f=130.81:r=44100[s1];sine=f=196.00:r=44100[s2];[s1][s2]amix=inputs=2,volume=0.08,lowpass=f=600,afade=t=in:ss=0:d=2,afade=t=out:st={int(duration)-2}:d=2"
        elif preset == "dramatic":
            # Deep low bass resonance
            filter_str = f"sine=f=55:r=44100[s1];sine=f=82.41:r=44100[s2];[s1][s2]amix=inputs=2,volume=0.12,lowpass=f=300,afade=t=in:ss=0:d=1,afade=t=out:st={int(duration)-2}:d=2"
        elif preset == "upbeat":
            # Warm rhythmic synth pulse
            filter_str = f"sine=f=261.63:r=44100[s1];sine=f=329.63:r=44100[s2];[s1][s2]amix=inputs=2,volume=0.07,afade=t=in:ss=0:d=1,afade=t=out:st={int(duration)-2}:d=2"
        else:
            # Ambient pad (default)
            filter_str = f"sine=f=146.83:r=44100[s1];sine=f=220.00:r=44100[s2];[s1][s2]amix=inputs=2,volume=0.08,lowpass=f=500,afade=t=in:ss=0:d=2,afade=t=out:st={int(duration)-2}:d=2"

        cmd = [
            self.ffmpeg, "-y",
            "-f", "lavfi",
            "-i", filter_str,
            "-t", dur_str,
            "-c:a", "pcm_s16le",
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=False)
