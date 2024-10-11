# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

LOGGING_LEVEL = 'critical'

KEY_TRACK = None

ON_AT_LOAD = True
ONLY_TURN_OFF = False
ONLY_TURN_ON = False

class auto_metronome(UserActionsBase):

    ### boilerplate

    def log(self, message, critical = False):
        if LOGGING_LEVEL is not 'all' and not critical:
            return
        if critical:
            message = 'CRITICAL: ' + message
        self.canonical_parent.log_message(f'{self.__class__.__name__.upper()}: {message}')

    def msg(self, message):
        self.canonical_parent.show_message(f'{self.__class__.__name__.upper()}: {message}')

    def cxp_action(self, action_list):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_list)

        ### extras

    def get_selected_track(self):
        return self._song.view.selected_track

    def get_selected_scene_index(self):
        return list(self._song.scenes).index(self._song.view.selected_scene)

    def get_track_by_name(self, search_name):
        for track in list(self._song.tracks):
            if track.name == search_name:
                return track
        self.log('no track matching search term!', critical=True)
        return False

    def pushmsg(self, message, class_label = False):
        if not class_label:
            self.cxp_action(f'PUSH MSG "{message}"')
        else:
            self.cxp_action(f'PUSH MSG "{self.__class__.__name__.upper()}: {message}"')

    def shout(self, message, critical = False, class_label = False):
        self.log(message, critical)
        self.msg(message)
        self.pushmsg(message, class_label)

    ### end boilerplate

    def create_actions(self):
        self.add_global_action('autometro', self.auto_metronome)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._song.add_current_song_time_listener(self.set_load_wait)

    def set_load_wait(self):
        if self._song.current_song_time_has_listener:
            self._song.remove_current_song_time_listener(self.set_load_wait)
        self.on_status = ON_AT_LOAD
        self.assign_track(KEY_TRACK)
        if ONLY_TURN_ON and ONLY_TURN_OFF:
            self.log(f'"ONLY_TURN_OFF = True and ONLY_TURN_ON = True" are incompatible! Disabling both', critical=True)

    def assign_track(self, track_name):
        if track_name == None:
            return
        new_track = self.get_track_by_name(track_name)
        if new_track is False:
            self.shout('no track by that name!')
            return
        self.key_track = new_track
        new_track.add_playing_slot_index_listener(self.key_track_callback)
        self.key_track_callback()

    def auto_metronome(self, action_def, args):
        self.log('running')
        self.log(args)
        if args == '':
            if self.on_status == True:
                status_string = 'off'
            else:
                status_string = 'on'
            self.on_status = not self.on_status
            self.shout(f'toggled autometro {status_string}')
            return
        args = args.split('"')
        if args[0] == 'on':
            self.on_status = True
            return
        elif args[0] == 'off':
            self.on_status = False
            return
        if len(args) > 1:
            new_track = args[1]
        else:
            new_track = args[0]
        self.assign_track(new_track)

    def key_track_callback(self):
        if self.on_status is False:
            return
        if self.key_track.playing_slot_index >= 0:
            if ONLY_TURN_ON:
                return
            self.log('key track is playing')
            self.cxp_action('WAIT 1; METRO OFF')
        else:
            if ONLY_TURN_OFF:
                return
            self.log('key track is not playing')
            self.cxp_action('WAIT 1; METRO ON')