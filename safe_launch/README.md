# safelaunch

Launches a scene, only if it isn't empty. Shouts at you<sup>1</sup> if you try to launch an empty scene.

## usage
`SAFELAUNCH <scene number>`\
`SAFELAUNCH SEL` launch the selected scene\
`SAFELAUNCH NEXT` launch the scene below the selected scene

### checking within a range of tracks

Optionally, you can specify a range of tracks, and only those tracks will be considered when determining if a scene is empty: at least one clip must be present on a track within this range for the scene to launch.

You can specify this range in two ways:

#### globally in safe_launch.py

Near the top are the variables `FIRST_TRACK` and `LAST TRACK`, set to `None` by default. Change these to the names of your tracks, or leave them as `None`.

#### as arguments to the action

You can set the first or the first __and__ last tracks to consider when calling the action like `SCENELAUNCH SEL "drums" "keys"`. Double-quotes are mandatory (specifying tracks by number is not supported). Only specifying the first track will leave the last track as the value defined in __safe_launch.py__.

### select scene after launching
The flag `SELECT_AFTER_LAUNCHING` near the top of __safe_launch.py__ can be set to `True` to select a successfully launched scene. Redundant if you have 'Select On Launch' enabled in Live's preferences.
#

<sup>1</sup> Shows an error in the Live UI, in the log, and on a connected Push 1 or Push 2. Push 2 in Live 12+ only supported if used with the legacy control surface script.