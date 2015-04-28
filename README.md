remotefreebox
=============

Python library for the Freebox network-based input API (rudp, foil). The code is based from the C implementation available at https://github.com/fbx/ .

The documentation of the protocol is available here: http://dev.freebox.fr/sdk/

## Usage

Use the class FreeboxController, that automatically look for the network for a freebox.
Then, use the press method to simulate a key press.

    fbx = FreeboxController()
    fbx.press("Chan +")
