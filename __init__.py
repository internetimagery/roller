# Create rolling controller. Great for offsets etc
import math
import maya.cmds as cmds

RADIANS = math.radians(1)

def main():
    err = cmds.undoInfo(openChunk=True)
    try:
        pass
    except err:
        pass
    finally:
        cmds.select(clear=True)
        cmds.undoInfo(closeChunk=True)
        if err: cmds.undo()
