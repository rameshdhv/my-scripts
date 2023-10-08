"""
---------------------------------------------------------
Author: Ramesh Darisi
--------------------------------------------------------

"""

def ribbonjoints():
    #########################################
    #for creating controls
    ########################################
    import maya.cmds as cmds
    ctrl_sel=cmds.ls(sl=1)
    
    if len(ctrl_sel)>1:
        cmds.warning("select one surface at a time")
    
    elif len(ctrl_sel)==0:
        cmds.warning("No surface object selected")
            
    elif len(ctrl_sel)==1:
        
        ctrl_shp=cmds.listRelatives(ctrl_sel[0],s=True)
        
                   
        ctrl_count=int(cmds.textFieldGrp(ctrl_number, q=1, text=1))
        ctrl_j=0
        ctrl_placement=1/(float(ctrl_count)-1)
        #null group
        ctrl_Follicle_Group=cmds.group(em=True,n="Ctrl_Hair_Follicle_Group")
        ctrl_Follicles=[]
        
        for obj in range(ctrl_count):
            ctrl_fol=cmds.createNode("follicle")
            ctrl_foltransform=cmds.listRelatives(ctrl_fol,p=1)
            
            cmds.connectAttr(ctrl_shp[0]+".local",ctrl_fol+".inputSurface")
            cmds.connectAttr(ctrl_shp[0]+".worldMatrix",ctrl_fol+".inputWorldMatrix")
            
            cmds.connectAttr(ctrl_fol+".outRotate",ctrl_foltransform[0]+".rotate")
            cmds.connectAttr(ctrl_fol+".outTranslate",ctrl_foltransform[0]+".translate")
            #set paremeter v to middle of the surface
            
            cmds.setAttr(ctrl_fol+".parameterV",0.5)
            #set parameterU according to the length of surface
            cmds.setAttr(ctrl_fol+".parameterU",ctrl_placement*ctrl_j)
            
            ctrl_j+=1
            
            ctrl_Follicles.append(ctrl_foltransform[0])
            #Group the follicles
            
            cmds.parent(ctrl_foltransform[0],ctrl_Follicle_Group)
            
        #create joints on each follicle
        num=1
        Follicle_Control_Group=cmds.group(em=True,n=ctrl_sel[0]+"_Follicle_Ctrl_Group")
        for each in ctrl_Follicles:
            ctrl_jnt=cmds.createNode("joint",n=ctrl_sel[0]+"_"+str(num).zfill(2)+"_Ctrl_Jnt")
            cmds.matchTransform(ctrl_jnt,each)
            cmds.select(cl=1)
            
            ctrl=cmds.circle(ch=0,nr=(1,0,0),n=ctrl_sel[0]+"_"+str(num).zfill(2)+"_Ctrl")
            cmds.setAttr(ctrl[0]+".overrideEnabled",1)
            cmds.setAttr(ctrl[0]+".overrideColor",20)
            
            ctrl_grp=cmds.group(ctrl,n=ctrl_sel[0]+"_"+str(num).zfill(2)+"_Ctrl_Group")
            cmds.matchTransform(ctrl_grp,each)
            cmds.delete(each)
            cmds.parent(ctrl_grp,Follicle_Control_Group)
            
            cmds.parent(ctrl_jnt,ctrl)
            num+=1
        cmds.delete(ctrl_Follicle_Group)    
        ########################################
        #For creating Ribbon joints
        #########################################
        
        shp=cmds.listRelatives(ctrl_sel[0],s=True)
        if len(ctrl_sel)>1:
            cmds.error("select one surface at a time")
            
        jntcount=int(cmds.textFieldGrp(jnt_number, q=1, text=1))
        j=0
        placement=1/(float(jntcount)-1)
        #null group
        Follicle_Group=cmds.group(em=True,n=ctrl_sel[0]+"_Hair_Follicle_Group")
        Follicles=[]
        
        for obj in range(jntcount):
            fol=cmds.createNode("follicle",n=ctrl_sel[0]+"_"+str(num).zfill(2)+"_Follicle")
            foltransform=cmds.listRelatives(fol,p=1)
            
            cmds.connectAttr(shp[0]+".local",fol+".inputSurface")
            cmds.connectAttr(shp[0]+".worldMatrix",fol+".inputWorldMatrix")
            
            cmds.connectAttr(fol+".outRotate",foltransform[0]+".rotate")
            cmds.connectAttr(fol+".outTranslate",foltransform[0]+".translate")
            #set paremeter v to middle of the surface
            
            cmds.setAttr(fol+".parameterV",0.5)
            #set parameterU according to the length of surface
            cmds.setAttr(fol+".parameterU",placement*j)
            
            j+=1
            
            Follicles.append(foltransform[0])
            #Group the follicles
            
            cmds.parent(foltransform[0],Follicle_Group)
            
        #create joints on each follicle
        for each in Follicles:
            jnt=cmds.createNode("joint",n=ctrl_sel[0]+"_"+str(num).zfill(2)+"_Jnt")
            cmds.matchTransform(jnt,each)
            cmds.parent(jnt,each)
            
        if cmds.attributeQuery("GlobalScale",node=shp[0],exists=1):
            cmds.deleteAttr(shp[0],attribute="GlobalScale")
        gscale=cmds.addAttr(shp[0],ln="GlobalScale",dv=1,at="double",k=True)
        
        for i in Follicles:
            cmds.connectAttr(shp[0]+".GlobalScale",i+".sx")
            cmds.connectAttr(shp[0]+".GlobalScale",i+".sy")
            cmds.connectAttr(shp[0]+".GlobalScale",i+".sz")
        
        
   
