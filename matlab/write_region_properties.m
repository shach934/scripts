function write_region_properties(target_path, regions)
    file_name = "regionProperties";
    for i = 1:length(regions)
      if regions{i}(1:3) == "air"
         fluids = [fluids; regions(i,:)];
      endif
    endfor
  
endfunction