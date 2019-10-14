//DUAL MOTOR TUNING
#include<avr/io.h> 
#include <avr/interrupt.h>
#define Pi 3.14
#define FOSC 16000000                                             // Clock Speed
#define BAUD 9600                
#define MYUBRR FOSC/16/BAUD -1

char control = '0';
//Position and Angle Feedback 
float cur_x = 0, cur_y = 0 ,cur_theta  = 0 ;
float Vl ,Vr, R ,radius = 0.036 ,del_theta = 0,L = 0.325;
float pulse_per_rev = 14760/4 ;                                   //CPR value = 14760  ; PPR = CPR/4 ;  
int pulse1=0,pulse2=0;                                            //variable used to calculate the number of pulses from each encoder
int comp_val = 3124;                                              // for 0.05 s timer                             
float rpm_1,rpm_2;                                                   

void speedometer_init()
{   TCCR1B |= (1 << WGM12)|(1 << CS12)  ;                         // Set up timer with prescaler = 256 and CTC mode                                                
    OCR1A = comp_val ;                                            // Initialize compare value
    TIMSK1 |= (1 << OCIE1A);                                      // Counter Output Compare A Match interrupt is enabled            
}

/* External interrupts INT0 and INT1 
 * used to count the encoder pulses
 * INT0 - PIN 2 - MOTOR A
 * INT1 - PIN 3 - MOTOR B
 * MODE - RISING n
 */
 void ext_interrupts_init()
{   EICRA |= (1 << ISC11)|(1 << ISC10)|(1 << ISC01)|(1 << ISC00);                                 
    EIMSK |= (1 << INT0)|(1 << INT1);  
}
 void ext_interrupts_deinit()
{   EICRA &=~ (1 << ISC11)|(1 << ISC10)|(1 << ISC01)|(1 << ISC00);                                 
    EIMSK &=~ (1 << INT0)|(1 << INT1); 
}
/*calculates rpms of the wheels and resets pulse counters*/
ISR(TIMER1_COMPA_vect)
{ 
  rpm_1=float((pulse1/pulse_per_rev)*20.0*60.0);                                                 // rpm = [{(no.of pulses counted)/(no.of pulses per revolution)}*60] / (time taken)
  rpm_2=float((pulse2/pulse_per_rev)*20.0*60.0);                                                        
  pulse1=0;
  pulse2=0;
  Vl = rpm_1*radius*2*Pi/60;
  Vr = rpm_2*radius*2*Pi/60;
  Serial.print(Vl);
  Serial.print(Vr);
  
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
  float _flush = 0.5;
  ext_interrupts_init();
  speedometer_init();
  sei();  
  
  Serial.begin(9600);
  Serial.print(_flush);
while(1)
{     
      
    
}
}
