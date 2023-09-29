#creates Controls on the ribbon




##############################################################

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

def customwindow(name):
    global ctrl_number,jnt_number
    if cmds.window(name,exists=1):
        cmds.deleteUI(name)
    mywindow=cmds.window(name,width=350,height=500,sizeable=1)
    cmds.showWindow(mywindow)
    ############################
    W=350
    H=500
    cmds.columnLayout()
    #cmds.rowColumnLayout(numberOfColumns=3,columnOffset=(1,"left",2))
    
    ctrl_number=cmds.textFieldGrp( label='Controls', text='5',w=W)
    jnt_number=cmds.textFieldGrp( label='Ribbon Joints', text='50',w=W)
    
    
    
    
    
    cmds.setParent("..")
    cmds.columnLayout()
    
    
    cmds.button(label="Create Ribbon Rig",c="ribbonjoints()",w=350,h=H/10,bgc=(0.7,0.4,0.1))
    
    
    cmds.setParent("..")
        
customwindow("RibbonRig_v1.0--RD") 
         
