function copy_mesh(indi_mesh_path, target_path, regions)
  for i = 1:length(regions)
    from = indi_mesh_path + regions{i} + "/constant/polyMesh";
    to   = target_path + "/constant/" + regions{i};
    copyfile(from, to);
  end
end