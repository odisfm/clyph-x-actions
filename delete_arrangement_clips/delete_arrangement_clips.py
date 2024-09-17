from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
 
class delete_arrangement_clips(UserActionsBase):

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
        self.add_global_action('delarrclips', self.delarrclips)

    def delarrclips(self, action_def, args):
        self.log('running', critical=True)
        tracklist = list(self._song.tracks)
        for track in tracklist:
            self.log(f'starting {track.name}')
            if track.clip_slots[0].is_group_slot:
                continue
            arrangement_clips = list(track.arrangement_clips)
            self.log('beginning loop')
            for clip in arrangement_clips:
                self.log('attempting delete')
                track.delete_clip(clip)
            self.log(f'finished track {track.name}')

        self.log('finished', critical=True)