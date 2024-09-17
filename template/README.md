# user action template

The template I use for all my user actions. It's pretty barebones but has a couple of nice quality of life features:

### Aliases for the standard log_message and show_message methods

Native ClyphX method:\
`self.canonical_parent.log_message(f'Hello world!')`

Alias:\
`self.msg(f'Hello world!)`

### Prepend the (class) name of your user action to logged messages

When logging a message to log.txt, messages are prepended with the class they are inside.

Input: `self.log('firing clip on scene 3')`\
Output: `MYCOOLACTION: firing clip on scene 3`

### Filter non-critical log messages

When coding a user action, you may require many log messages for debug purposes. When the action is complete, these become unnecessary, but there are certain errors you always want to log.

In the `__init__` method of the template is a line `self.logging_level = 'all'`. Changing this to `self.logging_level = 'critical'` will suppress all log messages not passed like this: `self.log(f'track not found!', critical=True)`. You don't need to pass any argument for non-critical messages.

Messages logged like this will also be prepended with `CRITICAL:`. This allows you to make a rule in your log viewer to highlight them.

### Alias for triggering ClyphX Pro action lists

Previously you could trigger action lists like this:
`self.canonical_parent.clyphx_pro_component.trigger_action_list('METRO ON')`

The alias is much shorter:\
`self.cxp_action('METRO ON')`


## Helper methods
Several methods I often use with my actions:

`get_selected_track()`\
Returns the track object of the currently selected track.

`get_selected_scene_index()`\
Returns an integer containing the number of the scene selected in Live's UI (zero-indexed)

`get_track_by_name(search_name)`\
Pass a string and get back the first track in the set with that name. Returns `False` if no track with that name exists.

`push_msg(message)`\
Pass a string to display a message on a connected Push 1 or Push 2 in Live mode. (This just calls the native Clyph X action `PUSH MSG`). _Push 2 on Ableton 12+ must be using the legacy control surface script)._