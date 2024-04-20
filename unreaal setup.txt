from maya.cmds import*
#prints out all geomteries of the selected group
geolist=[]

xyz=ls("Geometry",dag=True,type="mesh")

for each in xyz:
   k=listRelatives(each,p=True)[0]
   geolist.append(k)
geolist=set(geolist)
print(len(geolist)) 

#query the geo that has skin cluster nodes and group into new set
    
skinclusterlist=[]

for object in geolist:
    hist=cmds.listHistory(object)
    
    for xyz in hist:
        if objectType(xyz)=="skinCluster":
            skinclusterlist.append(xyz)
        
print(skinclusterlist)
print(len(skinclusterlist))

#####################################################################
bindjntlist=[]
#identify bind joints of each geometry
bindjntlist=[]
for item in skinclusterlist:
    bindjnts=cmds.skinCluster(item,q=True,inf=True)
    for jnt in bindjnts:
        bindjntlist.append(jnt)
    
bindjntlist=set(bindjntlist)
print(bindjntlist)

#create new skin joints in plce of bind jnts

newskinjntlist=[]
unreal_root=joint(n="Unreal_Root_Jnt")
for oldjnt in bindjntlist:
     cmds.select(cl=1)
     skinjnt=joint(n="Skin_"+oldjnt)
     matchTransform(skinjnt,oldjnt)
     parentConstraint(oldjnt,skinjnt,mo=1)
     scaleConstraint(oldjnt,skinjnt,mo=1)
     parent(skinjnt,unreal_root)
newskinjntlist.append(skinjnt)
select(cl=1)



####################################################################
#add new skin joint weights to each geometry


#cmds.skinCluster("skinCluster2",edit=True,ai=('n_Jnt','n_Jnt1'),lw=True,wt=0)

for obj in skinclusterlist:
    
    bindjntlist=cmds.skinCluster(obj,q=True,inf=True)
    new_skinjntlist=[]
    
    
    for i in bindjntlist:
        nskinjnts="Skin_"+i
        new_skinjntlist.append(nskinjnts)
    cmds.skinCluster(obj,edit=True,ai=new_skinjntlist,lw=True,wt=0)
    connections = listConnections(obj, c=1, d=1, type="mesh")
    if connections:
        associated_geo = connections[1]
        # Rest of your code that uses associated_geo
    
        select(associated_geo+".vtx[*]")
        for old_jnt, new_jnt in zip(bindjntlist, new_skinjntlist):
            setAttr(old_jnt+".liw",0)
            setAttr(new_jnt+".liw",0)
            cmds.skinPercent(obj, tmw=[old_jnt, new_jnt])
    
        
        cmds.select(cl=1)
            
    else:
        print("No associated geometry found for", obj)   
    



