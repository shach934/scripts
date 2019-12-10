function clarify_bcs(bcs)
% this function is used to apply the boundary condition
% then write the boundary conditions to the boundary file. 
% basic types are:
% 1 patch,          used for inlet and outlet, type patch and no special naming convention
% 2 wall,           used for wall boundary, name end with "_wall", 
% 3 mappedWall      solid 2 fluid boundary, has a "2" between the patch names.
for i = 1:length(bcs) 
    bc = bcs(i);
    for j = 1:length(bc)
        name = bc{i}{1};
        type = bc{i}{2};
        if contains(name, "_wall")
           bc{i}{2} = "wall";
        else if contains(name, "2")
           bc{i}{2} = "mappedWall";
           
           
        end
    end
end
end