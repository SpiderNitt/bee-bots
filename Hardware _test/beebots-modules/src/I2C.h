#ifndef I2C_H
#define I2C_H

#include <stdint.h>

extern const uint8_t IMUAddress; // AD0 is logic low on the PCB
extern const uint16_t I2C_TIMEOUT; // Used to check for errors in I2C communication

uint8_t i2cWrite(uint8_t registerAddress, uint8_t data, bool sendStop);
uint8_t i2cWrite(uint8_t registerAddress, uint8_t *data, uint8_t length, bool sendStop);
uint8_t i2cRead(uint8_t registerAddress, uint8_t *data, uint8_t nbytes);

#endif