###################################################################




def DynamicRig():

    #select FK controls in sequence and run the script
    
    
       
    import maya.cmds as cmds
    import maya.mel as mel
    sel=cmds.ls(sl=1)
    
    division=3
    if len(sel)<=3:
        division=1
    else:
        division=3
        
    
    if len(sel)<=2:
        cmds.warning("Please select atleast 3 objects in sequence")
        
    else:
         
        pointdata=[]
        jntset=[]
        grpset=[]
        for i in sel:
            
            pos=cmds.xform(i,q=1,ws=1,t=1)
            pointdata.append(pos)
            cmds.select(cl=1)
            dyn_jnt=cmds.joint(n=i+"_Dyn_Jnt")
            cmds.matchTransform(dyn_jnt,i)
            jntset.append(dyn_jnt)
            cmds.select(cl=1)
    
        
        
                  
        ref_crv= cmds.curve(p=pointdata,n=sel[0]+"reference_Crv",d=division)
        cmds.select(cl=1)
        cmds.matchTransform(ref_crv,sel[0],piv=True)
        
        #parents all dynamic joints hierarchy
        count=len(jntset)-1
            
        for i in range(count):
            cmds.parent(jntset[count],jntset[count-1])
            count-=1
        #Make Curves dynamic
        cmds.select(ref_crv)
        
        
        
        mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')
        
        #sort the wanted nodes and group them
        hairshapenodes=[]
        
        ref_crv_data=cmds.listConnections(ref_crv)
        history=cmds.listHistory(ref_crv_data[0],pdo=0)
        
        for i in history:
            if cmds.nodeType(i)=="follicle":
                hairshapenodes.append(i)
            elif cmds.nodeType(i)=="hairSystem":
                hairshapenodes.append(i)    
        print(hairshapenodes)
        
        #hairnodes=[follicleshapesnode,hairsystem shape node,follicle node,hairsystem node]
        #set the point lock to base
        cmds.setAttr(hairshapenodes[0]+".pointLock",1)
        hairnodes=[]
        for eachobject in hairshapenodes:
            nodes=cmds.listRelatives(eachobject,p=True)
            
            hairnodes.append(nodes)
        
        output_crv=cmds.listConnections(hairshapenodes[0])[-1]
        ikh=cmds.ikHandle(sj=jntset[0],ee=jntset[-1],c=output_crv,sol="ikSplineSolver",ccv=0)
        print(ikh)
        
        grp=cmds.group(hairnodes[0][0],hairnodes[1][0],n=sel[0]+"Hair_Follicle_Group",r=True)
        cmds.matchTransform(grp,sel[0],piv=True)
        
        
        #create base jnt parent all dynamic jnts ,follicle,hairsystem,curve under this base jnt
        
        
        
        
        
        
        dyn_grp=cmds.group(ikh[0],output_crv,n=sel[0]+"_Dyn_Deformers_Group")
        dyn_jnt_grp=cmds.group(jntset[0],r=True,n=sel[0]+"_Dyn_Jnt_Group")
        cmds.matchTransform(dyn_jnt_grp,jntset[0],piv=True)
        cmds.parent(grp,dyn_jnt_grp)
        cmds.select(cl=1)
        cmds.parent(dyn_jnt_grp,dyn_grp)
        
        
        cmds.delete(hairnodes[1][0]+"Follicles")
        cmds.delete(hairnodes[1][0]+"OutputCurves")
        cmds.refresh()
        
        
        
        
        #create attributes
        
        Dynamics_Header=cmds.addAttr(sel[0],ln="DynamicsSection",at="enum",en="------",k=True)
        
        cmds.setAttr(sel[0]+".DynamicsSection",l=True)
        Dynamics_switch=cmds.addAttr(sel[0],ln="Dynamics",at="bool",dv=1,k=True)
        
        Dynamics_attr=cmds.addAttr(sel[0],ln="Simulation",at="enum",en="Off:Static:DynamicFollicles:AllFollicles:",dv=3,k=True)
        pointlock=cmds.addAttr(sel[0],ln="PointLock",at="enum",en="NoAttach:Base:Tip:BothEnds:",dv=1,k=True)
        
        stretch_resistance=cmds.addAttr(sel[0],ln="Stretch_Resistance",at="float",dv=10,k=True)
        mass_attr=cmds.addAttr(sel[0],ln="Mass",at="float",dv=1,k=True)
        damp_attr=cmds.addAttr(sel[0],ln="Damp",at="float",dv=0,min=0,k=True)
        
        collide_Header=cmds.addAttr(sel[0],ln="CollideSection",at="enum",en="****:****",k=True)
        cmds.setAttr(sel[0]+".CollideSection",l=True)
        collide_attr= cmds.addAttr(sel[0],ln="Collide",at="bool",k=True,dv=1)
        collideself_attr = cmds.addAttr(sel[0],ln="SelfCollide",at="bool",k=True,dv=0)
        
        #connect to attributes
        cmds.connectAttr(sel[0]+".PointLock",hairshapenodes[0]+".pointLock")
        cmds.connectAttr(sel[0]+".Simulation",hairshapenodes[1]+".simulationMethod")
        cmds.connectAttr(sel[0]+".Stretch_Resistance",hairshapenodes[1]+".stretchResistance")
        cmds.connectAttr(sel[0]+".Mass",hairshapenodes[1]+".mass")
        cmds.connectAttr(sel[0]+".Mass",hairshapenodes[1]+".damp")
        cmds.connectAttr(sel[0]+".Collide",hairshapenodes[1]+".collide")
        cmds.connectAttr(sel[0]+".SelfCollide",hairshapenodes[1]+".selfCollide")
        
        
        
        for j in sel:
            sdk=cmds.group(j,n=j+"dyn_Offset_Group")
            cmds.matchTransform(sdk,j,piv=True)
            grpset.append(sdk)
            
        
        
        
        #connect dynamic rig to fk controls
        pcset=[]
        scset=[]
        for each,each2 in zip(jntset,grpset):
            sc=cmds.scaleConstraint(each,each2,mo=1)[0]
            pc=cmds.parentConstraint(each,each2,mo=1)[0]
            pcset.append(pc)
            scset.append(sc)
        for obj,obj2,obj3 in zip(pcset,scset,jntset):
            
            
            cmds.connectAttr(sel[0]+".Dynamics","{}.{}W0".format(obj,obj3))
            cmds.connectAttr(sel[0]+".Dynamics","{}.{}W0".format(obj2,obj3))
        
        
   




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

        
    


