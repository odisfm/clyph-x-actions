# halve

Clip action that takes an existing (or recording<sup>1, 3</sup>) clip and changes the loop markers so that only the left or right half plays. Can be used repeatedly.

Usage: `USER_CLIP HALVE` `<` or `>` or `RESET` (see below).

Applies to the playing (or recording), clip on the targeted track. Applies to the selected clip if none is playing. Applies to the selected track if none specified. Can be applied to specific clips with `USER_CLIP(<scene number of clip>) HALVE`.

### reset

The Live API does not provide a practical way to determine the original length of a recorded clip. Calling `USER_CLIP HALVE_RESET` will set the clip's Loop Start to 1.1.1 and the Loop End to a default value of 9.1.1 (8 bars long).

The default value can be changed by setting the variable at the top of the file:

`DEFAULT_CLIP_LENGTH_BARS = 8`

_Note that calling this action on a clip shorter than this value will still result in an 8 bar clip, meaning on a 4 bar clip you will have 4 bars of silence at the end._

#### <sup>1</sup> calling during recording

Calling on a recording clip will have different behaviour based on whether it is an audio or MIDI clip, as well as how far into the recording you are (based on the aforementioned `DEFAULT_CLIP_LENGTH_BARS`).

_The following example assumes a default value of `8` bars._

As the clip loop braces can't be changed on a still-recording clip, a callback will be registered when the recording is complete. If you trigger `USER_CLIP HALVE <` before bar 5 of the recording, the clip will be re-triggered (while still recording), and shortly after firing, the clip will be halved<sup>2</sup>. __This will happen according to your set's global quantization value, meaning it only really works properly if that is set to 4 bars. (if you triggered the action between the start of bar 3 and end of bar 4, a GQ of 2 bars would work).__


This slight delay means that calling `USER_CLIP HALVE >` on a recording clip will result in you hearing a short portion (~100ms <sup>3</sup>) of the first half of your clip before the second half starts playing. This is particularly noticeable if the first and second halves of the clip start on different pitches. The clip will, however, remain in time.

__Note:__ When triggering a fixed-length MIDI recording from Ableton Push, Live actually pre-creates a clip according to the fixed-length setting. This means that calling `USER_CLIP HALVE >` in the first half of recording will produce undesired effects.

<sup>2</sup> Often, this re-triggering will mean the clip actually _doesn't_ need halving, but the action will determine that automatically.

<sup>3</sup> If the callback is not working on working unreliably, try increasing `CALLBACK_WAIT_TIME` near the top of the file. Works in increments of 100 milliseconds.