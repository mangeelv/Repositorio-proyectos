function resultado = trapecio(f,a,b)
    xx = linspace(a,b,100);
    h = xx(2) -xx(1);
    resultado = 0;
    for i=2:length(xx)
        resultado = resultado + (f(xx(i-1)) + f(xx(i)));
    end
    resultado = (h/2) * resultado;
end