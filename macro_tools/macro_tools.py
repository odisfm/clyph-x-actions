from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
import random

LOGGING_LEVEL = 'critical'

class macro_tools(UserActionsBase):
    
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
        self.add_device_action('macinc', self.increment_macro_variation)
        self.add_device_action('macset', self.recall_macro_variation)
        self.add_device_action('macrandom', self.randomize_macro_controls)

    def is_device_rack(self, device):
        if device.class_name in ['AudioEffectGroupDevice', 'MidiEffectGroupDevice', 'InstrumentGroupDevice']: 
            return True
        else:
            message = f'Selected device is not a rack!'
            self.shout(message, critical=True)
            return False
       
    def increment_macro_variation(self, action_def, args):
        device = action_def['device']

        if not self.is_device_rack(device):
            return
        
        current_variation = device.selected_variation_index
        variation_count = device.variation_count

        if current_variation == -1:
            new_variation = 0
        elif args == '<':
            new_variation = current_variation -1
        elif args == '>':
            new_variation = current_variation + 1
        else:
            self.log('valid arguments are "<" or ">"')
            return

        if new_variation < 0:
            new_variation = variation_count -1
        elif new_variation >= variation_count:
            new_variation = 0

        device.selected_variation_index = new_variation
        device.recall_selected_variation()
        
    def recall_macro_variation(self, action_def, args):
        device = action_def['device']

        if not self.is_device_rack(device):
            return
        
        current_variation = device.selected_variation_index
        variation_count = device.variation_count

        if args == 'rnd':
            random_variation = current_variation
            while random_variation == current_variation:
                random_variation = random.randint(0, (variation_count - 1))
                device.selected_variation_index = random_variation
                device.recall_selected_variation()
        else:
            try:
                new_variation = int(args)
                new_variation -= 1
            except:
                self.log(f'valid arguments are \'RND\' or the number of an existing macro variation', critical=True)
                return
            if new_variation < 0:
                self.log(f'macro variation must be a positive number', critical=True)
                return
            elif new_variation + 1 > variation_count:
                self.log(f'variation {new_variation + 1} does not exist on targeted device', critical=True)
                return
            device.selected_variation_index = new_variation
            device.recall_selected_variation() 

    def randomize_macro_controls(self, action_def, args):
        device = action_def['device']
        if not self.is_device_rack(device):
            return
        device.randomize_macros()
        


        
        