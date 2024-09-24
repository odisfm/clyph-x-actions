# macset, macinc, macrandom

Three device actions for interacting with the macro variation feature on Audio Effect, MIDI, and Instrument Racks.

__Note:__ ClyphX requires all user device actions to be prefixed with `USER_DEV`. This allows targeting specific devices with the syntax `USER_DEV("my arpeggiator") MACRANDOM`. 

### `USER_DEV MACSET` `<number of macro variation>` or `RND`

When calling `USER_DEV MACSET 3`, macro variation 3 on the targeted device will be selected and then instantly recalled. This is equivalent to the native ClyphX action list `DEV VAR 3; DEVVARRECALL`.

Calling `USER_DEV MACSET RND` will recall a random variation, other than the one currently selected<sup>1</sup>.

### `USER_DEV MACINC` `<` or `>`

Selects and recalls the previous or next variation, relative to the one currently selected<sup>1</sup>. Calling `USER_DEV MACINC <` when the first variation is selected will wrap around and recall the last one, and `USER_DEV MACINC >` will wrap to the first when the last is selected.

### `USER_DEV MACRANDOM`

Calls the native Live macro randomization feature.

ClyphX includes a native action `DEV RND`, which will randomise the parameters of any device. However, it does not respect the rack feature 'Exclude Macro from Randomization' (available when right-clicking a macro knob). This action does.
#

<sup>1</sup> Live does not store the currently selected or recalled macro variation when saving the set. This means when loading the set, no variation is selected (obviously the actual controls are how you left them). This has implications for these actions:

Calling `USER_DEV MACINC` on a rack with no selected macro will always recall the first variation.

Calling `USER_DEV MACSET RND` on a rack with no selected macro has a chance to recall the last variation recalled before the set was loaded, resulting in no change to the macro controls.