#select all controls then reference control curve and run the script
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
        
        





#select the objects in order you wish to parent
def parentSequence():
    import maya.cmds as cmds
    sel=cmds.ls(sl=1)

    count=len(sel)-1 #-1 is for range we need the parent function to work n-1 times.ex: if 3 objects we need to run the parent loop twice

    for i in range(count):
        cmds.parent(sel[count],sel[count-1])
        count-=1
        







def controlatpivot():
    # creates a control along with joint on each vertex/object selected.
    # when Local option is checked control follows the axis of object/vertex selected
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
    # creates  joint on each vertex/object selected
    # when Local option is checked joint follows the axis of object/vertex selected
    import maya.cmds as cmds
    
    
    sel = cmds.ls(sl=1)
    if len(sel)==0:
        cmds.warning("Please Select atleat 1 Object")
    else:    
        for i in sel:
            cmds.select(cl=1)
            jnt = cmds.joint()
            pointlocation = cmds.xform(i, q=True, ws=True, t=1)
            jntlocation = cmds.xform(jnt, ws=1, t=pointlocation)

    
            
            
    
        
        
        





def grouping():
    #select all objects and run the script
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
    # zeroout applies for list of selected items
    import maya.cmds as cmds
    sel = cmds.ls(sl=1)
    for i in sel:
        grp = cmds.group(i, em=True,n=i+"_Offset_Group")
        cmds.matchTransform(grp, i)
        cmds.parent(i, grp)



