function polinomio = newton_interpolate(f,xx)
    % Lo hacemos simbólico, numérico es un lio 
    syms x
    suma =  0;
    for i=2:length(xx)
        prod = 1;
        for j=1:i-1
            prod = prod * (x-xx(j));
        end
        suma =suma + difdiv(f,xx(1:i))*prod;
    end
    polinomio = difdiv(f,[xx(1)]) + suma;
end