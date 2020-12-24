#!/usr/bin/python

# This script is used to create a dirty version of the base project
# to be used in the ruby script script.rb which populates the dirty
# Xcode project with necessary source and header files. The dirty
# project is then compiled into a static library from this script.

import os
import subprocess
import shutil
import shlex

# Common variables
Output_Dir = "build"
Dirty = "Dirty"
RUBY = "ruby"
RUBY_SCRIPT = "script.rb"
XCODEBUILDER = "xcodebuild"
XCODEPROJECT = "-project"
XCODETARGET = "-target"
LIPO = "lipo"
LIPO_ARGS = "-create"
LIPO_OUTPUT = "-output"

UNIVERSAL_LIBRARY = "libUniversal.a"
MAC_LIBRARY = "libFitSdkCpp.a"
iOS_LIBRARY = "libFitSdkCppiOS.a"

# Keys for the projects dictionary
DIR = 'dir'
BUILD_DIR = 'build_dir'
PROJECT = 'project'
LIB_PATH = 'lib_path'
LIB = 'lib'
TARGET = 'target'
SEARCH_STRING = 'search'

projects = [{DIR : "FitMacBaseProject", BUILD_DIR : "FitMacBaseProjectDirty", PROJECT : "/FitSdkCpp.xcodeproj", LIB_PATH : "Release/", LIB : "libFitSdkCpp.a", TARGET : "FitSdkCpp", SEARCH_STRING : "*.{cpp,hpp}"}, {DIR : "FitSdkCppiOS", BUILD_DIR : "FitSdkCppiOSDirty", PROJECT : "/FitSdkCppiOS.xcodeproj", LIB_PATH : "Release-iphoneos/", LIB : "libFitSdkCppiOS.a", TARGET : "universal", SEARCH_STRING : "*.{mm,h,cpp,hpp}"}]

'''
Clones a project directory for building in a temporary location
'''
def cloneProject(dir, build_dir):
    # delete build_dir if it exists
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    # copy the dir to build_dir
    shutil.copytree(dir, build_dir)

# Delete common build directory
if os.path.exists(Output_Dir):
    shutil.rmtree(Output_Dir)

for p in projects:
    # Clone the dir to build_dir
    cloneProject(p[DIR], p[BUILD_DIR])
    # Project file is located in BUILD_DIR + PROJECT
    project = p[BUILD_DIR] + p[PROJECT]
    # Create static lib project(s)
    subprocess.call([RUBY, RUBY_SCRIPT, project, p[SEARCH_STRING]])
    # Compile the project
    subprocess.call([XCODEBUILDER, XCODEPROJECT, project, XCODETARGET, p[TARGET]])
