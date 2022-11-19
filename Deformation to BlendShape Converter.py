import maya.cmds as cmds

class My_Window(object):
        
    #constructor
    def __init__(self):
            
        self.window = "My_Window"
        self.title = "Deformation to BS Converter_v1.0------Ramesh Darisi"
        self.size = (400, 400)
       
        
        
            
        # close old window is open
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            
        #create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        
        cmds.columnLayout(adjustableColumn=1)
        cmds.text(self.title)
        cmds.separator(height=20)
        cmds.text("Selct Geo amd run the Initialise Button(Run this only once) ")
        cmds.button(label="Initialise",w=300,c = self.Initialise)
        cmds.separator(height=20)
        cmds.text("Run the script by Selecting single control and Geometry ")
        cmds.separator(height=20)
        
        self.proxygeo=cmds.textFieldGrp(label="ProxyMesh: ",text="")
        self.proxyBS=cmds.textFieldGrp(label="BlendShapeNode",text="")
        self.BS_value=cmds.floatFieldGrp(label='BS_TranslateValue',numberOfFields=1,value1=5 )
        self.BS_Rotatevalue=cmds.floatFieldGrp(label='BS_RotateValue',numberOfFields=1,value1=180 )
        self.CI_value=cmds.floatFieldGrp(label='Control_Order',numberOfFields=1,value1=0)
        
        cmds.button(label="BStoSkinConvert",w=300,c = self.BStoSkinConvert)
        

        cmds.showWindow()
        
        
        
    def Initialise(self,*args):
        sel=cmds.ls(sl=1)
        
        if len(sel)==0:
            print("Please select Main Geometry  and then run initialise Button")
        
        elif len(sel)>1:
            print("please selct only one geometry mesh." )
        
        else:
            
            proxy_mesh=cmds.duplicate(sel[0],n=sel[0]+"_proxy")
            BS=cmds.blendShape(proxy_mesh, frontOfChain=True, n=proxy_mesh[0] + "_BS")
            cmds.setAttr(proxy_mesh[0]+".visibility",0,lock=True)
            
    
        
        
    def BStoSkinConvert(self,*args):
        global num
        sel = cmds.ls(sl=1)
        value = cmds.floatFieldGrp(self.BS_value,q=True,value1=True) 
        value02 = cmds.floatFieldGrp(self.BS_Rotatevalue,q=True,value1=True)  
        control_index=cmds.floatFieldGrp(self.CI_value,q=True,value1=True)
        print(value)
        print(control_index) 
        
        cc=control_index*6
        
        geoset = []
        newset = []
        proxy = cmds.textFieldGrp(self.proxygeo,q=1,text=True)
        bs_node =cmds.textFieldGrp(self.proxyBS,q=1,text=True)
        
        attributes = [".translateX", ".translateY", ".translateZ", ".rotateX", ".rotateY", ".rotateZ"]
        
        #num=0 
        ######################################################
        cmds.setAttr(sel[0] + ".translateX", value)
    
        geo_01 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}translateX_{value}")
        geoset.append(geo_01)
        cmds.setAttr(sel[0] + ".translateX",0)
        #cmds.setAttr(geo_01[0] + ".visibility", 0, lock=True)
        
        
    ################################################
        cmds.setAttr(sel[0] + ".translateY", value)
        geo_02 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}translateY_{value}")
        geoset.append(geo_02)
        cmds.setAttr(sel[0] + ".translateY",0)
        #cmds.setAttr(geo_02[0] + ".visibility", 0, lock=True)
  ######################################################### 
        cmds.setAttr(sel[0] + ".translateZ", value)
        geo_03 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}translateZ_{value}")
        geoset.append(geo_03)
        cmds.setAttr(sel[0] + ".translateZ",0)
        #cmds.setAttr(geo_03[0] + ".visibility", 0, lock=True)
  ###############################################################
        cmds.setAttr(sel[0] + ".rotateX", value02)
        geo_04 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}rotateX_{value02}")
        geoset.append(geo_04)
        cmds.setAttr(sel[0] + ".rotateX",0)
        #cmds.setAttr(geo_04[0] + ".visibility", 0, lock=True)
########################################################################
        cmds.setAttr(sel[0] + ".rotateY", value02)
        geo_05 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}rotateY_{value02}")
        geoset.append(geo_05)
        cmds.setAttr(sel[0] + ".rotateY",0)
        #cmds.setAttr(geo_05[0] + ".visibility", 0, lock=True)
 ############################################################################
        cmds.setAttr(sel[0] + ".rotateZ", value02)
        geo_06 = cmds.duplicate(sel[-1], name=f"{sel[-1]}_{sel[0]}rotateZ_{value02}")
        geoset.append(geo_06)
        cmds.setAttr(sel[0] + ".rotateZ",0)
        #cmds.setAttr(geo_06[0] + ".visibility", 0, lock=True)
    
        
     
        
  
  ##########################################################     
        
        
        print(geoset)
        for obj in range(len(geoset)):
            newset.append(geoset[obj][0])
        print(newset)
        ################################################################################
        #bs_node = cmds.blendShape(proxy, frontOfChain=True, n=proxy + "_BS")
        
        num = 0
        
        
        for nobj in newset:
            shapes=cmds.blendShape(bs_node, e=True, t=(proxy, cc, nobj, 1))
            
            # deletes duplicated geometries
            cmds.delete(newset[num])
            num += 1
            cc += 1
        print(cc)
              
        ################################################################################
        cmds.select(cl=1)
        ################################################################################
        count=0
        for i in newset:
            cmds.setAttr(sel[0]+attributes[count],(value*-1))
            cmds.setAttr(bs_node+"."+i,-1)
            cmds.setDrivenKeyframe(bs_node+"."+i,cd=sel[0]+attributes[count])
        
            cmds.setAttr(sel[0]+attributes[count],value)
            cmds.setAttr(bs_node+"."+i,1)
            cmds.setDrivenKeyframe(bs_node+"."+i,cd=sel[0]+attributes[count])
            
            cmds.setAttr(sel[0]+attributes[count],0)
            cmds.setAttr(bs_node+"."+i,0)
            cmds.setDrivenKeyframe(bs_node+"."+i,cd=sel[0]+attributes[count])
            count+=1 
            #scale sdk fix
            
             
       
        
      
        
        control_index+=1
        #reset scale values
        
        cmds.select(cl=1)
        
    
        
        
        
            
            
            
         
    
    
            
            
           
            
            
            
            #display new window
            
                                   
myWindow = My_Window()  
            
            
            
            
            
                
            
          

