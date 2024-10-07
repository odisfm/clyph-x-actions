# lpr

Track action that exposes functions for the Looper device that were added to the Live API in version 12.0.5. Targets the first Looper device on the specified track.

Usage: `LPR <specific function>`

The functions available are listed in [the Live Object Model documentation](https://docs.cycling74.com/max8/vignettes/live_object_model#live_obj_anchor_LooperDevice) under LooperDevice.

All exposed functions are available for use in ClyphX Pro, with some caveats:

* `export_to_clip_slot` requires Live 12.1 or above. See below for usage
* functions named with underscores like `half_length` should be called with no underscores (all one word)
* `overdub_after_record` is called like `LPR DUBAFTER <MODE>` (where `<MODE>` is `ON`, `OFF`, or omitted to toggle the state)
* the record length is called like `LPR BARS <LENGTH>` (where `<LENGTH>` is any number of bars available in the UI, as well as `X`)

### Available functions

* `LPR RECORD`
* `LPR CLEAR`
* `LPR HALFSPEED`
* `LPR DOUBLESPEED`
* `LPR HALFLENGTH`
* `LPR DOUBLELENGTH`
* `LPR OVERDUB`
* `LPR PLAY`
* `LPR STOP`
* `LPR UNDO`
* `LPR BARS <LENGTH>`\
sets the record length, where `<LENGTH>` is any number of bars available in the UI, as well as `X`
* `LPR DUBAFTER <MODE>`\
where `<MODE>` is `ON`, `OFF`, or omitted to toggle the state
* `LPR EXPORT <TRACK> <SLOT NUMBER>`\
where `<TRACK>` is `SEL` for the selected track, `SELF` for the track containing the Looper, or any track name in double-quotes. `<SLOT NUMBER>` may be any valid scene number or `SEL` for the selected scene. The variable `EXPORT_MATCH_TRACK_COLOUR` at the top of __looper.py__ determines whether the new clip's colour will be set to that of the destination track 