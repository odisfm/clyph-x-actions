# _extras

Here's some other stuff.
<br>
### modified OSC output
Using [Stray's OSC output actions](https://nativekontrol.proboards.com/thread/3620/beta-osc-output-clyphx-pro) it is possible to send OSC out from Live. As mentioned in the linked thread, the OSC messages will be re-sent every 500 milliseconds to mitigate packet loss. Contrary to Stray's advice, setting this refresh rate to 0 does not stop the refresh happening. 

I was provided with an alternative version of the OSC server file which stops the refresh, however this mod stops _manual_ repeated messages from sending. For example, after calling `OSC INT /test 1`, any repeated calls of `OSC INT /test 1` will not be sent, until another value, like `OSC INT /test 2` is sent. I decompiled this modified file to change this behaviour.

#### usage
Download __OSCserver.py__ and replace the original __OSCserver.pyc__ file with it. Note the change of file extension from __.pyc__ to __.py__. 

The location of the original is `<path to Live remote scripts folder>/ClyphX_Pro/clyphx_pro/osc/OSCserver.pyc`