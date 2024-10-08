from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

LOGGING_LEVEL = 'all'

class latency_report(UserActionsBase):

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

    ### end boilerplate

    def create_actions(self):
        self.add_global_action('latency', self.latency_report)

    def latency_report(self, action_def, args):
        self.log('running')
        tracklist = list(self._song.tracks)
        report = []

        def recursive_search(devices, master=False, return_track=False, inside_chain=None):
            for device in devices:
                if device.class_name in ['AudioEffectGroupDevice', 'MidiEffectGroupDevice', 'InstrumentGroupDevice'] and len(list(device.chains)) > 0:
                    for chain in list(device.chains):
                        recursive_search(chain.devices, master, return_track, inside_chain=chain.canonical_parent.name)
                elif device.class_name == 'DrumGroupDevice' and len(list(device.chains)) > 0:
                    for chain in list(device.chains):
                        recursive_search(chain.devices, master, return_track, inside_chain=chain.canonical_parent.name)

                elif device.latency_in_ms > 0.0:
                    item = {
                        "track": track.name,
                        "device": device.name,
                        "device_class": device.class_display_name,
                        "latency": round(device.latency_in_ms, 1),
                        "samples_latency": device.latency_in_samples,
                        "inside_chain": None
                    }
                    if master:
                        item['track'] = 'MAIN/MASTER'
                    elif return_track:
                        item['track'] = 'RETURN ' + item['track']
                    if inside_chain:
                        item['inside_chain'] = inside_chain
                    report.append(item)


        for track in tracklist:
            recursive_search(list(track.devices))
        for track in list(self._song.return_tracks):
            recursive_search(list(track.devices), return_track=True)

        recursive_search(self._song.master_track.devices, master=True)

        message = ''
        report = sorted(report, key=lambda x: x['latency'], reverse=True)

        for item in report:
            chain_string = ''
            if item['inside_chain'] != None:
                chain_string = f"(inside {item['inside_chain']}) "
            message += f"\n{item['track']} | {item['device']} {chain_string}[{item['device_class']}] | {item['samples_latency']}smpl | {item['latency']}ms"

        if message != '':
            self.log(message)
        else:
            message = 'No latency inducing devices found in set'
            self.log(message)

        self.msg('Wrote latency report to log.txt')