#include<avr/io.h> 
#include <avr/interrupt.h>
#define pi 3.14
uint8_t  set = 0  ;
float pulse_per_rev = 14760/4 ;                                   //CPR value = 14760  ; PPR = CPR/4 ;  
int pulse1=0,pulse2=0;                                            //variable used to calculate the number of pulses from each encoder
int comp_val = 3124;                                              // for 0.05 s timer                             
float rpm_1,rpm_2;                                               
/* Timer 1 is used to measure the rpm 
 * Used in CTC mode with interrupts
 * Time period : 100 ms
 */
void speedometer_init()
{   TCCR1B |= (1 << WGM12)|(1 << CS12)  ;                        // Set up timer with prescaler = 256 and CTC mode                                                
    OCR1A = comp_val ;                                           // Initialize compare value
    TIMSK1 |= (1 << OCIE1A);                                     // Counter Output Compare A Match interrupt is enabled            
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
  rpm_1=float((pulse1/pulse_per_rev)*20.0*60.0);                                                 // rpm = [{(no.of pulses counted)/(no.of pulses per revolution)}*60] / (time taken)
  rpm_2=float((pulse2/pulse_per_rev)*20.0*60.0);    
  Serial.print(rpm_1);
  Serial.print(":");
  Serial.print(rpm_2);
  Serial.println(" ");                                                    
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
{ speedometer_init();
  DDRD &=~(1<<2)|(1<<3);    
  ext_interrupts_init();
  sei();
  Serial.begin(9600);
    
while(1)
{
  
}
return 0;
}
