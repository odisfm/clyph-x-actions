# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
 
class retrigger(UserActionsBase):

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

    ### end boilerplate

    def create_actions(self):
        self.add_track_action('retrigger', self.retrigger)

    def retrigger(self, action_def, args):
        target = action_def["track"]
        if target.playing_slot_index < 0:
            error = f'{target.name} has no playing clip!'
            self.log(error, critical = True)
            self.pushmsg(error)
            self.cxp_action(f'"{target.name}" / PLAYNEXT')
            return
        clip_slot = target.clip_slots[target.playing_slot_index]
        clip_slot.fire()
        clip_index = list(target.clip_slots).index(clip_slot)
        message = f'Retriggered {target.name} clip {clip_index + 1}'
        self.log(message)
        self.pushmsg(message)