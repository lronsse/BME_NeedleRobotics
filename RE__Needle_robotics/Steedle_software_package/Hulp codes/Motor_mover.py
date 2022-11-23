# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:26:59 2021

@author: Rolf
"""
import serial
import time
from pySerialTransfer import pySerialTransfer as txfer

step_count_M1 = [ 0]
step_count_M2 = [ 0]
step_count_M3 = [ 1000]


if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('COM9')
        
        link.open()
            
        time.sleep(2) # allow some time for the Arduino to completely reset
        
        list_of_lists = [step_count_M1,
                         step_count_M2,
                         step_count_M3] 
                     
    
        length = len(list_of_lists)
        
        while True:
            for i in range(length):
                send_size = 0
                    
                ###################################################################
                # Send a list
                ###################################################################
                list_ = list_of_lists[i]
                list_size = link.tx_obj(list_)
                send_size += list_size
                print(send_size)
                    
                '''          
                    ###################################################################
                    # Send a string
                    ###################################################################
                    str_ = 'hello'
                    str_size = link.tx_obj(str_, send_size) - send_size
                    send_size += str_size
                    
                    ###################################################################
                    # Send a float
                    ###################################################################
                    float_ = 5.234
                    float_size = link.tx_obj(float_, send_size) - send_size
                    send_size += float_size
                '''
                ###################################################################
                # Transmit all the data to send in a single packet
                ###################################################################
                print('hallo2')
                link.send(send_size)
                print('hallo')
                
                ###################################################################
                # Wait for a response and report any errors while receiving packets
                ###################################################################
                while not link.available():
                    if link.status < 0:
                        if link.status == txfer.CRC_ERROR:
                            print('ERROR: CRC_ERROR')
                        elif link.status == txfer.PAYLOAD_ERROR:
                            print('ERROR: PAYLOAD_ERROR')
                        elif link.status == txfer.STOP_BYTE_ERROR:
                            print('ERROR: STOP_BYTE_ERROR')
                        else:
                            print('ERROR: {}'.format(link.status))
                    
                ###################################################################
                # Parse response list
                ###################################################################
                rec_list = link.rx_obj(obj_type=type(list_),
                                       obj_byte_size=list_size,
                                       list_format='i')
                    
                    
                '''                   
                ###################################################################
                # Parse response string
                ###################################################################
                rec_str_   = link.rx_obj(obj_type=type(str_),
                                         obj_byte_size=str_size,
                                             start_pos=list_size)
                    
                ###################################################################
                # Parse response float
                ###################################################################
                rec_float_ = link.rx_obj(obj_type=type(float_),
                                         obj_byte_size=float_size,
                                         start_pos=(list_size + str_size))
                    '''
                ###################################################################
                # Display the received data
                ###################################################################
                
              
                print('SENT: {}'.format(list_))
                print('RCVD: {}'.format(rec_list))
                print(' ')
            link.close()
            break
        
        
                
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass

            
               