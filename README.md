# Vivara 🎬

> **The free, open-source, locally-run AI video studio.**  
> Built as an AI Creator Studio workflow platform with modular node pipeline execution.

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![React](https://img.shields.io/badge/React-18-61dafb.svg)

---

## ✨ Key Features

| Feature | Status |
|---|---|
| **OmniRoute AI Gateway** (Universal LLM Provider Layer) | ✅ Integrated |
| **Workflow Platforms** (Top 10 Rankings, Reviews, Explainers, Shorts, Documentaries, News, Podcasts) | ✅ Live |
| **Modular DAG Node Execution Graph** | ✅ Live |
| **5 Voice / TTS Engines** (Kokoro-82M, Edge-TTS, Google Translate TTS, ElevenLabs, OpenAI Speech) | ✅ Live |
| **Stock Media Search** (Openverse/Wikimedia [No Key Required!], Pexels, Pixabay, Unsplash) | ✅ Live |
| **Clip Intelligence Studio** (Podcast repurposing, silence removal, scene cut detection, viral highlights) | ✅ Live |
| **FFmpeg Rendering** with NVENC GPU Acceleration | ✅ Live |
| **Project Management** (Rename, Duplicate, Edit Script, Delete, Direct MP4 Download) | ✅ Live |

---

## 🚀 Quick Start (Windows)

### Prerequisites

1. **Python 3.10+** — https://python.org/downloads  
2. **Node.js 18+** — https://nodejs.org  
3. **FFmpeg** — `winget install ffmpeg` or https://ffmpeg.org/download.html  

### Setup & Launch

```powershell
# Clone the repository
git clone https://github.com/vivekmarathe2004/Vivara.git
cd Vivara

# Run the batch launcher (installs all dependencies & starts servers)
.\start.bat
```

The app will open at **http://localhost:5173**.

---

## 📁 Repository Architecture

```
Vivara/
├── backend/          # Python FastAPI backend
│   ├── api/          # Projects, Generate, Settings, Setup, Clip routers
│   ├── services/     # OmniRoute LLM, Kokoro/Edge/gTTS/ElevenLabs/OpenAI TTS, Whisper, Media, FFmpeg
│   ├── models/       # SQLAlchemy ORM
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # App entry point
├── frontend/         # React 18 + Vite + Tailwind CSS v3
│   └── src/
│       ├── pages/    # Dashboard, NewProject, ProjectDetail, ClipMode, Settings, SetupWizard
│       ├── components/
│       ├── api/      # Backend API wrappers
│       └── store/    # Zustand state
├── storage/          # Runtime data (gitignored)
└── start.bat         # Windows launcher script
```

---

## 📄 License

MIT — free forever.
