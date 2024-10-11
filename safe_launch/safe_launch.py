# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

FIRST_TRACK = None
LAST_TRACK = None

SELECT_AFTER_LAUNCH = False


class safe_launch(UserActionsBase):

    ### boilerplate

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.logging_level = 'critical'

    def log(self, message, critical = False):
        if self.logging_level != 'all' and critical == False:
            return
        if critical:
            message = 'CRITICAL: ' + message
        self.canonical_parent.log_message(f'{self.__class__.__name__.upper()}: {message}')

    def msg(self, message):
        self.canonical_parent.show_message(f'{self.__class__.__name__.upper()}: {message}')

    def cxp_action(self, action_list):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_list)

        ### extras

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
        self.add_global_action('safelaunch', self.safe_launch)

    def safe_launch(self, action_def, args):
        self.log('running')
        arg_scene = args.split(' ')[0]
        if arg_scene == '':
            self.log('must specify scene number, \'NEXT\', or \'SEL\'!', critical=True)
            return
        if arg_scene == 'next':
            scene_index = self.get_selected_scene_index() + 1
        elif arg_scene == 'prev':
            scene_index = self.get_selected_scene_index() - 1
        elif arg_scene == 'sel':
            scene_index = self.get_selected_scene_index()
        else:
            try:
                scene_index = int(arg_scene) - 1
            except:
                self.log('must specify scene number, \'NEXT\', or \'SEL\'!', critical=True)
                return

        if scene_index >= len(list(self._song.scenes)) or scene_index < 0:
            message = f'scene {scene_index + 1} does not exist!'
            self.shout(message)
            return

        first_track = FIRST_TRACK
        last_track = LAST_TRACK

        arg_quotes = args.split('"')

        if len(arg_quotes) >= 2:
            first_track = arg_quotes[1]
            if len(arg_quotes) >= 4:
                last_track = arg_quotes[3]

        scene_has_clip = False

        if first_track == None:
            started = True
        else:
            started = False

        self.log(f'checking tracks between {first_track} and {last_track}')

        for track in self._song.tracks:
            self.log(f'checking track {track.name}')
            if track.name == first_track:
                started = True
            if not started:
                continue
            if track.clip_slots[scene_index].has_clip:
                scene_has_clip = True
                break
            if track.name == last_track:
                break

        if not scene_has_clip:
            message = f'Can\'t launch empty scene! ({scene_index + 1})'
            self.shout(message, critical=True)
            return
        else:
            self._song.scenes[scene_index].fire()
            if SELECT_AFTER_LAUNCH:
                self._song.view.selected_scene = self._song.scenes[scene_index]