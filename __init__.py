# Create rolling controller. Great for offsets etc
import math
import maya.cmds as cmds

XYZ = ("X", "Y", "Z")

def main():
    err = cmds.undoInfo(openChunk=True)
    try:
        # Create our objects. Parent them together.
        root = cmds.group(name="roller_root", empty=True)
        ctrl = cmds.polySphere(name="%s_ctrl" % root)[0] # TODO: change this to something nicer
        cmds.parent(ctrl, root)

        # Lock our rotation axis.
        cmds.setAttr("%s.ry" % ctrl, lock=True)

        # Create our nodes.
        mult_radians = cmds.shadingNode("multiplyDivide", asUtility=True)
        mult_scale = cmds.shadingNode("multiplyDivide", asUtility=True)
        mult_invert = cmds.shadingNode("multiplyDivide", asUtility=True)

        # Set values
        radians = math.radians(1)
        for xyz in XYZ:
            cmds.setAttr("%s.input1%s" % (mult_radians, xyz), radians)
            cmds.setAttr("%s.input1%s" % (mult_invert, xyz), -1)

        # Plug em together!
        for xyz in XYZ:
            cmds.connectAttr(
                "%s.rotate%s" % (ctrl, xyz),
                "%s.input2%s" % (mult_radians, xyz),
                force=True)
            cmds.connectAttr(
                "%s.scale%s" % (ctrl, xyz),
                "%s.input1%s" % (mult_scale, xyz),
                force=True)
            cmds.connectAttr(
                "%s.output%s" % (mult_radians, xyz),
                "%s.input2%s" % (mult_scale, xyz),
                force=True)
            cmds.connectAttr(
                "%s.output%s" % (mult_scale, xyz),
                "%s.input2%s" % (mult_invert, xyz),
                force=True)

        cmds.connectAttr(
            "%s.outputX" % mult_scale,
            "%s.translateZ" % ctrl,
            force=True)
        cmds.connectAttr(
            "%s.outputZ" % mult_invert,
            "%s.translateX" % ctrl,
            force=True)
        cmds.connectAttr(
            "%s.outputY" % mult_scale,
            "%s.translateY" % ctrl,
            force=True)

    except err:
        pass
    finally:
        cmds.select(clear=True)
        cmds.undoInfo(closeChunk=True)
        if err: cmds.undo()
