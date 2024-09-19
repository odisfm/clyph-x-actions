# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

class looper(UserActionsBase):

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
        self.add_track_action('lpr', self.looper)

    def looper(self, action_def, args):
        target = action_def["track"]
        looper_device = None
        device_list = list(target.devices)
        for device in device_list:
            if device.class_name == 'Looper':
                looper_device = device
                break
        if looper_device is None:
            message = f'No looper device on track {target.name}!'
            self.shout(message)
            return

        if args == 'record':
            looper_device.record()
        elif args == 'clear':
            looper_device.clear()
        elif args == 'doublespeed':
            looper_device.double_speed()
        elif args == 'halfspeed':
            looper_device.half_speed()
        elif args == 'halflength':
            looper_device.half_length()
        elif args == 'overdub':
            looper_device.overdub()
        elif args == 'play':
            looper_device.play()
        elif args == 'stop':
            looper_device.stop()
        elif args == 'undo':
            looper_device.undo()
        else:
            args_original = args
            args = args.split(' ')

            if args[0] == 'bars':
                record_length = None
                try:
                    record_length = int(args[1])
                except:
                    if args[1] == 'x':
                        record_length = 10
                    else:
                        message = f'Invalid input for looper record length'
                        self.msg(message)
                        self.log(message, critical=True)
                        return
                if record_length >= 1 and record_length <= 8:
                    record_length -= 1
                elif record_length == 12:
                    record_length = 8
                elif record_length == 16:
                    record_length = 9
                elif record_length == 10:
                    pass
                else:
                    message = f'Invalid input for looper record length'
                    self.msg(message)
                    self.log(message, critical=True)
                    return

                looper_device.record_length_index = record_length

            elif args[0] == 'dubafter':
                if len(args) == 1:
                    looper_device.overdub_after_record = not looper_device.overdub_after_record
                elif args[1] in ['on', 'true', '1']:
                    looper_device.overdub_after_record = True
                elif args[1] in ['off', 'false', '0']:
                    looper_device.overdub_after_record = False