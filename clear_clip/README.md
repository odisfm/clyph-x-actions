# clearclip

Clip action that deletes the targeted clip, only if it's not playing. Will delete a playing clip if called with argument `FORCE`.

By default targets the playing clip on the selected track, but functions just like a native clip action in that it can be applied to specific tracks, specific clips, or ranges. (See ClyphX Pro User Manual).

As with all user clip actions, it must be called as below:

`USER_CLIP CLEARCLIP`

`USER_CLIP(1) CLEARCLIP` (first clip on selected track)

`"bass gtr" / USER_CLIP CLEARCLIP` (playing clip or selected clip on track called "bass gtr")

Also includes a helper action, `CLEARCLIPPROMPT`. This does nothing but indicate what the main action will do when triggered by displaying a message in the Live UI and on a Push 1 or 2†. Useful if using G-Controls.

Here's an example G-Control definition:

```
MY_BUTTON = NOTE, 1, 36, 127, 0, FALSE
MY_BUTTON RELEASED_IMMEDIATELY = USER_CLIP(SEL) CLEARCLIPPROMPT
MY_BUTTON PRESSED_DELAYED = USER_CLIP(SEL) CLEARCLIP
```

† _only if using Push 2 with legacy control surface script, I believe it's not possible with Push 3. Push 1 and 2 must both be in 'Live' mode (not 'User' mode)_