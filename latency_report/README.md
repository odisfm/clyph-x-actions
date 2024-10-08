# latency_report

Global action that checks every device in a Live set, and outputs its latency (in samples and milliseconds) to the log file, from highest to lowest. Searches recursively inside racks.

__Usage:__ `LATENCY`

Example output:
```
vocals | Auto Shift [Auto Shift] | 6144smpl | 128.0ms
cowbell | Spectral Resonator [Spectral Resonator] | 1536smpl | 32.0ms
vocals | catch peaks (inside dynamics rack) [Limiter] | 256smpl | 5.3ms
MAIN/MASTER | fuck my shit up (inside analog warmth) [Erosion] | 240smpl | 5.0ms
MAIN/MASTER | Vinyl Distortion (inside analog warmth) [Vinyl Distortion] | 144smpl | 3.0ms
guitar | Gate [Gate] | 72smpl | 1.5ms
RETURN C-big verb | Gate (inside Audio Effect Rack) [Gate] | 72smpl | 1.5ms
strings | waooow [Corpus] | 64smpl | 1.3ms
drums | Redux (inside Tom Mid) [Redux] | 64smpl | 1.3ms
bass | lo cut [EQ Eight] | 16smpl | 0.3ms
guitar | face melter [Overdrive] | 5smpl | 0.1ms
MAIN/MASTER | Saturator [Saturator] | 3smpl | 0.1ms
```
