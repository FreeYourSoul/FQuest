cmake_minimum_required(VERSION 3.16)
project(FQuestLib)

add_library(FQuestLib
        ${CMAKE_CURRENT_LIST_DIR}/src/FQuest.cpp
        ${CMAKE_CURRENT_LIST_DIR}/include/FQuest.hh)

set_target_properties(FQuestLib PROPERTIES
        CXX_STANDARD 17
        CMAKE_CXX_COMPILER /usr/bin/g++)

set_target_properties(FQuestLib PROPERTIES INCLUDE_DIRECTORIES
        ${CMAKE_CURRENT_LIST_DIR}/include
        )