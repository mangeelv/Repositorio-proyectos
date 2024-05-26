function resultado = ptomedio(f,a,b)
    xx = linspace(a,b,100);
    h = xx(2)-xx(1);
    resultado = 0;

    for i=2:length(xx)
        resultado = resultado +f((xx(i-1)+xx(i))/2);
    end
    resultado = resultado*h;

end