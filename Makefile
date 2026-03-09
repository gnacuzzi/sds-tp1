CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2
LDFLAGS = -lm

SRC_DIR = src

SRCS = \
$(SRC_DIR)/main.c \
$(SRC_DIR)/generator.c \
$(SRC_DIR)/io.c \
$(SRC_DIR)/geometry.c \
$(SRC_DIR)/brute_force.c \
$(SRC_DIR)/cim.c \
$(SRC_DIR)/particle.c \
$(SRC_DIR)/experiment.c

TARGET = tp1

all: $(TARGET)

$(TARGET):
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS)

run: $(TARGET)
	./$(TARGET)

run-periodic: $(TARGET)
	./$(TARGET) 100 10 1

clean:
	rm -f $(TARGET)