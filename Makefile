CXX := g++
CXXFLAGS := -shared -std=c++11 -fPIC -Wall -O3
PYFLAGS := `python -m pybind11 --includes`
TARGET := utils
SO_SUFFIX := `~/anaconda3/bin/python3-config --extension-suffix`

SRCDIR := src
OBJDIR := obj
SRCS := $(notdir $(wildcard ${SRCDIR}/*.cpp))
OBJS := $(addprefix $(OBJDIR)/, $(patsubst %.cpp, %.o, $(SRCS)))

$(shell [ -d $(OBJDIR) ] || mkdir -p $(OBJDIR))

all: $(TARGET) $(OBJS)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(PYFLAGS) $^ -o $@$(SO_SUFFIX)

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(PYFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -rf $(OBJDIR) $(TARGET).*.so
