COMMON_SRC =

ARM_SRC += $(COMMON_SRC) \
		   src/pen.c \
		   src/l6470.c \
		   src/wires.c \
		   src/pwm.c \
		   src/draw.c

X86_SRC += $(COMMON_SRC) \
		   src/Xdraw.c

ifeq (,$(findstring arm, $(CC)))
	SRC := $(X86_SRC)
	DEPS := $(shell pkg-config --cflags --libs x11) -lm -DSIMULATION
	CC := gcc
else
	SRC := $(ARM_SRC)
	DEPS := -lm
endif

all: lib app

lib:
	@echo "--> generate polargraph library"
	$(CC) -fPIC -shared -o libpolargraph.so $(SRC) -Wall $(DEPS) -pthread -DGETTEXT_PACKAGE="\"intltest"\"
app: lib
	@echo "--> generate polargraph application"
	$(CC) -o polargraph src/main.c -L. -lpolargraph -Wall $(DEPS) -pthread -DGETTEXT_PACKAGE="\"intltest"\"

clean:
	rm -f libpolargraph.so polargraph
