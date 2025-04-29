# add_named_track

A global action to create an audio or MIDI track with a specified name, and optionally a position.

## Usage

`ADDAUDION "my audio track"`

Creates an audio track called `my audio track` to the right of the currently selected track.

`ADDMIDIN "my midi track" 3`

Creates a MIDI track called `my MIDI track` as track number 3.

`ADDMIDIN "my midi track" <` or `>`

Creates a MIDI track to the left or right of the currently selected track.

`ADDAUDION "my audio track" -1`

Creates an audio track at the end of the track list.

## Notes

- All formats are allowed for both audio and MIDI tracks
- Track name must always be specified
- Track name must always be enclosed in double-quotes
- Supports emojis 🥸