def follicleAtPivot():
    #creates follicle at each object/vertex selected
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
    #select only one surface at a time and run the script
    #Follicle control follows the respective surface
    
    

    
    
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
    global ctrl_number,jnt_number
    if cmds.window(name,exists=1):
        cmds.deleteUI(name)
    mywindow=cmds.window(name,width=350,height=700,sizeable=1)
    cmds.showWindow(mywindow)
    ############################
    wWidth=350
    wHeight=900
    
    cmds.columnLayout()
    cmds.button(label="Create Control at Each Vertex",c="controlatpivot()",width=wWidth,height=wHeight/18,bgc=(0,0.25,0.25))
    cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    
    
    cmds.checkBox("CGlobal",label="        Global",width=wWidth/2,height=wHeight/18)
    cmds.checkBox("CLocal",label="          Local",width=wWidth/2,height=wHeight/18)
    cmds.separator(width=5,height=5,style="in")
    cmds.setParent("..")
    
    cmds.columnLayout()
    cmds.button(label="Create Control at Each Pivot",c="jointatselection()",width=wWidth,height=wHeight/18,bgc=(0,0.2,0.2))
    
    cmds.setParent("..")
    
    cmds.columnLayout()
    
   
    cmds.button(label="Follicle at each Pivot",c="follicleAtPivot()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Follicle Control",c="follicelcontrol()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Parent Sequence",c="parentSequence()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="ZeroOut",c="Zeroout()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Create/Add Blendshape",c="create_AddBlendshape()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Group",c="grouping()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    cmds.button(label="Swap Control Shapes",c="swapControlCurves()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    
    cmds.setParent("..")
    cmds.frameLayout( label='Ribbon Rig', labelAlign='center',cll=True,bgc=(.7,.4,.1),cl=1,w=wWidth)
    cmds.columnLayout()
    ctrl_number=cmds.textFieldGrp( label='Controls', text='5',w=wWidth)
    jnt_number=cmds.textFieldGrp( label='Ribbon Joints', text='50',w=wWidth)
    cmds.button(label="Create Ribbon Rig",c="ribbonjoints()",w=350,h=wHeight/20,bgc=(0,0.25,0.25))
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.button(label="Dynamic FK Rig",c="DynamicRig()",width=wWidth,height=wHeight/20,bgc=(0,0.25,0.25))
    
    
    
customwindow("Rigging Tools V2.3 - RameshDarisi")
    
