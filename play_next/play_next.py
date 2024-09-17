from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

FIRST_SCENE = None
LAST_SCENE = None
 
class play_next(UserActionsBase):

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

    def cxp_action(self, action_list):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_list)

    def create_actions(self):
        self.add_track_action('playnext', self.play_next)
       
    def play_next(self, action_def, args):
        self.log('running')
        first_scene = FIRST_SCENE
        last_scene = LAST_SCENE
        if first_scene == None:
            first_scene = 1
        if last_scene == None:
            last_scene = len(list(action_def["track"].clip_slots)) - 1
        args = args.split()
        self.log(args)
        self.log('any' in args)
        target = action_def["track"]
        clip_slots = target.clip_slots
        if target.playing_slot_index >= 0:
            if 'any' not in args:
                first_scene = target.playing_slot_index + 2

        if first_scene > last_scene:
            self.log('next clip out of range')
            return


        for i in range(first_scene - 1, last_scene + 1):
            if not clip_slots[i].has_clip:
                continue
            else:
                clip_slots[i].fire()
                return

        message = f'no valid clip!'
        self.msg(message)
        self.log(message, critical=True)
        self.pushmsg(message)

        self.log('finished')





         
    