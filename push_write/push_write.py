# made by odis :)
# https://github.com/odisfm/clyph-x-actions

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

class push_write(UserActionsBase):

    ### boilerplate

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.logging_level = 'all'
    
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
        self.add_global_action('pushwrite', self.push_write)
       
    def push_write(self, action_def, args):
        line_number = int(args.split(' ')[0])
        message = args.split('"')[1]
        ASCII = self.string_to_ASCII(message)
        line = self.format_line(ASCII)
        self.print_message(line_number, line)

    def string_to_ASCII(self, string):
        output = []
        for char in string:
            output.append(ord(char))
        return output
    
    def format_line(self, ASCII):
        if len(ASCII) > 68:
            ASCII = ASCII[0:68]
        while len(ASCII) < 68:
            ASCII.append(32)
        output = ''
        for char in ASCII:
            output += f'{char} '
        return output
    
    def print_message(self, line, ASCIIstring):
        if line == 1:
            line = 24
        elif line == 2:
            line = 25
        elif line == 3:
            line = 26
        elif line == 4:
            line = 27

        message = f'240 71 127 21 {line} 0 69 0 {ASCIIstring} 247'

        self.cxp_action(f'MIDI {message}')
        