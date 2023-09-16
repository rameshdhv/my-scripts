"""
---------------------------------------------------------
Author: Ramesh Darisi
--------------------------------------------------------
#Add objects in parent List
#Add objects in children List
and Run the script
This works for assigning tasks on one to many, Many to Many basis


Note: if parentList is more than 1 and not matching with children list it throws an error. 
--------------------------------------------------------
"""


import maya.cmds as cmds
def selectionA():
    global selA
    selA=cmds.ls(sl=1)
    print(selA)
def selectionB():
    global selB
    selB=cmds.ls(sl=1)
    print(selB)

def connectBlendShapes():
    global BSnodes
    BSnodes=[]
    for i,j in zip(selA,selB):
        BSoutput=cmds.blendShape(i,j,n=i+"_BS")[0]
        BSnodes.append(BSoutput)
    print(BSnodes)
    
        
    
    for obj,obj2 in zip(BSnodes,selA):
        cmds.setAttr(obj+"."+obj2,1)
        
def DisconnectBlendShapes():
    BS_output=[]
    
    for i in selB:
        hist=cmds.listHistory(i)
        for j in hist:
            if cmds.nodeType(j)=="blendShape":
                BS_output.append(j)
                
    
    for each in BS_output:
        cmds.delete(each)
##############################################################################

def ParentC():
    par_offset=cmds.checkBox("ParentOffset",q=True,value=True)
    
    
    if len(selA)==len(selB):
        for each,each2 in zip(selA,selB):
            cmds.parentConstraint(each,each2,mo=par_offset)
            
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.parentConstraint(selA[0],each,mo=par_offset)
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")
        
        
###########################################################################        
        
def OrientC():
    orient_offset=cmds.checkBox("OrientOffset",q=True,value=True)
    if len(selA)==len(selB):
        for each,each2 in zip(selA,selB):
            cmds.orientConstraint(each,each2,mo=orient_offset)
            
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.orientConstraint(selA[0],each,mo=orient_offset)
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")
########################################################################        
def PointC():
    point_offset=cmds.checkBox("PointOffset",q=True,value=True)
    if len(selA)==len(selB):
        for each,each2 in zip(selA,selB):
            cmds.pointConstraint(each,each2,mo=point_offset)
            
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.pointConstraint(selA[0],each,mo=point_offset)
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")   
#######################################################################
def ScaleC():
    scale_offset=cmds.checkBox("ScaleOffset",q=True,value=True)
    if len(selA)==len(selB):
        for each,each2 in zip(selA,selB):
            cmds.scaleConstraint(each,each2,mo=scale_offset)
            
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.scaleConstraint(selA[0],each,mo=scale_offset)
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")               
#####################################################################
def MatchTransforms():
    if len(selA)==len(selB):
        for i,j in zip(selA,selB):
            cmds.matchTransform(j,i)
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.matchTransform(each,selA[0])
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")             
########################################################################  
def Match_Pivots():
    if len(selA)==len(selB):
        for i,j in zip(selA,selB):
            cmds.matchTransform(j,i,piv=True)
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.matchTransform(each,selA[0],piv=True)
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")
#########################################################################
def Parenting():
    if len(selA)==len(selB):
        for i,j in zip(selA,selB):
            cmds.parent(j,i)
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.parent(each,selA[0])
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")
######################################################################
def connectAttributes():
    if len(selA)==len(selB):
    
        for i,j in zip(selA,selB):
            cmds.connectAttr(i+".t",j+".t")
            cmds.connectAttr(i+".r",j+".r")
            cmds.connectAttr(i+".s",j+".s")
    elif len(selA)==1 and len(selB)>1:
        for each in selB:
            cmds.connectAttr(selA[0]+".t",each+".t")
            cmds.connectAttr(selA[0]+".r",each+".r")
            cmds.connectAttr(selA[0]+".s",each+".s")
                
    elif len(selA)>1 and len(selB)>len(selA):
        cmds.warning("List Length should be 1 or match with ChildrenSet")            
                

#####################################################################



        
def customwindow(name):
    if cmds.window(name,exists=1):
        cmds.deleteUI(name)
    mywindow=cmds.window(name,width=350,height=530,sizeable=0)
    cmds.showWindow(mywindow)
    ############################
    W=350
    H=500
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    
    cmds.button(label="ParentList",c="selectionA()",w=W/2,h=H/8,bgc=(0.2,0.2,0.1))
    cmds.button(label="ChildrenList",c="selectionB()",w=W/2,h=H/8,bgc=(0.2,0.2,0.1))
    
    
    cmds.setParent("..")
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    cmds.checkBox("ParentOffset",label="Offset",w=W/3,h=H/10)
    cmds.button(label="Parent Constraint",c="ParentC()",w=W*.65,h=H/10,bgc=(0.7,0.4,0.1))
    cmds.separator(width=3,height=3,style="in")
    
    cmds.setParent("..")
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    cmds.checkBox("PointOffset",label="Offset",w=W/3,h=H/10)
    cmds.button(label="Point Constraint",c="PointC()",w=W*.65,h=H/10,bgc=(0.7,0.4,0.1))
    cmds.separator(width=3,height=3,style="in")
    
    
    cmds.setParent("..")
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    cmds.checkBox("OrientOffset",label="Offset",w=W/3,h=H/10)
    cmds.button(label="Orient Constraint",c="OrientC()",w=W*.65,h=H/10,bgc=(0.7,0.4,0.1))
    cmds.separator(width=3,height=3,style="in")
    
    cmds.setParent("..")
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    cmds.checkBox("ScaleOffset",label="Offset",w=W/3,h=H/10)
    cmds.button(label="Scale Constraint",c="ScaleC()",w=W*.65,h=H/10,bgc=(0.7,0.4,0.1))
    cmds.separator(width=5,height=5,style="in")
    
    
    
    
    cmds.setParent("..")
    cmds.columnLayout()
    
    cmds.button(label="Parent",c="Parenting()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    
    cmds.button(label="ConnectAttr",c="connectAttributes()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    
    cmds.button(label="Match Transformations",c="MatchTransforms()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    
    cmds.button(label="Match Pivots",c="Match_Pivots()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    cmds.button(label="Connect Blendshape",c="connectBlendShapes()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    
    cmds.button(label="Disconnect Blendshape",c="DisconnectBlendShapes()",w=W,h=H/12,bgc=(0.5,0.4,0.1))
    
    cmds.refresh()

    
    
    
    
customwindow("SetSelectionTools_v1.0- Ramesh Darisi")
    
