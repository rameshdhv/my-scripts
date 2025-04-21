"""
Maya Skin Weights Relax Tool(for Maya 2020 and upper versions)
with progress bar for working with large numbers of vertices

Usage:
1. Select skinned vertices
2. Run the script from Maya's script editor
3. Use the UI to apply relaxation

Author: Ramesh Darisi
"""

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import functools

class SkinRelaxTool:
    def __init__(self):
        self.window_name = "skinRelaxToolWindow"
        self.progress_canceled = False
        self.create_ui()
        
    def create_ui(self):
        # Check if window exists and delete it
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
            
        # Create window
        cmds.window(self.window_name, title="Skin Weights Relax Tool", width=300, height=300)
        
        # Create main layout
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=["both", 5])
        
        # Influences layout
        cmds.frameLayout(label="Influences", collapsable=True, collapse=False)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        
        # Only use all influences
        cmds.text(label="Using all influences for relaxation")
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Relax options layout
        cmds.frameLayout(label="Relax Options", collapsable=True, collapse=False)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        
        # Intensity slider - display from 0 to 1 (user-friendly)
        cmds.text(label="Intensity (1.0 = Maximum strength):")
        self.intensity_slider = cmds.floatSliderGrp(field=True, minValue=0.0, maxValue=1.0, fieldMinValue=0.0, 
                                                   fieldMaxValue=1.0, value=0.1, step=0.01, precision=2)
        
        # Iterations slider
        cmds.text(label="Iterations:")
        self.iterations_slider = cmds.intSliderGrp(field=True, minValue=1, maxValue=10, 
                                                  fieldMinValue=1, fieldMaxValue=100, value=1, step=1)
        
        # Volume control checkbox
        self.volume_checkbox = cmds.checkBox(label="Preserve volume", value=True)
        
        # Only use selection
        cmds.text(label="Area: Using selection")
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Progress section
        cmds.frameLayout(label="Progress", collapsable=False, collapse=False)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        
        # Progress bar and status
        self.progress_bar = cmds.progressBar(maxValue=100, width=290, visible=False)
        self.status_text = cmds.text(label="Ready", align="center", width=290)
        self.cancel_button = cmds.button(label="Cancel", command=self.cancel_operation, visible=False)
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Buttons
        self.apply_button = cmds.button(label="Apply", command=self.apply_relax)
        cmds.button(label="Close", command=lambda x: cmds.deleteUI(self.window_name))
        
        # Display the window
        cmds.showWindow(self.window_name)
    
    def cancel_operation(self, *args):
        """Cancel the current operation"""
        self.progress_canceled = True
    
    def setup_progress(self, title, max_progress):
        """Setup the progress bar in the UI"""
        # Reset cancel flag
        self.progress_canceled = False
        
        # Update UI
        cmds.progressBar(self.progress_bar, edit=True, maxValue=max_progress, progress=0, visible=True)
        cmds.text(self.status_text, edit=True, label=title)
        cmds.button(self.cancel_button, edit=True, visible=True)
        cmds.button(self.apply_button, edit=True, enable=False)
        
        # Force UI update
        cmds.refresh(force=True)
    
    def update_progress(self, progress, status=None):
        """Update the progress bar"""
        cmds.progressBar(self.progress_bar, edit=True, progress=progress)
        if status:
            cmds.text(self.status_text, edit=True, label=status)
        
        # Force UI update to show progress
        cmds.refresh(force=True)
        
        # Return True to continue, False if user requested cancel
        return not self.progress_canceled
    
    def end_progress(self):
        """Reset the progress UI elements"""
        cmds.progressBar(self.progress_bar, edit=True, visible=False, progress=0)
        cmds.text(self.status_text, edit=True, label="Ready")
        cmds.button(self.cancel_button, edit=True, visible=False)
        cmds.button(self.apply_button, edit=True, enable=True)
        
        # Force UI update
        cmds.refresh(force=True)
    
    def get_skin_cluster(self, mesh):
        """Get the skinCluster node for a given mesh"""
        if not mesh:
            return None
            
        skin_clusters = cmds.ls(cmds.listHistory(mesh), type='skinCluster')
        if skin_clusters:
            return skin_clusters[0]
        return None
    
    def get_influences(self, skin_cluster):
        """Get all influences for a skinCluster"""
        return cmds.skinCluster(skin_cluster, query=True, influence=True)
    
    def get_selected_influence(self):
        """Get currently selected influence in the scene"""
        selection = cmds.ls(selection=True, type='joint')
        if selection:
            return selection[0]
        return None
    
    def get_component_selection(self):
        """Get selected components"""
        selection = cmds.ls(selection=True, flatten=True)
        if not selection:
            return None, None
            
        # Check if selection is a mesh or components
        if '.vtx[' in selection[0]:
            # Handle vertex selection
            mesh_name = selection[0].split('.')[0]
            vertices = []
            for vtx in selection:
                # Handle range selections like pCube1.vtx[1:10]
                if ':' in vtx:
                    parts = vtx.split('[')[1].split(']')[0].split(':')
                    start = int(parts[0])
                    end = int(parts[1])
                    vertices.extend(range(start, end + 1))
                else:
                    vertices.append(int(vtx.split('[')[1].split(']')[0]))
            return mesh_name, vertices
        elif cmds.objectType(selection[0], isType='transform') or cmds.objectType(selection[0], isType='mesh'):
            # Handle mesh selection
            mesh_shapes = cmds.listRelatives(selection[0], shapes=True, type='mesh') or []
            if mesh_shapes:
                mesh_name = selection[0]
                # Get all vertices
                num_vertices = cmds.polyEvaluate(mesh_name, vertex=True)
                vertices = list(range(num_vertices))
                return mesh_name, vertices
                
        return None, None
    
    def get_connected_vertices(self, mesh, vertex_index):
        """Get connected vertices for a given vertex"""
        vertex_path = f"{mesh}.vtx[{vertex_index}]"
        connected_edges = cmds.polyListComponentConversion(vertex_path, fromVertex=True, toEdge=True)
        if not connected_edges:
            return []
            
        connected_vertices = cmds.polyListComponentConversion(connected_edges, fromEdge=True, toVertex=True)
        connected_vertices_indices = []
        
        if connected_vertices:
            flattened = cmds.ls(connected_vertices, flatten=True)
            for vtx in flattened:
                if '.vtx[' in vtx:
                    index = int(vtx.split('[')[1].split(']')[0])
                    if index != vertex_index:  # Exclude self
                        connected_vertices_indices.append(index)
        return connected_vertices_indices
    
    def get_skin_weights(self, skin_cluster, mesh, vertex_indices):
        """Get skin weights for given vertices using API for better performance and reliability"""
        weights = {}
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        influence_indices = {}
        
        # Get influence indices
        for i, infl in enumerate(influences):
            influence_indices[infl] = i
        
        # Create an MSelectionList to get the DAG path of the mesh
        sel_list = om.MSelectionList()
        sel_list.add(mesh)
        dag_path = om.MDagPath()
        sel_list.getDagPath(0, dag_path)
        
        # Get skin cluster object
        skin_sel_list = om.MSelectionList()
        skin_sel_list.add(skin_cluster)
        skin_obj = om.MObject()
        skin_sel_list.getDependNode(0, skin_obj)
        skin_node = oma.MFnSkinCluster(skin_obj)
        
        # Process vertices in batches with progress updates
        vertices_count = len(vertex_indices)
        processed = 0
        batch_size = self.calculate_optimal_batch_size(vertices_count)  # Use dynamic batch size
        
        # Update progress bar
        self.update_progress(0, f"Loading weights: 0/{vertices_count} vertices")
        
        for batch_start in range(0, vertices_count, batch_size):
            batch_end = min(batch_start + batch_size, vertices_count)
            batch_vertices = vertex_indices[batch_start:batch_end]
            
            # Create a single component for the entire batch
            batch_comp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
            for vertex in batch_vertices:
                om.MFnSingleIndexedComponent(batch_comp).addElement(vertex)
            
            # Get weights for all influences in the batch
            mweights = om.MDoubleArray()
            util = om.MScriptUtil()
            util.createFromInt(0)
            ptr = util.asUintPtr()
            
            skin_node.getWeights(dag_path, batch_comp, mweights, ptr)
            
            # Parse weights for each vertex in the batch
            for i, vertex in enumerate(batch_vertices):
                weight_dict = {}
                for infl, idx in influence_indices.items():
                    weight_index = i * len(influences) + idx
                    if weight_index < mweights.length():
                        weight = mweights[weight_index]
                        if weight > 0.0001:  # Only store non-zero weights for efficiency
                            weight_dict[infl] = weight
                
                weights[vertex] = weight_dict
            
            # Update progress
            processed += len(batch_vertices)
            progress_pct = int(100.0 * processed / vertices_count)
            if not self.update_progress(progress_pct, f"Loading weights: {processed}/{vertices_count} vertices ({progress_pct}%)"):
                return None, None  # User cancelled
        
        return weights, influences
    
    def relax_weights(self, mesh, skin_cluster, vertex_indices, influences, intensity, preserve_volume=True):
        """Relax skin weights for specified vertices and influences with progress tracking"""
        # Get original weights
        original_weights, all_influences = self.get_skin_weights(skin_cluster, mesh, vertex_indices)
        if original_weights is None:  # User cancelled during weight loading
            return None
            
        # Filter influences if needed
        if influences[0] != 'all':
            active_influences = influences
        else:
            active_influences = all_influences
            
        new_weights = {}
        
        # Initialize new weights with original values
        for vertex in vertex_indices:
            new_weights[vertex] = {infl: original_weights[vertex].get(infl, 0.0) for infl in active_influences}
        
        # Update progress bar for relaxation phase
        vertices_count = len(vertex_indices)
        self.update_progress(0, f"Relaxing weights: 0/{vertices_count} vertices")
        
        # Process vertices in batches with progress updates
        processed = 0
        batch_size = self.calculate_optimal_batch_size(vertices_count)
        
        # Cache vertex connections to avoid redundant queries
        connection_cache = {}
        
        # Normalize intensity for internal calculations (1.0 is the standard strength)
        # Values > 1.0 will provide stronger effects for high-resolution meshes
        normalized_intensity = min(intensity, 10.0) / 10.0
        
        for batch_start in range(0, vertices_count, batch_size):
            batch_end = min(batch_start + batch_size, vertices_count)
            batch_vertices = vertex_indices[batch_start:batch_end]
            
            for vertex in batch_vertices:
                # Get connected vertices (from cache if available)
                if vertex in connection_cache:
                    connected_vertices = connection_cache[vertex]
                else:
                    connected_vertices = self.get_connected_vertices(mesh, vertex)
                    connected_vertices = [v for v in connected_vertices if v in vertex_indices]
                    connection_cache[vertex] = connected_vertices
                
                if not connected_vertices:
                    continue
                    
                # Calculate average weights from neighbors
                avg_weights = {}
                for infl in active_influences:
                    neighbor_sum = sum(original_weights[neighbor].get(infl, 0.0) for neighbor in connected_vertices if neighbor in original_weights)
                    avg_weights[infl] = neighbor_sum / len(connected_vertices) if connected_vertices else 0.0
                
                # For intensity > 1.0, we increase the effect by applying a progressive curve
                effect_intensity = normalized_intensity
                if intensity > 1.0:
                    # Apply stronger smoothing for higher intensity values
                    effect_intensity = min(intensity / 1.0, 1.0)  # Cap at 1.0 for blending
                
                # Blend original with averaged weights based on intensity
                for infl in active_influences:
                    original = original_weights[vertex].get(infl, 0.0)
                    average = avg_weights.get(infl, 0.0)
                    new_weights[vertex][infl] = original * (1.0 - effect_intensity) + average * effect_intensity
            
                # For high-intensity values (>1.0), apply additional passes of smoothing
                if intensity > 1.0:
                    extra_passes = int(intensity) - 1
                    temp_weights = dict(new_weights[vertex])
                    
                    for _ in range(extra_passes):
                        # Calculate average of current iteration
                        refined_avg = {}
                        for neighbor in connected_vertices:
                            if neighbor in original_weights:
                                for infl in active_influences:
                                    if infl not in refined_avg:
                                        refined_avg[infl] = 0.0
                                    # Use the current iteration's weights for neighbors 
                                    # that have already been processed
                                    if neighbor < vertex and neighbor in new_weights:
                                        refined_avg[infl] += new_weights[neighbor].get(infl, 0.0)
                                    else:
                                        refined_avg[infl] += original_weights[neighbor].get(infl, 0.0)
                        
                        # Normalize the refined averages
                        for infl in refined_avg:
                            refined_avg[infl] /= len(connected_vertices)
                        
                        # Apply additional blending
                        blend_factor = 0.5  # Less aggressive for additional passes
                        for infl in active_influences:
                            current = temp_weights.get(infl, 0.0)
                            refined = refined_avg.get(infl, 0.0)
                            temp_weights[infl] = current * (1.0 - blend_factor) + refined * blend_factor
                    
                    # Update with the result of multiple passes
                    new_weights[vertex] = temp_weights
                
                # Normalize weights for this vertex
                total = sum(new_weights[vertex].values())
                if total > 0:
                    scale_factor = 1.0 / total
                    for infl in active_influences:
                        new_weights[vertex][infl] *= scale_factor
                
                # Apply volume preservation if enabled
                if preserve_volume:
                    # This is a simplified volume preservation approach
                    significant_threshold = 0.1
                    for infl in active_influences:
                        orig_weight = original_weights[vertex].get(infl, 0.0)
                        if orig_weight > significant_threshold:
                            # Limit change for significant influences, but scale by intensity
                            max_change = 0.5 * min(intensity, 1.0)  # Cap at 0.5 for high intensities
                            new_weight = new_weights[vertex][infl]
                            clamped_weight = max(min(new_weight, orig_weight + max_change), orig_weight - max_change)
                            new_weights[vertex][infl] = clamped_weight
                    
                    # Re-normalize after volume preservation
                    total = sum(new_weights[vertex].values())
                    if total > 0:
                        scale_factor = 1.0 / total
                        for infl in active_influences:
                            new_weights[vertex][infl] *= scale_factor
            
            # Update progress
            processed += len(batch_vertices)
            progress_pct = int(100.0 * processed / vertices_count)
            if not self.update_progress(progress_pct, f"Relaxing weights: {processed}/{vertices_count} vertices ({progress_pct}%)"):
                return None  # User cancelled
        
        return new_weights
    
    def apply_weights(self, skin_cluster, mesh, new_weights):
        """Apply calculated weights to the skin cluster using the Maya API with progress tracking"""
        if new_weights is None:  # User cancelled during relaxation
            return False
            
        # Create an MSelectionList to get the DAG path of the mesh
        sel_list = om.MSelectionList()
        sel_list.add(mesh)
        dag_path = om.MDagPath()
        sel_list.getDagPath(0, dag_path)
        
        # Get skin cluster object
        skin_sel_list = om.MSelectionList()
        skin_sel_list.add(skin_cluster)
        skin_obj = om.MObject()
        skin_sel_list.getDependNode(0, skin_obj)
        skin_node = oma.MFnSkinCluster(skin_obj)
        
        # Get influences
        influence_objects = om.MDagPathArray()
        influence_count = skin_node.influenceObjects(influence_objects)
        
        # Create influence indices map
        influence_indices = {}
        for i in range(influence_count):
            influence_name = influence_objects[i].partialPathName()
            influence_indices[influence_name] = i
        
        # Group vertices by their influence sets for efficiency
        influence_groups = {}
        for vertex, weights in new_weights.items():
            weight_keys = tuple(sorted(weights.keys()))
            if weight_keys not in influence_groups:
                influence_groups[weight_keys] = []
            influence_groups[weight_keys].append((vertex, weights))
        
        # Update progress bar for weight application phase
        total_vertices = len(new_weights)
        vertices_applied = 0
        self.update_progress(0, f"Applying weights: 0/{total_vertices} vertices")
        
        # Process each influence group
        for influences, vertex_weight_pairs in influence_groups.items():
            if not influences:
                continue
                
            # Calculate optimal batch size based on vertex count
            batch_size = self.calculate_optimal_batch_size(len(vertex_weight_pairs))
            
            # Process in smaller batches for better progress updates
            for batch_start in range(0, len(vertex_weight_pairs), batch_size):
                batch_end = min(batch_start + batch_size, len(vertex_weight_pairs))
                batch_vertex_weights = vertex_weight_pairs[batch_start:batch_end]
                
                # Create vertex component for this batch
                vertex_indices = [vw[0] for vw in batch_vertex_weights]
                component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
                for vertex in vertex_indices:
                    om.MFnSingleIndexedComponent(component).addElement(vertex)
                
                # Create influence array
                influence_array = om.MIntArray(len(influences))
                for i, infl in enumerate(influences):
                    if infl in influence_indices:
                        influence_array.set(influence_indices[infl], i)
                
                # Create weight array (vertices × influences)
                weight_array = om.MDoubleArray(len(vertex_indices) * len(influences))
                for i, (vertex, weights) in enumerate(batch_vertex_weights):
                    for j, infl in enumerate(influences):
                        weight = weights.get(infl, 0.0)
                        weight_array.set(weight, i * len(influences) + j)
                
                # Set the weights - using normalize=False to prevent locked influence warnings
                try:
                    # Make sure weights are already normalized to avoid the warning
                    skin_node.setWeights(dag_path, component, influence_array, weight_array, normalize=False)
                except Exception as e:
                    # Fall back to per-vertex setting if batch fails
                    for vertex, weights in batch_vertex_weights:
                        self.apply_single_vertex_weights(skin_cluster, mesh, vertex, weights)
                
                # Update progress
                vertices_applied += len(batch_vertex_weights)
                progress_pct = int(100.0 * vertices_applied / total_vertices)
                if not self.update_progress(progress_pct, f"Applying weights: {vertices_applied}/{total_vertices} vertices ({progress_pct}%)"):
                    return False  # User cancelled
        
        return True
    
    def calculate_optimal_batch_size(self, vertices_count):
        """Calculate optimal batch size based on vertex count"""
        if vertices_count <= 1000:
            # For small selection, use larger batches for speed
            return min(500, vertices_count)
        elif vertices_count <= 10000:
            # For medium selections, use moderate batches
            return min(300, vertices_count)
        elif vertices_count <= 50000:
            # For large selections, use smaller batches for better UI responsiveness
            return 200
        else:
            # For very large selections, use minimal batch sizes
            return 100
    
    def apply_single_vertex_weights(self, skin_cluster, mesh, vertex, weights):
        """Fallback method to set weights for a single vertex using cmds"""
        # Filter out zero weights for efficiency
        non_zero_weights = [(infl, weight) for infl, weight in weights.items() if weight > 0.0001]
        
        if non_zero_weights:
            vertex_path = f"{mesh}.vtx[{vertex}]"
            # Use normalize=False to prevent locked influence warnings, since we've already normalized the weights
            cmds.skinPercent(skin_cluster, vertex_path, transformValue=non_zero_weights, normalize=False)
    
    def apply_relax(self, *args):
        """Main function to apply relaxation based on UI settings"""
        # Get UI values
        ui_intensity = cmds.floatSliderGrp(self.intensity_slider, query=True, value=True)
        # Scale UI intensity (0-1) to internal intensity (0-10)
        intensity = ui_intensity * 10.0 
        iterations = cmds.intSliderGrp(self.iterations_slider, query=True, value=True)
        preserve_volume = cmds.checkBox(self.volume_checkbox, query=True, value=True)
        use_selection = True  # Always use selection
        all_influences_selected = True  # Always use all influences
        
        # Get mesh and vertices
        mesh, vertices = self.get_component_selection()
        if not mesh or not vertices:
            cmds.warning("Nothing selected. Please select a skinned mesh or components.")
            return
        
        # Get skin cluster
        skin_cluster = self.get_skin_cluster(mesh)
        if not skin_cluster:
            cmds.warning(f"No skinCluster found on {mesh}")
            return
        
        # Get influences
        if all_influences_selected:
            influences = ['all']
        else:
            selected_influence = self.get_selected_influence()
            if not selected_influence:
                cmds.warning("No influence selected. Please select a joint or use 'All influences' option.")
                return
            influences = [selected_influence]
        
        # Initialize progress UI
        try:
            cmds.waitCursor(state=True)
            
            # Set up UI for progress tracking
            self.setup_progress(f"Relaxing {len(vertices)} vertices", 100)  # Always 0-100%
            
            # Get original weights - we'll need these as a starting point
            original_weights, all_influences = self.get_skin_weights(skin_cluster, mesh, vertices)
            if original_weights is None:  # User cancelled during weight loading
                cmds.warning("Operation cancelled by user")
                self.end_progress()
                cmds.waitCursor(state=False)
                return
                
            # Filter influences if needed
            if influences[0] != 'all':
                active_influences = influences
            else:
                active_influences = all_influences
            
            # Initialize current weights with original weights
            current_weights = {}
            for vertex in vertices:
                current_weights[vertex] = {infl: original_weights[vertex].get(infl, 0.0) for infl in active_influences}
            
            # Process all iterations internally without updating the viewport
            for i in range(iterations):
                iteration_str = f"Iteration {i+1}/{iterations}"
                self.update_progress(i * (100 / iterations), f"{iteration_str} - Processing...")
                
                # Process this iteration (starting from current weights)
                # We'll use a modified relax_weights function that takes current weights as input
                new_weights = self.relax_weights_iteration(mesh, skin_cluster, vertices, 
                                                         active_influences, intensity, 
                                                         current_weights, original_weights,
                                                         preserve_volume)
                
                if new_weights is None:
                    cmds.warning("Operation cancelled by user")
                    break
                
                # Update current weights for next iteration
                current_weights = new_weights
                
                # Update progress
                self.update_progress((i + 0.5) * (100 / iterations), f"{iteration_str} - Completed")
                
                # Check if user cancelled
                if self.progress_canceled:
                    cmds.warning("Operation cancelled by user")
                    break
            
            # Apply the final weights only once
            if not self.progress_canceled:
                self.update_progress(99, f"Applying final weights...")
                result = self.apply_weights(skin_cluster, mesh, current_weights)
                if not result:
                    cmds.warning("Operation cancelled during final application")
            
            # Reset progress UI
            self.end_progress()
            
            # Re-select the vertices that were relaxed to stay in vertex selection mode
            vertex_selection = [f"{mesh}.vtx[{v}]" for v in vertices]
            cmds.select(vertex_selection)
            cmds.inViewMessage(amg=f"Relaxed weights applied ({iterations} iterations)", pos='midCenter', fade=True)
        except Exception as e:
            self.end_progress()
            cmds.warning(f"Error applying relaxation: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            cmds.waitCursor(state=False)
    
    def relax_weights_iteration(self, mesh, skin_cluster, vertex_indices, active_influences, 
                              intensity, current_weights, original_weights, preserve_volume=True):
        """Process a single relaxation iteration using current weights as input"""
        # This is a modified version of relax_weights that doesn't need to query weights from Maya
        new_weights = {}
        
        # Initialize new weights with current values
        for vertex in vertex_indices:
            new_weights[vertex] = {infl: current_weights[vertex].get(infl, 0.0) for infl in active_influences}
        
        # Process vertices in batches with progress updates
        vertices_count = len(vertex_indices)
        batch_size = self.calculate_optimal_batch_size(vertices_count)
        
        # Cache vertex connections to avoid redundant queries
        connection_cache = {}
        
        # Normalize intensity for internal calculations (1.0 is the standard strength)
        # Values > 1.0 will provide stronger effects for high-resolution meshes
        normalized_intensity = min(intensity, 10.0) / 10.0
        
        for batch_start in range(0, vertices_count, batch_size):
            batch_end = min(batch_start + batch_size, vertices_count)
            batch_vertices = vertex_indices[batch_start:batch_end]
            
            for vertex in batch_vertices:
                # Get connected vertices (from cache if available)
                if vertex in connection_cache:
                    connected_vertices = connection_cache[vertex]
                else:
                    connected_vertices = self.get_connected_vertices(mesh, vertex)
                    connected_vertices = [v for v in connected_vertices if v in vertex_indices]
                    connection_cache[vertex] = connected_vertices
                
                if not connected_vertices:
                    continue
                    
                # Calculate average weights from neighbors
                avg_weights = {}
                for infl in active_influences:
                    neighbor_sum = sum(current_weights[neighbor].get(infl, 0.0) for neighbor in connected_vertices if neighbor in current_weights)
                    avg_weights[infl] = neighbor_sum / len(connected_vertices) if connected_vertices else 0.0
                
                # For intensity > 1.0, we increase the effect by applying a progressive curve
                effect_intensity = normalized_intensity
                if intensity > 1.0:
                    # Apply stronger smoothing for higher intensity values
                    effect_intensity = min(intensity / 1.0, 1.0)  # Cap at 1.0 for blending
                
                # Blend current with averaged weights based on intensity
                for infl in active_influences:
                    current = current_weights[vertex].get(infl, 0.0)
                    average = avg_weights.get(infl, 0.0)
                    new_weights[vertex][infl] = current * (1.0 - effect_intensity) + average * effect_intensity
            
                # For high-intensity values (>1.0), apply additional passes of smoothing
                if intensity > 1.0:
                    extra_passes = int(intensity) - 1
                    temp_weights = dict(new_weights[vertex])
                    
                    for _ in range(extra_passes):
                        # Calculate average of current iteration
                        refined_avg = {}
                        for neighbor in connected_vertices:
                            if neighbor in current_weights:
                                for infl in active_influences:
                                    if infl not in refined_avg:
                                        refined_avg[infl] = 0.0
                                    # Use the current iteration's weights for neighbors 
                                    # that have already been processed
                                    if neighbor < vertex and neighbor in new_weights:
                                        refined_avg[infl] += new_weights[neighbor].get(infl, 0.0)
                                    else:
                                        refined_avg[infl] += current_weights[neighbor].get(infl, 0.0)
                        
                        # Normalize the refined averages
                        for infl in refined_avg:
                            refined_avg[infl] /= len(connected_vertices)
                        
                        # Apply additional blending
                        blend_factor = 0.5  # Less aggressive for additional passes
                        for infl in active_influences:
                            current = temp_weights.get(infl, 0.0)
                            refined = refined_avg.get(infl, 0.0)
                            temp_weights[infl] = current * (1.0 - blend_factor) + refined * blend_factor
                    
                    # Update with the result of multiple passes
                    new_weights[vertex] = temp_weights
                
                # Normalize weights for this vertex
                total = sum(new_weights[vertex].values())
                if total > 0:
                    scale_factor = 1.0 / total
                    for infl in active_influences:
                        new_weights[vertex][infl] *= scale_factor
                
                # Apply volume preservation if enabled
                if preserve_volume:
                    # This is a simplified volume preservation approach
                    significant_threshold = 0.1
                    for infl in active_influences:
                        orig_weight = original_weights[vertex].get(infl, 0.0)
                        if orig_weight > significant_threshold:
                            # Limit change for significant influences, but scale by intensity
                            max_change = 0.5 * min(intensity, 1.0)  # Cap at 0.5 for high intensities
                            new_weight = new_weights[vertex][infl]
                            clamped_weight = max(min(new_weight, orig_weight + max_change), orig_weight - max_change)
                            new_weights[vertex][infl] = clamped_weight
                    
                    # Re-normalize after volume preservation
                    total = sum(new_weights[vertex].values())
                    if total > 0:
                        scale_factor = 1.0 / total
                        for infl in active_influences:
                            new_weights[vertex][infl] *= scale_factor
            
            # Check for cancellation periodically
            if self.progress_canceled:
                return None
        
        return new_weights

# Create and show the tool
relax_tool = SkinRelaxTool()