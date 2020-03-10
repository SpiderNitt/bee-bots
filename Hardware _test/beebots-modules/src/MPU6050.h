#include <Wire.h>
#include "Kalman.h" // Source: https://github.com/TKJElectronics/KalmanFilter

#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

namespace MPU6050 {
    extern Kalman kalmanX; // Create the Kalman instances
    extern Kalman kalmanY;

    /* IMU Data */
    extern double accX, accY, accZ;
    extern double gyroX, gyroY, gyroZ;
    extern int16_t tempRaw;

    extern double gyroXangle, gyroYangle; // Angle calculate using the gyro only
    extern double compAngleX, compAngleY; // Calculated angle using a complementary filter
    extern double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter

    extern uint32_t timer;
    extern uint8_t i2cData[14]; // Buffer for I2C data

    void init();
    void update();
};