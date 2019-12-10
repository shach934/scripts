% The procedure to generate a chtMultiRegionSimpleFoam case. 
% 1, output ANSA mesh file to individual mesh folder by regions. 
% 2, the boundaries in each regions follow the naming convention: _wall, .*2.*, .*
% 3, setup a case folder tree by regions.
% 4, move the mesh from individual region to the case folder.
% 5, change the boundary file in each region to its type.
% 6, write regionProperties, g to constant folder.
% 7, write radiationProperties, thermophysicalProperties file to each region.
% 8, create empty boundary files according to turbulence model in 0 folder for each regions.
% 9, create the files in system folder. 
%%

clear; clc; close;
indi_mesh_path = "C:/Shaohui/OpenFoam/car_model_Af/individual_mesh/";
target_path = "C:/Shaohui/OpenFoam/car_model_Af/car3_test/";
turbulence_model = "k-epsilon";

% 
regions = extract_region_names(indi_mesh_path);
if length(regions) == 1
    disp("Only ONE region found!\nDouble check if this is a multi region problem!\n")
end
create_Folder_structure(target_path, regions);
copy_mesh(indi_mesh_path, target_path, regions);
boundaries = extract_boundary_names(target_path, regions);
clarify_bcs(boundaries);