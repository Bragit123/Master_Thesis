# Package directories
EXTERNAL_DIR = ../external
LHAPDF_INC = $(EXTERNAL_DIR)/LHAPDF/include
CUBA_INC = $(EXTERNAL_DIR)/cuba/include
LOOPTOOLS_INC = $(EXTERNAL_DIR)/LoopTools/include
LHAPDF_LIB = $(EXTERNAL_DIR)/LHAPDF/lib
CUBA_LIB = $(EXTERNAL_DIR)/cuba/lib
LOOPTOOLS_LIB = $(EXTERNAL_DIR)/LoopTools/lib

# Compiler things for readability of compile line
INCLUDE_FLAGS = -Iinclude -I$(LHAPDF_INC) -I$(CUBA_INC) -I$(LOOPTOOLS_INC)
LIB_FLAGS = -L$(LHAPDF_LIB) -L$(CUBA_LIB) -L$(LOOPTOOLS_LIB)
LINK_FLAGS = -lLHAPDF -lcuba -looptools -lgfortran

compile:
	g++-15 -std=c++17 src/* -o main.exe $(INCLUDE_FLAGS) $(LIB_FLAGS) $(LINK_FLAGS)