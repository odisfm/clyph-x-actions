# looper

Exposes actions for the Looper device that were added to the Live API in version 12.0.5.

Syntax is `USER_DEV LPR <specific function>`

The functions available are listed in [the Live Object Model documentation](https://docs.cycling74.com/max8/vignettes/live_object_model#live_obj_anchor_LooperDevice) under LooperDevice.

All exposed functions are available for use in ClyphX Pro, with some caveats:

* didn't implement `export_to_clip_slot`, I may later
* functions named with underscores like `half_length` should be called with no underscores (all one word)
* `overdub_after_record` is called like `USER_DEV LPR DUBAFTER <MODE>` (where \<MODE> is `ON`, `OFF`, or omitted to toggle the state)
* the record length is called like `USER_DEV LPR BARS <LENGTH>` (where \<LENGTH> is any number of bars available in the UI, as well as 'X')

### Available functions

* `USER_DEV LPR RECORD`
* `USER_DEV LPR CLEAR`
* `USER_DEV LPR HALFSPEED`
* `USER_DEV LPR DOUBLESPEED`
* `USER_DEV LPR HALFLENGTH`
* `USER_DEV LPR DOUBLELENGTH`
* `USER_DEV LPR OVERDUB`
* `USER_DEV LPR PLAY`
* `USER_DEV LPR STOP`
* `USER_DEV LPR UNDO`
* `USER_DEV LPR BARS <LENGTH>` (sets the record length, where \<LENGTH> is any number of bars available in the UI, as well as 'X')
* `USER_DEV LPR DUBAFTER <MODE>` (where \<MODE> is `ON`, `OFF`, or omitted to toggle the state)