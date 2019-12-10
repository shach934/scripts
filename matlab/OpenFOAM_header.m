function head = OpenFOAM_header(fileType)
  % this function is used to generate the file head of openfoam config file.
  head = regexp(fileread("MRFProperties"), "\n", "split");
endfunction