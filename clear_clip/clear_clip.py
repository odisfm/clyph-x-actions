# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
 
class clear_clip(UserActionsBase):

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
        self.add_clip_action('clearclip', self.clear_clip)
        self.add_clip_action('clearclipprompt', self.prompt)
       
    def clear_clip(self, action_def, args):
        self.log('running')
        target = action_def["clip"]
        parent_slot = target.canonical_parent
        target_index = list(parent_slot.canonical_parent.clip_slots).index(parent_slot)

        if parent_slot.is_playing and args != 'force':
            message = f'{parent_slot.canonical_parent.name} clip on scene {target_index + 1} is playing!'
            self.log(message)
            self.msg(message)
            self.pushmsg(message)
            return
        
        parent_slot.delete_clip()

        self.log('finished')

    def prompt(self, action_def, args):
        if action_def["clip"] == None:
            message = f'no clip selected!'
            self.msg(message)
            self.log(message, critical=True)
            self.pushmsg(message)
            return
        target = action_def["clip"]
        parent_slot = target.canonical_parent
        target_index = list(parent_slot.canonical_parent.clip_slots).index(parent_slot)

        if parent_slot.is_playing:
            message = f'{parent_slot.canonical_parent.name} clip on scene {target_index + 1} is playing!'
            self.msg(message)
            self.log(message)
            self.pushmsg(message)
            return
        else:
            message = f'hold to delete {parent_slot.canonical_parent.name} clip on scene {target_index + 1}'
            self.msg(message)
            self.log(message)
            self.pushmsg(message)