# Makefile for RISC-V UDB Converter

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
TARGET = c_to_yaml
SOURCE = c_to_yaml.c

# Default target
all: $(TARGET)

# Build the C program
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE)

# Clean build artifacts
clean:
	del /Q $(TARGET).exe 2>nul || echo "No executable to clean"
	del /Q *.o 2>nul || echo "No object files to clean"

# Test the complete workflow
test: $(TARGET)
	@echo "=== Testing complete workflow ==="
	@echo "Step 1: Converting YAML to C header..."
	python yaml_to_c.py sample_instruction.yaml output.h
	@echo "Step 2: Converting C header back to YAML..."
	./$(TARGET) output.h output.yaml
	@echo "Step 3: Converting generated YAML to C header again..."
	python yaml_to_c.py output.yaml output2.h
	@echo "Step 4: Converting second C header to YAML..."
	./$(TARGET) output2.h output2.yaml
	@echo "=== Workflow complete! Check output.yaml and output2.yaml ==="

# Run a quick demo
demo: $(TARGET)
	@echo "=== Quick Demo ==="
	python yaml_to_c.py sample_instruction.yaml demo.h
	./$(TARGET) demo.h demo.yaml
	@echo "Generated demo.h and demo.yaml from sample_instruction.yaml"

.PHONY: all clean test demo
