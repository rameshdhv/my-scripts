"""
------------------------------------------------------------------------

CUSTOM TOOLS v1.0.py  ----Ramesh Darisi


-----------------------------------------------------------------------"""


def grouping(*args):
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)
    if len(sel) == 0:
        cmds.error("Please select objects to group")
    else:
        for i in sel:
            cmds.select(cl=1)
            k = cmds.group(i, n=i + "_Group")
            cmds.matchTransform(k, i, piv=True)


####################################################################
def parentorder(*args):
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)

    for i in sel:
        cmds.parent()


##########################################################################33
def jointatselection(*args):
    import maya.cmds as cmds
    sel = cmds.ls(sl=1, fl=1)
    for i in sel:
        cmds.select(cl=1)
        jnt = cmds.joint()
        pointlocation = cmds.xform(i, q=True, ws=True, t=1)
        jntlocation = cmds.xform(jnt, ws=1, t=pointlocation)


################################################################################
def Zeroout(*args):
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)
    for i in sel:
        grp = cmds.group(i, em=True,n=i+"_Offset_Group")
        cmds.matchTransform(grp, i)
        cmds.parent(i, grp)


############################################################################
def follicleAtPivot(*args):
    import maya.cmds as cmds
    import maya.mel as mel
    sel = cmds.ls(sl=1, fl=1)
    for i in sel:
        planes = cmds.nurbsPlane(i, ax=[0, 1, 0], lr=1, w=0.2, ch=0, n=i + "_Follicle_Geo")

        plane_shapes = cmds.pickWalk(planes, d="down")

        follicle_shapes = cmds.createNode("follicle", n=i + "_Follicle")

        # transform_node=cmds.createNode("transform",n=i+"_Transform")
        follicle = cmds.pickWalk(follicle_shapes, d="up")

        # query the world position
        pos = cmds.xform(i, q=True, ws=1, t=1)
        cmds.xform(planes[0], t=pos)

        cmds.connectAttr(plane_shapes[0] + ".local", follicle_shapes + ".inputSurface")
        cmds.connectAttr(plane_shapes[0] + ".worldMatrix[0]", follicle_shapes + ".inputWorldMatrix")
        cmds.connectAttr(follicle_shapes + ".outRotate", follicle[0] + ".rotate")
        cmds.connectAttr(follicle_shapes + ".outTranslate", follicle[0] + ".translate")
        cmds.setAttr(follicle_shapes + ".parameterU", 0.5)
        cmds.setAttr(follicle_shapes + ".parameterV", 0.5)
###############################################################################
def controlatpivot(*args):
    import maya.cmds as cmds
    sel = cmds.ls(sl=1, fl=1)
    for i in sel:
        cmds.select(cl=1)
        jnt = cmds.joint(n=i+"Jnt")
        jnt_grp=cmds.group(jnt,n=i+"Group")
        
        pointlocation = cmds.xform(i, q=True, ws=True, t=1)
        jntlocation = cmds.xform(jnt_grp, ws=1, t=pointlocation)
        #create a control with offset group
        ctrl=cmds.circle(ch=0,n=i+"Ctrl")
        ctrl_grp=cmds.group(ctrl,n=i+"Ctrl_Group")
        ctrllocation=cmds.xform(ctrl_grp,ws=1,t=pointlocation)
        cmds.parent(jnt_grp,ctrl)
##################################################################################        

def showWindow():
    name = "CustomTools"
    if cmds.window(name, q=True, exists=True):
        cmds.deleteUI(name)
    cmds.window(name,widthHeight=(100,100))
    #scrollLayout = cmds.scrollLayout(verticalScrollBarThickness=10)
    cmds.showWindow()
    column = cmds.columnLayout()
    cmds.frameLayout(label="Custom Tools_v1.1----Ramesh Darisi", bgc=(0.5, 0, 0.25), hlc=(1, 1, 1))
    

    cmds.button(label="Group", w=200, c=grouping, bgc=(0, .25, .25))
    cmds.button(label="parent In Order", w=200, c=parentorder, bgc=(0, .25, .25))
    cmds.button(label="Joint at Selection",w=200, c=jointatselection, bgc=(0, .25, .25))

    cmds.button(label="Zero_Out", w=200, c=Zeroout, bgc=(0, .25, .25))
    cmds.button(label="Follicle at Each Pivot", w=200, c=follicleAtPivot, bgc=(0, .25, .25))
    cmds.button(label="Control at Each Pivot", w=200, c=controlatpivot, bgc=(0, .25, .25))


showWindow()