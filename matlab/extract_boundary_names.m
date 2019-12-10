function bcs = extract_boundary_names(target_path, regions)
  bcs = containers.Map;
  for i = 1:length(regions)
    path = target_path + "/constant/" + regions{i} + "/polyMesh/boundary";
    text = fileread(path);
    text = text(~isspace(text));
    [from, to] = regexp(text, '\((.*)\)');
    text = text(from+1:to);
    bc = regexp(text, '(.*?)\{type(.*?);startFace(\d*?);nFaces(\d*?);\}', 'tokens');
    bcs(regions{i}) = bc;
  end
end