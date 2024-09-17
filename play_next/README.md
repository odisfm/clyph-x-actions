# playnext

Track action that fires the next clip below the currently playing clip, or the first clip if none is playing.

Usage: `"my track" / PLAYNEXT`

Variables `FIRST_SCENE` and `LAST SCENE` at the top of the file can be modified so clips only within that range are eligible.

Can also be called like `PLAYNEXT ANY` to fire clips above the currently playing clip (still respects the scene range).