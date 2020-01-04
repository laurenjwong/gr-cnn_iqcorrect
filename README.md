# gr-cnn_iqcorrec

A custom GNU Radio block for correcting IQ imbalance using a Convolutional Neural Network (CNN). The custom module takes in 1024 samples from a simulated channel  and  512  symbols  from  a  matched  root  raised  cosine
filter. The  samples  are  sent  to  two  neural  networks,  one  for estimating  gain  offset  and  one  for  estimating  phase  offset. After  the  estimation  is  complete,  those  estimates  are  then used  to  correct  for  the  I/Q  imbalance  on  the  symbols  in  the second  input. The  custom  module  then  outputs  the  corrected 512 symbols. This implementation was tested using simulated 16QAM signals generated in GNU Radio.
