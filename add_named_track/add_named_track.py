# made by odis :)
# https://github.com/odisfm/clyph-x-actions

import traceback

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


class add_named_track(UserActionsBase):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)

    def create_actions(self):
        self.add_global_action('addaudion', self.add_named_audio_track)
        self.add_global_action('addmidin', self.add_named_midi_track)

    def add_named_audio_track(self, action_def, args):
        self.add_named_track('audio', args)

    def add_named_midi_track(self, action_def, args):
        self.add_named_track('midi', args)

    def add_named_return_track(self, action_def, args):
        self.add_named_track('return', args)

    def add_named_track(self, track_type: str, args: str):
        try:
            _args = args.split('"')

            if len(_args) == 1:
                raise ValueError(f'Invalid format: track name must be enclosed in quotes')

            track_name = _args[1]

            if len(_args) == 3:
                index_def = _args[2]
                if index_def:
                    try:
                        index = int(index_def)
                        if index > 0:
                            index -= 1

                    except ValueError:
                        selected_index = self.get_selected_track_index()
                        if index_def == ' <':
                            index = selected_index
                        elif index_def == ' >':
                            index = selected_index +1
                        else:
                            raise ValueError(f'Invalid format used: addtrackn {args}')
                else:
                    index = self.get_selected_track_index() + 1

            else:
                index = self.get_selected_track_index() + 1

            self.canonical_parent.log_message(f'creating {track_type} track called "{track_name}" with index {index}')

            if track_type == 'audio':
                track = self._song.create_audio_track(Index=index)
            elif track_type == 'midi':
                track = self._song.create_midi_track(Index=index)
            else:
                raise ValueError(f'unknown track type `{track_type}')

            track.name = track_name

        except:
            self.canonical_parent.log_message(traceback.format_exc())
            self.canonical_parent.log_message(f'args: `{args}')

    def get_selected_track_index(self):
        return list(self._song.tracks).index(self._song.view.selected_track)
