export type VideoType = 'ranking' | 'review' | 'explainer' | 'shorts' | 'documentary' | 'educational';
export type StageType = 'script' | 'voice' | 'subtitles' | 'media' | 'render';
export type StageStatus = 'pending' | 'running' | 'done' | 'error' | 'skipped';

export interface PipelineStage {
  id: string;
  project_id: string;
  stage: StageType;
  status: StageStatus;
  progress: number;
  result_path?: string;
  error_msg?: string;
  log?: string;
  started_at?: string;
  completed_at?: string;
}

export interface ProjectSettings {
  duration?: string;
  aspect_ratio?: string;
  voice?: string;
  subtitle_style?: string;
  bg_music?: string;
}

export interface Project {
  id: string;
  title: string;
  video_type: VideoType;
  status: StageStatus;
  topic: string;
  script?: string;
  settings: ProjectSettings;
  thumbnail_path?: string;
  output_path?: string;
  created_at: string;
  updated_at: string;
  stages: PipelineStage[];
}

export interface ProjectCreate {
  title: string;
  video_type: VideoType;
  topic: string;
  settings: ProjectSettings;
}

export interface SystemCheck {
  ffmpeg: boolean;
  gpu: boolean;
  gpu_name?: string;
  kokoro: boolean;
  edge_tts: boolean;
  whisper: boolean;
  ollama: boolean;
  pexels_key: boolean;
  pixabay_key: boolean;
  first_run: boolean;
}
