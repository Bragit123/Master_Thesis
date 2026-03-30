######################################
# Note to self:                      #
# $@ = Target (left of :).           #
# $< = First dependency (right of :) #
# $^ = All dependencies (right of :) #
######################################

# Compiler options
CXX = g++
CPP_VERSION = c++17
COMPILE_FLAGS = -std=$(CPP_VERSION) -I $(INCLUDE_DIR)
LINK_FLAGS = -std=$(CPP_VERSION)

# Directories
SRC_DIR = src
BUILD_DIR = build
OBJ_DIR = build/obj
INCLUDE_DIR = include

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
	./$(EXECUTABLE)

clean:
	@echo "### Cleaning..."
	rm $(OBJS) $(EXECUTABLE)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "### Compiling..."
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXX_FLAGS) -c $< -o $@

$(EXECUTABLE): $(OBJS)
	@echo "### Linking..."
	$(CXX) $(CXX_FLAGS) $^ -o $@