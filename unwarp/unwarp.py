# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

LOGGING_LEVEL = 'critical'

class unwarp(UserActionsBase):
    
### boilerplate

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
    
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
        self.add_clip_action('unwarp', self.unwarp)
       
    def unwarp(self, action_def, args):
        target = action_def['clip']
        if not target.is_audio_clip:
            message = f'Only available for audio clips'
            self.shout(message, critical=True, class_label=True)
            return
        warp_markers = list(target.warp_markers)
        for i in range(len(warp_markers)):
            target.remove_warp_marker(warp_markers[i].beat_time)