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

def follicelcontrol(*args):

    
    
    sel=cmds.ls(sl=1,fl=1)
    if len(sel)==0:
        cmds.error("please select the nurbsSurface")
    else:
        for i in sel:
            
            #planes=cmds.nurbsPlane(i,ax=[0,1,0],lr=1,w=0.2,ch=0,n=i+"_Follicle_Geo")
            
            plane_shapes=cmds.pickWalk(sel[0],d="down")
            
            follicle_shapes = cmds.createNode("follicle",n=i+"_Follicle")
            print(follicle_shapes)
            #transform_node=cmds.createNode("transform",n=i+"_Transform")
            follicle= cmds.pickWalk(follicle_shapes,d="up")
            print(follicle)
            #query the world position
            pos=cmds.xform(i,q=True,ws=1,t=1)
            cmds.xform(sel[0],t=pos)
            
            
            
            cmds.connectAttr(plane_shapes[0]+".local",follicle_shapes+".inputSurface")
            cmds.connectAttr(plane_shapes[0]+".worldMatrix[0]",follicle_shapes+".inputWorldMatrix")
            cmds.connectAttr(follicle_shapes+".outRotate",follicle[0] +".rotate")
            cmds.connectAttr(follicle_shapes+".outTranslate",follicle[0] +".translate")
            cmds.setAttr(follicle_shapes+".parameterU",0.5)
            cmds.setAttr(follicle_shapes+".parameterV",0.5)
            
            #create and snap the control group to xform
            
            circle_ctrl = cmds.circle(ch=0)
            sdk_grp = cmds.group(circle_ctrl,n=circle_ctrl[0]+"_SDK_Group")
            print(sdk_grp)
            ctrl_grp =  cmds.group(sdk_grp,n=circle_ctrl[0]+"_Ctrl_Group")
            cmds.xform(ctrl_grp,ws=1,t = pos)    
            
            #parent constrain ctrl group with the new follicle
            
            cmds.parentConstraint(follicle,ctrl_grp)
                
            #create a PlusminusAverage node and make the respective connections 
            pma=cmds.createNode("plusMinusAverage",n=i+"_PMA")
            
            MD01=cmds.createNode("multiplyDivide",n=circle_ctrl[0]+"_neg_MD")
            MD02=cmds.createNode("multiplyDivide",n=circle_ctrl[0]+"MD_offset")
            MD03=cmds.createNode("multiplyDivide",n=circle_ctrl[0]+"MD_offset")
           
            #extra attributes for the follicle control
            cmds.addAttr(circle_ctrl[0], ln = "X_senstivity",  at='float',  min=0, dv=0.1, k=1)
            cmds.addAttr(circle_ctrl[0], ln = "Y_senstivity",  at='float',  min=0, dv=0.1, k=1)
            
            cmds.addAttr(circle_ctrl[0], ln = "X_Offset",  at='float', dv=0, k=1)
            cmds.addAttr(circle_ctrl[0], ln = "Y_Offset",  at='float', dv=0, k=1)
            
            #use a offsetMD node to control the sensitivity of controls
            cmds.connectAttr(circle_ctrl[0]+".translateX",MD02+".input1X")
            cmds.connectAttr(circle_ctrl[0]+".translateY",MD02+".input1Y")
            
            cmds.connectAttr(circle_ctrl[0]+".X_senstivity",MD02+".input2X")
            cmds.connectAttr(circle_ctrl[0]+".Y_senstivity",MD02+".input2Y")
            
            
            
            #cmds.setAttr(MD02+".outputX",
            
            
            
            cmds.connectAttr(MD02+".outputX",pma+".input2D[1].input2Dx")
            cmds.connectAttr(MD02+".outputY",pma+".input2D[1].input2Dy")
            #xoffset and y offset connections
            cmds.connectAttr(circle_ctrl[0]+".X_Offset",MD03+".input1X")
            cmds.connectAttr(circle_ctrl[0]+".Y_Offset",MD03+".input1Y")
            cmds.setAttr(MD03+".input2X",0.1)
            cmds.setAttr(MD03+".input2Y",0.1)
            
            
            cmds.connectAttr(MD03+".outputX",pma+".input2D[2].input2Dx")
            cmds.connectAttr(MD03+".outputY",pma+".input2D[2].input2Dy")
            
            cmds.setAttr(pma+".input2D[0].input2Dx",0.5)
            cmds.setAttr(pma+".input2D[0].input2Dy",0.5)
            cmds.connectAttr(pma+".output2Dx",follicle_shapes+".parameterU")
            cmds.connectAttr(pma+".output2Dy",follicle_shapes+".parameterV")
            #counter double transform
            cmds.connectAttr(circle_ctrl[0]+".translate",MD01+".input1")
            cmds.setAttr(MD01+".input2X",-1)
            cmds.setAttr(MD01+".input2Y",-1)
            cmds.setAttr(MD01+".input2Z",-1)
            cmds.connectAttr(MD01+".output",sdk_grp+".translate",force=True)
            
            cmds.group(ctrl_grp,follicle,n=follicle[0]+"_Group")
            cmds.select(cl=1)
            
            
            
            
            
            ###--------------------------------------------------------------###
        


######################################################################################       

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
    cmds.button(label="Create Follicle Control", w=200, c=follicelcontrol, bgc=(0, .25, .25))
    


showWindow()
