######################################
# Note to self:                      #
# $@ = Target (left of :).           #
# $< = First dependency (right of :) #
# $^ = All dependencies (right of :) #
######################################

# Compiler stuff
CXX = g++
CPP_VERSION = c++17
CXX_FLAGS = -std=$(CPP_VERSION) -I$(INCLUDE_DIR) -I$(LHAPDF_DIR)/include -I$(GSL_DIR)/include
LD_FLAGS = -std=$(CPP_VERSION) -L$(LHAPDF_DIR)/lib -L$(GSL_DIR)/lib -lLHAPDF -lgsl -lgslcblas

# Project directories
SRC_DIR = src
BUILD_DIR = build
OBJ_DIR = build/obj
OUTPUT_DIR = output
INCLUDE_DIR = include

# External package directories
EXTERNAL_DIR = ../../external
LHAPDF_DIR = $(EXTERNAL_DIR)/LHAPDF
GSL_DIR = /opt/homebrew/opt/gsl

# Files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))
EXECUTABLE = $(BUILD_DIR)/main.exe

# Commands
all: run

compile: $(OBJS)

link: $(EXECUTABLE)

run: $(EXECUTABLE)
	@echo "### Running..."
	@mkdir -p $(OUTPUT_DIR)
	./$(EXECUTABLE)

clean:
	@echo "### Cleaning..."
	rm $(OBJS) $(EXECUTABLE) $(wildcard $(OUTPUT_DIR)/*)

# Compiler (creates objects, dependent on source files)
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "Compiling $<"
	@mkdir -p $(OBJ_DIR)
	@$(CXX) $(CXX_FLAGS) -c $< -o $@

# Linker (creates executable, dependent on objects)
$(EXECUTABLE): $(OBJS)
	@echo "Linking $<"
	@mkdir -p $(BUILD_DIR)
	@$(CXX) $(LD_FLAGS) $^ -o $@