#define FOSC 16000000                       // Clock Speed
#define BAUD 9600                
#define MYUBRR FOSC/16/BAUD -1
void uart_transmit (uint8_t data)
{
    while (!( UCSR0A & (1<<5)));                // wait while register is free
    UDR0 = data;                                   // load data in the register
}
void uart_init()
{   UBRR0H = (MYUBRR >> 8);
    UBRR0L = MYUBRR;
    UCSR0B |= (1 << RXEN0) | (1 << TXEN0);                       
    UCSR0C |= (1 << UCSZ01) | (1 << UCSZ00); 
}
int main()
{ float a = 232.56 ;    
  uart_init();
  while(1)
  {  uart_transmit(round(a));
   }
   return 0;
       
}
