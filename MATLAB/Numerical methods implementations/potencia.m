function [lambda] = potencia(A,v)
max_its = 1000; 
c = 0; 
w_old = v; % el método de la potencia empieza en v
tol = 10^-8;
converge =false; 
lambda_old = (w_old'*A*w_old)/(w_old'*w_old);
while c < max_its && not(converge)
   
    w = A*w_old/sqrt(w_old'*w_old); %wk+1


    lambda = (w'*A*w)/(w'*w); %lmdak+2

    c = c+1;

    converge = (abs(lambda-lambda_old) < tol);

    w_old = w;
    lambda_old = lambda;

end 

end