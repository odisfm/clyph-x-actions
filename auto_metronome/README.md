# autometro

Select a track — when it starts playing, turn off the metronome. When it stops, turn the metronome back on. __Only for session view clips.__

## usage
At the top of __auto_metronome.py__ you will find several variables:

#### `KEY_TRACK = None`
Set this to the name of the track you want to monitor, e.g. `'drums'`. Can be left as `None` if you want to set the track manually.

#### `ON_AT_LOAD = True`
Set this to `False` to only enable the action when you explicitly call it (see below).

#### `ONLY_TURN_OFF = False`
Set this to `True` and the metronome will turn off when the key track starts playing, but will __not__ turn back on when the track stops.

#### `ONLY_TURN_ON = False`
Inverse of the above.

### actions
#### `AUTOMETRO` `ON` or `OFF`
You can temporarily disable the action until you turn it back on again. Calling just `AUTOMETRO` with no arguments will toggle the status. 
#### `AUTOMETRO "<track name>"`
Set the name of the track to listen to. Double-quotes are mandatory.

__Note:__ Variables set this way will __not__ persist upon reloading the Live set  — they will be set to the values defined in `KEY_TRACK` and `ON_AT_LOAD`.