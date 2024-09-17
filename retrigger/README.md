# retrigger

Track action that retriggers the currently playing clip. Fun if you have a momentary button to control the global quantize.

Usage: `"my track" / RETRIGGER`

If used on a track that isn't playing, will attempt to fire my action [PLAYNEXT](https://github.com/odisfm/clyph-x-actions/tree/main/play_next), which by default will fire the first clip of the target track. If you don't have that action installed, it won't error.