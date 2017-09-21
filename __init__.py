# Create rolling controller. Great for offsets etc
import math
import maya.cmds as cmds


def main():
    err = cmds.undoInfo(openChunk=True)
    try:
        # Create our objects. Parent them together.
        root = cmds.group(name="roller_root", empty=True)
        ctrl = cmds.group(name="%s_ctrl" % root, empty=True) # TODO: change this to something nicer
        cmds.parent(ctrl, root)

        # Create our nodes.
        mult_radians = cmds.shadingNode(asUtility="multiplyDivide")
        mult_scale = cmds.shadingNode(asUtility="multiplyDivide")
        mult_invert = cmds.shadingNode(asUtility="multiplyDivide")

        # Set values
        radians = math.radians(1)
        cmds.setAttr("%s.input1X" % mult_radians, radians)
        cmds.setAttr("%s.input1Y" % mult_radians, radians)
        cmds.setAttr("%s.input1Z" % mult_radians, radians)


        pass
    except err:
        pass
    finally:
        cmds.select(clear=True)
        cmds.undoInfo(closeChunk=True)
        if err: cmds.undo()
