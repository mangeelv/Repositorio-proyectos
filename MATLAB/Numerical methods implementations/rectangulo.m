function resultado = rectangulo(f,a,b)
    xx = linspace(a,b,100); % 100 indica el numero de puntos en el intervalo, habría 99 subintervalos
    h = xx(2) - xx(1);
    resultado = 0;
    for i=1:length(xx)-1
        resultado = resultado + f(xx(i));
    end
    resultado = resultado*h;
end