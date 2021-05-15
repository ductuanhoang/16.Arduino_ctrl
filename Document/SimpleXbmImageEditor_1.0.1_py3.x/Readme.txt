Simple xbm Image Editor

Author                Mike Cavender
Programming Language  Python 3.5
Install Requires      Tkinter
Platform              Tested on a Windows 10 PC
Version               1.0.1
Development Status    Recently changed to Production
Intended Audience     Developers
License               New BSD; see the License.txt file

Description:

The Simple xbm Image Editor presents a Tkinter-based GUI and has the following functions:
- Create new .xbm image files and update existing files
- Images are displayed in actual size and in an enlarged grid suitable for editing
- Toggle the bits of the image edit grid to foreground/background with mouse clicks
- Increase or decrease the width and/or height of an image
- Rotate an image
- Shift an image up, down, left or right
- Change the colors in which an image is displayed, although colors are not stored
  in .xbm files. Background and foreground color selection is provided in order to
  experiment with colors for your application.

Only the .xbm image format is supported.

Note: The editor can display very large .xbm files in their actual size but the maximum
bitmap size that can be edited is 2500 pixels. This limit is arbitrary and can easily be
changed, but bitmap edit grid loading and, in particular, garbage collection become
quite slow if the limit is a lot more than 2500 pixels. Editing operations work fine at
bitmap sizes larger than 2500 pixels. Change the gridMax symbolic constant to experiment
with the size limit.
