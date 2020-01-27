#include<avr/io.h> 
#include <avr/interrupt.h>
#define pi 3.14

float pulse_per_rev = 540.0 ;                                       //motor used generates 540 pulse for a single revolution of the motor
float pulse1=0.0,pulse2=0.0;                                          //variable used to calculate the number of pulses from each encoder

int comp_val = 6249;                                           // for 0.1 s timer 

float kp1=0.5,kp2=0.5;                                             //only proportional constant used          
float err_1=0,p_err_1=0,err_2=0,p_err_2=0;
float set_speed_1,set_speed_2;
float rpm_1,rpm_2;

/* Timer 1 is used to measure the rpm 
 * Used in CTC mode with interrupts
 * Time period : 100 ms
 */
 
void speedometer_init()
{   TCCR1B |= (1 << WGM12)|(1 << CS12)  ;                       // Set up timer with prescaler = 256 and CTC mode                                                
    OCR1A = comp_val ;                                          // Initialize compare value
    TIMSK1 |= (1 << OCIE1A);                                    // Counter Output Compare A Match interrupt is enabled            
}

/* Timer 0 is used for generating pwm 
 * signals for both the motors 
 * OC0A - PIN 6 - MOTOR A - ENA
 * OC0B - PIN 5 - MOTOR B - ENB
 * PWM frequency = 5 KHz (2 to 20 Khz recommended)
 */
void PWM_init()
{ 
  TCCR0A |= (1 << WGM00)|(1 << COM0A1)|(1 << COM0B1);                                   // non-inverted PWM phase correct pwm with 
  TCCR0B |= (1 << CS02)|(1 << CS00);                                                    // frequency = 16000000/1024 = 15625 Hz
  TIMSK0 |= (1 << OCIE0A)|(1 << OCIE0B);
  // add different values to test
  OCR0A = 127;                                                                         
  OCR0B = 255; 
}

/* External interrupts INT0 and INT1 
 * used to count the encoder pulses
 * INT0 - PIN 2 - MOTOR A
 * INT1 - PIN 4 - MOTOR B
 * MODE - RISING 
 */
 void ext_interrupts_init()
{   EICRA |= (1 << ISC11)|(1 << ISC10)|(1 << ISC01)|(1 << ISC00);                                 
    EIMSK |= (1 << INT0)|(1 << INT1);  
}

/*calculates rpms of the wheels and resets pulse counters*/
ISR(TIMER1_COMPA_vect)
{
  rpm_1=float(pulse1/pulse_per_rev)*10.0*60.0;                                                 // rpm = [{(no.of pulses counted)/(no.of pulses per revolution)}*60] / (time taken)
  rpm_2=float(pulse2/pulse_per_rev)*10.0*60.0;                                                               
  pulse1=0;
  pulse2=0;
}

/* counts pulses*/
ISR (INT0_vect)  
{ 
  pulse1++;
}
ISR (INT1_vect)  
{ 
  pulse2++;
}


int main()
{ 
  speedometer_init();
  ext_interrupts_init();
  PWM_init();
  sei();
  Serial.begin(9600);
  DDRD |=(1<<5)|(1<<6);
  DDRB |=(1<<0)|(1<<1);           //PIN 8 and 9 in1 , in2
  DDRB |=(1<<2)|(1<<3);           //PIN 10 and 11 in3 , in4
  PORTB |=(1<<0)|(1<<2);
  PORTB &=~(1<<1)|(1<<3);         //forward
  
  sei();
  Serial.begin(9600);

while(1)
{ Serial.print(rpm_1);
  Serial.print(",");
  Serial.println(rpm_2);
  
}
return 0;
}
