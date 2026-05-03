#include <Arduino.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <Servo.h>

Servo esc;
Servo myServo;

static const size_t LINE_MAX = 16;    // max length of command (excluding the terminate character '\0')
static char   lineBuf[LINE_MAX + 1];
static size_t lineLen = 0;
static const char SOC = '@';          // start-of-command marker
static bool   inCommand = false;

/* Command Examples
@S90
@S100
@M1500
@M1600
*/

void setup() {
  Serial.begin(115200);
  esc.attach(9);
  esc.writeMicroseconds(1500);
  myServo.attach(4);
  myServo.writeMicroseconds(1500);
  delay(2000);
}

static void handleCommand(char* command) {
  if (!command || command[0] == '\0') return;

  // If the line includes '\r' (CRLF), terminate at it
  char* cr = strchr(command, '\r');
  if (cr) *cr = '\0';

  // Trim leading spaces
  while (*command && isspace((unsigned char)*command)) command++;
  if (*command == '\0') return;

  // Command type
  char type = *command++;

  // Parse integer
  char* endp = nullptr;
  long value = strtol(command, &endp, 10);

  // Must have at least one digit
  if (endp == command) return;

  if (type == 'S') {
    if (value < 800 || value > 2200) return;
    // TODO: Apply servo command here
    myServo.writeMicroseconds(value);
    Serial.print("SERVO,");
    Serial.println(value);

  } else if (type == 'M') {
    if (value < 1000 || value > 2000) return;
    // TODO: Apply motor command here
    esc.writeMicroseconds(value);
    Serial.print("Motor,");
    Serial.println(value);

  } else {
    // Unknown command type, ignore
    return;
  }
}

void loop() {
  // Read any available bytes without blocking
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    // Start of a new command
    if (c == SOC) {
      inCommand = true;
      lineLen = 0;
      continue;
    }

    // Ignore until we see SOC
    if (!inCommand) continue;

    // End of command -> process
    if (c == '\n') {
      lineBuf[lineLen] = '\0';
      handleCommand(lineBuf);
      inCommand = false;
      lineLen = 0;
      continue;
    }

    // Collect payload, drop frame on overflow (wait for next '@')
    if (lineLen < LINE_MAX) {
      lineBuf[lineLen++] = c;
    } else {
      // Too long: abandon this frame; next '@' will resync
      inCommand = false;
      lineLen = 0;
    }
  }

  // Put other time-critical work here (e.g. sensors if any)
}
