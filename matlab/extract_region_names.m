function regions = extract_region_names(indi_mesh_path)
  % extract the region names of multiregion cases. 
  % write the region properties, name convention: fluid regions start with air, other regions are all solids.
    files = dir(indi_mesh_path);
    files = files(3:end);
    regions = {};
    for i = 1:length(files)
      regions{i} = files(i).name;
    end
end