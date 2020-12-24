# This ruby script edits a copy of the Xcode template project
# and inserts necessary source and header files, creating a
# 'dirty' project to be used by build.sh for compilation.

require 'xcodeproj'

if ARGV.empty?
    puts "No Projects specified, aborting..."
    exit
end

if ARGV.length != 2
    puts "Two arguments required, project_file and search_string"
    exit
end

# Parse the project file name from the input parameters
project_file = ARGV[0]
search_string = ARGV[1]

puts "Preparing project: " + project_file

# load existing .xcodeproj file
project = Xcodeproj::Project.open(project_file)
main_target = project.targets.first

# change to top level
absolute = File.expand_path(File.expand_path(Dir.pwd))
pattern = /MacStaticLib/
upper_dir = absolute.to_s
last = upper_dir.rindex(pattern)
upper_dir = upper_dir[0..last-1]

# add in needed files
Dir.glob(upper_dir + search_string) do |file_name|
    test = project.groups()
    file = project['Source'].new_file(file_name)
    main_target.add_file_references([file])
end

for i in 0..main_target.headers_build_phase.files.length - 1
    build_file = main_target.headers_build_phase.files[i]
    build_file.settings = { 'ATTRIBUTES' => ['Public'] }
end

# save the project
project.save(project_file)