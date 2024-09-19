# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

DEFAULT_CLIP_LENGTH_BARS = 8

class clip_halve(UserActionsBase):
    
    ### boilerplate

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.logging_level = 'critical'
        self.midi_clips_listeners = []

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
        self.add_clip_action('halve', self.clip_halve)

    def clip_halve(self, action_def, args):
        target = action_def["clip"]
        self.log(f'OLD start_marker {target.start_marker} OLD end_marker {target.end_marker}')
        default_beat_count = float(DEFAULT_CLIP_LENGTH_BARS) * float(self._song.signature_numerator)

        if (target.is_audio_clip and target.is_recording) or (target.is_midi_clip and not target.is_overdubbing and target.is_recording):
            self.log(f'clip is recording!')
            callback = lambda: self.recording_callback(target, args)
            if target.is_audio_clip and args == '<':
                if target.playing_position < (default_beat_count / 2.0):
                    target.canonical_parent.fire()
                    return
                else:
                    target.add_is_recording_listener(callback)
            elif target.is_audio_clip and args == '>':
                target.add_is_recording_listener(callback)
            elif target.is_midi_clip and args == '>':
                self.midi_clips_listeners.append({
                    "clip": target,
                    "callback": callback
                })
                target.add_is_overdubbing_listener(callback)
                target.add_is_recording_listener(callback)
                #target.canonical_parent.fire()
                
                
            elif target.is_midi_clip and args == "<":
                target.canonical_parent.fire()
                return
            self.log(f'added callback, firing and returning')
            return

        current_loop_length = target.end_marker - target.start_marker
        halved_loop_length = current_loop_length / 2.0

        if args == '<':
            if target.loop_start == 0.0:
                target.end_marker = halved_loop_length
                target.loop_end = halved_loop_length
            else:
                target.end_marker = target.end_marker - halved_loop_length
                target.loop_end = target.end_marker
        elif args == '>':
            if target.loop_start == 0.0:
                target.start_marker = target.end_marker / 2.0
                target.loop_start = target.end_marker / 2.0
            else:
                target.start_marker = target.start_marker + halved_loop_length
                target.loop_start = target.start_marker

        elif args.lower() == 'reset':
            target.start_marker = 0.0
            target.end_marker = default_beat_count
            target.loop_start = 0.0
            target.loop_end = default_beat_count
        else:
            self.log('argument provided must be "<" or ">"', critical=True)
            return
        
        self.log(f'NEW start_marker {target.start_marker} end_marker {target.end_marker}')

        if target.is_midi_clip:
            self.log(f'checking for callback')
            self.log(self.midi_clips_listeners)
            for i in range(len(self.midi_clips_listeners) + 1):
                self.log(f'i = {i}')
                if i == len(self.midi_clips_listeners):
                    self.log('could not find listener')
                    break
                if self.midi_clips_listeners[i]["clip"] == target:
                    self.log(f'found callback at index {i}')
                    callback = self.midi_clips_listeners[i]["callback"]
                    target.remove_is_recording_listener(callback)
                    target.remove_is_overdubbing_listener(callback)
                    self.midi_clips_listeners.pop(i)
                    self.log('removed listener')
                    break
            
        self.log('finished')
        
    def recording_callback(self, target, args):
        self.log('callback firing')
        if target.is_audio_clip and target.is_recording:
            self.log('audio clip still recording, returning')
            return
        clip_slot = target.canonical_parent
        track = clip_slot.canonical_parent
        clip_index = list(track.clip_slots).index(clip_slot)
        self.cxp_action(f'WAIT 2; "{track.name}" / USER_CLIP({clip_index + 1}) HALVE {args}')
        self.log(f'callback finished')
        return



        