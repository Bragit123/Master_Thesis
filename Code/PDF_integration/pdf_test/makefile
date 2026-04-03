######################################
# Note to self:                      #
# $@ = Target (left of :).           #
# $< = First dependency (right of :) #
# $^ = All dependencies (right of :) #
######################################

# Compiler options
CXX = g++
CPP_VERSION = c++17
CXX_FLAGS = -std=$(CPP_VERSION) -I $(INCLUDE_DIR) -I $(LHAPDF_DIR)/include
LD_FLAGS = -std=$(CPP_VERSION) -L $(LHAPDF_DIR)/lib -lLHAPDF

# Directories
SRC_DIR = src
BUILD_DIR = build
OBJ_DIR = build/obj
OUTPUT_DIR = output
INCLUDE_DIR = include
LHAPDF_DIR = ../../LHAPDF

# Files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))
EXECUTABLE = $(BUILD_DIR)/main.exe

# Commands
all: run

compile: $(OBJS)

link: $(EXECUTABLE)

MEM ?= 0
run: $(EXECUTABLE)
	@echo "### Running..."
ifndef MEM
# 	$(error Must provide a member number. Usage: make run MEM=<member number>)
	@echo "# No argument given, setting member to 0."
	@echo "# To specify member value, use:"
	@echo "#   make run MEM=<member>"
endif
	@mkdir -p $(OUTPUT_DIR)
	./$(EXECUTABLE) PDF4LHC21_40 $(MEM)

clean:
	@echo "### Cleaning..."
	rm $(OBJS) $(EXECUTABLE) $(wildcard $(OUTPUT_DIR)/*)

# Compiler (creates objects, dependent on source files)
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "### Compiling..."
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXX_FLAGS) -c $< -o $@

# Linker (creates executable, dependent on objects)
$(EXECUTABLE): $(OBJS)
	@echo "### Linking..."
	$(CXX) $(LD_FLAGS) $^ -o $@