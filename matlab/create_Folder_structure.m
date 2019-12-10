function create_Folder_structure(target_path, regions)

if exist(target_path)
  preceed = input("The folder already exist.\nDouble check if you would like to overwrite it? (Y/N)\n", "s");
  if preceed ~= "Y"
      disp("Did NOT create the folders!!\n");
    return;
  end
end

for i = 1:length(regions)
mkdir(target_path + "0/" + regions{i});
mkdir(target_path + "constant/" + regions{i});
mkdir(target_path + "system/" + regions{i});
end

end