//DUAL MOTOR TUNING
#include<avr/io.h> 
#include <avr/interrupt.h>
#define pi 3.14
#define FOSC 16000000                                             // Clock Speed
#define BAUD 9600                
#define MYUBRR FOSC/16/BAUD -1

float error1 = 0, prev_error1 =0 , error2 = 0 , prev_error2 = 0  ;
float pulse_per_rev = 14760/4 ;                                   //CPR value = 14760  ; PPR = CPR/4 ;  
int pulse1=0,pulse2=0;                                            //variable used to calculate the number of pulses from each encoder
int comp_val = 3124;                                              // for 0.05 s timer                             
float rpm_1,rpm_2;                                   
float PID1 = 0 , PID2 = 0 ;
float  set_speed1 =80.0 ,set_speed2 = 110.0; 
float  current_speed1 = 0,current_speed2 = 0;

/*PID Tuned Parameters For M1 and M2 */
float Kp1 = 0.465 , Ki1 = 0 ,Kd1 = 0.002;                         //  M1 : Kp1 = 0.465 Kd = 0.002 sufficient to set speeds between 75 to 130 rpm . ki tuning required
float Kp2 = 0.435 , Ki2 =0  ,Kd2 = 0.002;                         //  M2 : Kp2 = 0.435 Kd = 0.002 sufficient to set speeds between 75 to 120 rpm . ki tuning required 
int a=0;                                                                                           


/*non-inverted PWM phase correct pwm 
 * frequency = 16000000/1024 = 15625 Hz
 */
void PWM_init()
{ 
  TCCR0A |= (1 << WGM00)|(1 << COM0A1)|(1 << COM0B1);                                   
  TCCR0B |= (1 << CS02)|(1 << CS00);                                                   
  TIMSK0 |= (1 << OCIE0A)|(1 << OCIE0B);

}     
/* Timer 1 is used to measure the rpm 
 * Used in CTC mode with interrupts
 * Time period : 50 ms
 */
void speedometer_init()
{   TCCR1B |= (1 << WGM12)|(1 << CS12)  ;                         // Set up timer with prescaler = 256 and CTC mode                                                
    OCR1A = comp_val ;                                            // Initialize compare value
    TIMSK1 |= (1 << OCIE1A);                                      // Counter Output Compare A Match interrupt is enabled            
}
/* External interrupts INT0 and INT1 
 * used to count the encoder pulses
 * INT0 - PIN 2 - MOTOR A
 * INT1 - PIN 3 - MOTOR B
 * MODE - RISING 
 */
 void ext_interrupts_init()
{   EICRA |= (1 << ISC11)|(1 << ISC10)|(1 << ISC01)|(1 << ISC00);                                 
    EIMSK |= (1 << INT0)|(1 << INT1);  
}
/*calculates rpms of the wheels and resets pulse counters*/
ISR(TIMER1_COMPA_vect)
{
  rpm_1=float((pulse1/pulse_per_rev)*20.0*60.0);                 // rpm = [{(no.of pulses counted)/(no.of pulses per revolution)}*60] / (time taken)                                                               
  rpm_2=float((pulse2/pulse_per_rev)*20.0*60.0);
  pulse2=0;
  pulse1=0;
  current_speed1 = rpm_1;
  current_speed2 = rpm_2; 
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
  PWM_init();
  ext_interrupts_init();
  speedometer_init();
  sei();
  DDRD |=(1<<5)|(1<<6);           //PIN 6 : ENA , 5 : ENB
  DDRB |=(1<<0)|(1<<1);           //PIN 8 : IN1 , 9 : IN2
  DDRB |=(1<<2)|(1<<3);           //PIN 10: IN3 , 11: IN4    
  PORTB |=(1<<0)|(1<<2);
  PORTB &=~(1<<1)|(1<<3);         
  
while(1)
{  
        error1 = set_speed1 - current_speed1 ;
        error2 = set_speed2 - current_speed2 ;  
        PID1  +=  Kp1*error1 + Kd1*(error1 - prev_error1) + Ki1*(error1+prev_error1) ;
        PID2  +=  Kp2*error2 + Kd2*(error2 - prev_error2) + Ki2*(error2+prev_error2) ;
        prev_error1 = error1;
        prev_error2 = error2;
        
        if( PID1 > 255)
        PID1 = 255 ;
        else
        if( PID1 < 0)
        PID1 = 0 ;
        
        if( PID2 > 255)
        PID2 = 255 ;
        else
        if( PID2 < 0)
        PID2 = 0 ;
         
        OCR0A = round(PID1);
        OCR0B = round(PID2);
    
        /*following two lines are used for a delay of 0.2 seconds*/
        for(int j =0 ; j<50 ;j++)              
        for(int i =0 ;i<65000;i++);
                   
}
return 0;
}
