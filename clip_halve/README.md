# halve

Clip action that takes an existing (or recording<sup>†</sup>) clip and changes the loop markers so that only the left or right half plays. Can be used repeatedly.

## usage

#### `USER_CLIP HALVE` `<` or `>` or `RESET` (see below).

__The results of this action are only audible according to the clip update rate set in Preferences > Record, Warp & Launch. Recommended setting is 1/16 or 1/32.__

Applies to the playing (or recording), clip on the targeted track. Applies to the selected clip if none is playing. Applies to the selected track if none specified. Can be applied to specific clips with `USER_CLIP(<scene number of clip>) HALVE`.

### `reset`

The Live API does not provide a practical way to determine the original length of a recorded clip. Calling `USER_CLIP HALVE_RESET` will set the clip's Loop Start to 1.1.1 and the Loop End to a default value of 9.1.1 (8 bars long).

The default value can be changed by setting the variable at the top of the file:

`DEFAULT_CLIP_LENGTH_BARS = 8`

_Note that calling this action on a clip shorter than this value will still result in an 8 bar clip, meaning on a 4 bar clip you will have 4 bars of silence at the end._

### <sup>†</sup> calling during recording

Calling on a recording clip will have different behaviour based on whether it is an audio or MIDI clip, as well as how far into the recording you are (based on the aforementioned `DEFAULT_CLIP_LENGTH_BARS`).

_The following example assumes a default value of 8 bars._

As the clip loop braces can't be changed on a still-recording clip, a callback will be registered to execute when the recording is complete. If you trigger `USER_CLIP HALVE <` before bar 5 of the recording, the clip will be retriggered* (while continuing to record), and immediately after launching, the clip will be halved<sup>1</sup>. This behaviour doesn't apply to overdubbing MIDI clips, which are changed instantly.

__*This will happen according to your set's global quantization value, meaning it only really works properly if that is set to 4 bars. (if you triggered the action between the start of bar 3 and end of bar 4, a GQ of 2 bars would work).__

Using `USER_CLIP HALVE >` in the second half of the recording _on an audio clip_ will result in the action triggering a short time after the clip starts playing back.

The length of this delay is the Live Clip Update Rate + ~200ms <sup>3</sup>, meaning you will hear the first half of your clip for this amount of time before the second half starts playing. This is particularly noticeable if the first and second halves of the clip start on different pitches. The clip will, however, remain in time. A Clip Update Rate of 1/16 or 1/32 is recommended for this reason.

<sup>1</sup> Often, this retriggering will mean the clip actually _doesn't_ need halving, but the action will determine that automatically. Note: When triggering a fixed-length record on a MIDI track via Ableton Push, Live creates a blank MIDI clip of your selected length and starts overdubbing it. This means the retriggering behaviour does not apply, and the action happens instantly. It also means that calling `USER_CLIP HALVE >` in the first half of recording will produce undesired effects.

<sup>2</sup> If the callback is not working, or working unreliably, try increasing `CALLBACK_WAIT_TIME` near the top of the file. Works in increments of 100 milliseconds.