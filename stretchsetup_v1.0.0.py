"""
------------------------------------------

Stretch Setup v1.0 - Ranesh Darisi

Selct the first IK joint and run the script.
-------------------------------------------
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om

import maya.cmds as cmds

class MR_Window(object):
        
    #constructor
    def __init__(self):
            
        self.window = "MR_Window"
        self.title = "Stretchy Setup V1.0---Ramesh Darisi"
        self.size = (200,200)
            
        # close old window is open
        if cmds.window(self.window, exists = True,ip=True):
            cmds.deleteUI(self.window, window=True)
            
        #create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout()
        cmds.separator(height=20)
        cmds.text("Select First IK Joint of the chain and Run the script")
        cmds.separator(height=20)
        self.rigname=cmds.textFieldGrp(label="RigName",text="",cal=(1,"left"))
        self.global_ctrl=cmds.textFieldGrp(label="Master Control",text="",cal=(1,"left")) 
        self.IK_ctrl=cmds.textFieldGrp(label="IK Control",text="",cal=(1,"left"))
        self.Clavicle_ctrl=  cmds.textFieldGrp(label="Clavicle Control",text="",cal=(1,"left"))
        cmds.button(label="Create Stretchy",w=382,c=self.stretchy,bgc=(.25,.5,.5))  
        #display new window
        cmds.showWindow()
          
                                   

    def stretchy(self,*args):
        # select the first IK joint
        ################################
        rigname=cmds.textFieldGrp(self.rigname,q=True,text=True)
        global_ctrl=cmds.textFieldGrp(self.global_ctrl,q=True,text=True)
        IK_ctrl= cmds.textFieldGrp(self.IK_ctrl,q=True,text=True)
        clavicle_ctrl=cmds.textFieldGrp(self.Clavicle_ctrl,q=True,text=True)
        
        ####################################
        pointpos = []
        jntset = []
        sel = cmds.ls(sl=1)
        if len(sel) == 1:
            children_joints = cmds.listRelatives(allDescendents=True, type='joint')
            children_joints = children_joints[::-1]
        
            children_joints.insert(0, sel[0])
        
            print(children_joints)
        
            startpos = om.MVector(cmds.xform(children_joints[0], q=1, ws=1, t=1))
            pointpos.append(startpos)
        
            endpos = om.MVector(cmds.xform(children_joints[2], q=1, ws=1, t=1))
            pointpos.append(endpos)
        
            DistanceNode = cmds.distanceDimension(sp=pointpos[0], ep=pointpos[1])
            print(DistanceNode)
            dist_loc=cmds.listConnections(DistanceNode,t="locator")
            
        else:
            cmds.error("Please select the first joint of IKChain")
        
        # Connecting stretch(Node Based)
        
        scale_compensate = cmds.createNode("multiplyDivide", n=rigname+"scaleCompensate")
        cmds.setAttr(scale_compensate + ".operation", 2)
        stretch_MD = cmds.createNode("multiplyDivide", n=rigname+"stretchPercentage")
        cmds.setAttr(stretch_MD + ".operation", 2)
        cmds.connectAttr(DistanceNode + ".distance", scale_compensate + ".input1X")
        cmds.connectAttr(scale_compensate + ".outputX", stretch_MD + ".input1X")
        distance_value = cmds.getAttr(DistanceNode + ".distance")
        cmds.setAttr(stretch_MD + ".input2X", distance_value)
        # stretch with if condition to work beyond certain distance
        condition_node = cmds.shadingNode("condition", asUtility=1,n=rigname+"_condition")
        cmds.connectAttr(scale_compensate + ".outputX", condition_node + ".firstTerm")
        cmds.setAttr(condition_node + ".secondTerm", distance_value)
        cmds.setAttr(condition_node + ".operation", 2)
        cmds.setAttr(condition_node + ".colorIfFalseR", 1)
        cmds.connectAttr(stretch_MD + ".outputX", condition_node + ".colorIfTrueR")
        
        # condition node gets connected to translate values of joints multiplied with stretch percent.
        stretch_values = cmds.createNode("multiplyDivide", n=rigname+"MD_stretchvalue")
        
        cmds.connectAttr(condition_node + ".outColorR", stretch_values + ".input1X")
        cmds.connectAttr(condition_node + ".outColorR", stretch_values + ".input1Y")
        x_value = cmds.getAttr(children_joints[1] + ".translateX")
        y_value = cmds.getAttr(children_joints[2] + ".translateX")
        
        cmds.setAttr(stretch_values + ".input2X", x_value)
        cmds.setAttr(stretch_values + ".input2Y", y_value)
        
        cmds.connectAttr(stretch_values + ".outputX", children_joints[1] + ".translateX")
        cmds.connectAttr(stretch_values + ".outputY", children_joints[2] + ".translateX")
        
        
        
        # parenting distance locators
        
        
        parent_loc=cmds.spaceLocator(n=rigname+"_IK_Loc")
        cmds.xform(parent_loc,ws=1,t=startpos)
        cmds.parent(children_joints[0],parent_loc)
        
        cmds.parent(dist_loc[0],parent_loc)
        
        
        cmds.parent(dist_loc[1],IK_ctrl)
        
        
        
        
        # connecting to global scale
        if cmds.objExists(global_ctrl):
            cmds.connectAttr(global_ctrl+".scaleX",scale_compensate+".input2X")
            if cmds.objExists(clavicle_ctrl):
                cmds.parent(parent_loc,clavicle_ctrl)
            else:
                cmds.parent(parent_loc,global_ctrl)
          
            
        else:
            print("Global_ctrl not found")
        
        cmds.select(cl=1)

myWindow = MR_Window()    
    
    
    
    
    
    
