# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

class armex(UserActionsBase):

    ### bolierplate

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.logging_level = 'critical'

    def get_selected_scene_index(self):
        return list(self._song.scenes).index(self._song.view.selected_scene)
    
    def log(self, message, critical = False):
        if self.logging_level != 'all' and critical == False:
            return
        if critical:
            message = 'CRITICAL: ' + message
        self.canonical_parent.log_message(f'{self.__class__.__name__.upper()}: {message}')

    def msg(self, message):
        self.canonical_parent.show_message(f'{self.__class__.__name__.upper()}: {message}')

    def pushmsg(self, message, class_label = False):
        if not class_label:
            self.cxp_action(f'PUSH MSG "{message}"')
        else:
            self.cxp_action(f'PUSH MSG "{self.__class__.__name__.upper()}: {message}"')

    def cxp_action(self, action_list):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_list)

    ### end boilerplate

    def create_actions(self):
        self.add_track_action('armex', self.arm_exclusive)
        self.add_global_action('armexshift', self.handle_shift)
        self.shifted = False

    def arm_exclusive(self, action_def, args):
        target = action_def["track"]
        if self.shifted == False:
            tracklist = list(self.song().tracks)

            for track in tracklist:
                if track.name != target.name and track.can_be_armed == True:
                    track.arm = False
                if track.name == target.name and track.can_be_armed == True:
                    track.arm = True

        elif self.shifted == True:
            target.arm = not target.arm
       
    def handle_shift(self, action_def, args):
        if args == 'on':
            self.shifted = True
        elif args == 'off':
            self.shifted = False
        else:
            self.log('invalid argument', critical=True)
            return