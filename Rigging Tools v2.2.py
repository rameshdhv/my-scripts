def create_AddBlendshape():
    #select all targets first and main geo 
    import maya.cmds as cmds
    sel=cmds.ls(sl=1)
    iso_sel=sel[:-1]
    bsnode=[]
    hist=cmds.listHistory(sel[-1])
    
    for obj in hist:
        if cmds.nodeType(obj)=="blendShape":
            bsnode.append(obj)
            
    try:
        tgt=cmds.aliasAttr(bsnode[0],q=True)[::2]
    except:
        pass
    
    if len(bsnode)==0:
        cmds.blendShape(sel[:-1],sel[-1],n=sel[-1]+"_BlendShape")
        
    else:
        count=len(tgt)
        for each in iso_sel:
            cmds.blendShape(bsnode[0],edit=True,t=[sel[-1],count,each,1])
            count+=1

        
    



def swapControlCurves():
    import maya.cmds as cmds
    sel=cmds.ls(sl=1)
    new_sel=sel[:-1]
    
    count=0
    for i in new_sel:
        
        #step1: duplicate reference control 
        ref= cmds.duplicate(sel[-1])
        #get the shape node of reference control
        ref_ctrl=cmds.listRelatives(ref,s=True)[0]
        #get the shape node of old controls
        old_ctrl=cmds.listRelatives(i,s=1)[0]
        #delete shape nodes of old control 
        cmds.delete(old_ctrl)
        #parent the reference control shape node under old control
        cmds.parent(ref_ctrl,i,r=True,s=True)
        #rename the shape node according to old control 
        cmds.rename(ref_ctrl,old_ctrl)
        #delete unused transform nodes of duplicated reference controls
        cmds.delete(ref)
        #clear the selection
        cmds.select(cl=1)
        
        






def parentSequence():
    import maya.cmds as cmds
    sel=cmds.ls(sl=1)

    count=len(sel)-1 #-1 is for range we need the parent function to work n-1 times.ex: if 3 objects we need to run the parent loop twice

    for i in range(count):
        cmds.parent(sel[count],sel[count-1])
        count-=1
        







def controlatpivot():
    
    import maya.cmds as cmds
    c_global=cmds.checkBox("CGlobal",q=True,value=True)
    c_local=cmds.checkBox("CLocal",q=True,value=True)
    if c_global==True and c_local==False:
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
    elif c_global==False and c_local==True:
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
            cmds.select(cl=1)
            cmds.select(i)
            
            ppc=cmds.pointOnPolyConstraint(i,ctrl_grp,mo=0)
            cmds.delete(ppc)
    elif c_global==False and c_local==False:
        cmds.warning("Select any one of the options below Global or Local")
        
    elif c_global==True and c_local==True:
        cmds.warning("Select only one Axis")
        
def jointatselection():
    import maya.cmds as cmds
    j_global=cmds.checkBox("JGlobal",q=True,value=True)
    j_local=cmds.checkBox("JLocal",q=True,value=True)
    if j_global==True and j_local==False:
        sel = cmds.ls(sl=1, fl=1)
        for i in sel:
            cmds.select(cl=1)
            jnt = cmds.joint()
            pointlocation = cmds.xform(i, q=True, ws=True, t=1)
            jntlocation = cmds.xform(jnt, ws=1, t=pointlocation)

    elif j_global==False and j_local==True:
        sel = cmds.ls(sl=1, fl=1)
        for i in sel:
            cmds.select(cl=1)
            jnt = cmds.joint()
            pointlocation = cmds.xform(i, q=True, ws=True, t=1)
            jntlocation = cmds.xform(jnt, ws=1, t=pointlocation)
            cmds.select(i)
            ppc=cmds.pointOnPolyConstraint(i,jnt,mo=0)
            cmds.delete(ppc)
            
            
    elif j_global==False and j_local==False:
        cmds.warning("Select any one of the options below Global or Local")
        
    elif j_global==True and j_local==True:
        cmds.warning("Select only one Axis")
            
        
        
        
        





def grouping():
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)
    if len(sel) == 0:
        cmds.error("Please select objects to group")
    else:
        for i in sel:
            cmds.select(cl=1)
            k = cmds.group(i, n=i + "_Group")
            cmds.matchTransform(k, i, piv=True)


def Zeroout():
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)
    for i in sel:
        grp = cmds.group(i, em=True,n=i+"_Offset_Group")
        cmds.matchTransform(grp, i)
        cmds.parent(i, grp)



def follicleAtPivot():
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



def follicelcontrol():

    
    
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







def customwindow(name):
    if cmds.window(name,exists=1):
        cmds.deleteUI(name)
    mywindow=cmds.window(name,width=350,height=500,sizeable=1)
    cmds.showWindow(mywindow)
    ############################
    wWidth=350
    wHeight=900
    cmds.columnLayout()
    cmds.button(label="Create Control at Pivot",c="controlatpivot()",width=wWidth,height=wHeight/18,bgc=(0,0.25,0.25))
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    
    
    cmds.checkBox("CGlobal",label="        Global",width=wWidth/2,height=wHeight/18)
    cmds.checkBox("CLocal",label="          Local",width=wWidth/2,height=wHeight/18)
    cmds.separator(width=5,height=5,style="in")
    cmds.setParent("..")
    
    cmds.columnLayout()
    cmds.button(label="Joint at Pivot",c="jointatselection()",width=wWidth,height=wHeight/18,bgc=(0,0.2,0.2))
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    
    
    cmds.checkBox("JGlobal",label="       Global",width=wWidth/2,height=wHeight/18)
    cmds.checkBox("JLocal",label="        Local",width=wWidth/2,height=wHeight/18)
    cmds.separator(width=5,height=5,style="in")
    cmds.setParent("..")
    
    cmds.columnLayout()
    cmds.button(label="Follicle at each Pivot",c="follicleAtPivot()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Follicle Control",c="follicelcontrol()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Parent Sequence",c="parentSequence()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="ZeroOut",c="Zeroout()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Create/Add Blendshape",c="create_AddBlendshape()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Group",c="grouping()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Swap Control Shapes",c="swapControlCurves()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))

    
    
    
    
    
customwindow("Rigging Tools V2.0")
    
