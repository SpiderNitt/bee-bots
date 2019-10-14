//DUAL MOTOR TUNING
#include<avr/io.h> 
#include <avr/interrupt.h>
#define pi 3.14
#define FOSC 16000000                                             // Clock Speed
#define BAUD 9600                
#define MYUBRR FOSC/16/BAUD -1
char ReceivedChar ;

void USART_RX_init()
{   
    UBRR0H = (MYUBRR >> 8);
    UBRR0L = MYUBRR;
    UCSR0B |= (1 << RXEN0) | (1 << TXEN0);      // Enable receiver and transmitter
    UCSR0B |= (1 << RXCIE0);                    // Enable reciever interrupt
    UCSR0C |= (1 << UCSZ01) | (1 << UCSZ00);    // Set frame: 8data, 1 stp
}
ISR (USART_RX_vect)
{  PORTD |=(1<<5)|(1<<6);
   char control;
   control  = UDR0 ;   
   if(control == 'l')
   {  PORTB &=~ (1<<0)|(1<<3);
      PORTB |=  (1<<1)|(1<<2);
   }
   else
   if(control == 'r')
   {  PORTB |= (1<<0)|(1<<3);
      PORTB &=~(1<<1)|(1<<2);
    }
   else
   if(control == 's')
   {  PORTB &=~ (1<<0)|(1<<1)|(1<<2)|(1<<3);
    }
    
   
}                     

int main()
{ sei();
  USART_RX_init();
  DDRD |=(1<<5)|(1<<6);           //PIN 6 : ENA , 5 : ENB
  DDRB |=(1<<0)|(1<<1);           //PIN 8 : IN1 , 9 : IN2
  DDRB |=(1<<2)|(1<<3);           //PIN 10: IN3 , 11: IN4 
  
  while(1)
  { 
    }
  return 0;
  }
