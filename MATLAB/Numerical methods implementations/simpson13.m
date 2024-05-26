function resultado = simpson13(f,a,b)
    ptos = 999;
    xx = linspace(a,b,ptos); % hace falta un numero impar de puntos
    h = xx(2) -xx(1);
    m = (ptos-1)/2;
    suma1 = 0;
    for i=1:m
        suma1 = suma1 + f(xx(2*i-1));
    end
    suma2 = 0;
    for i=1:m
        suma2 = suma2 + f(xx(2*i));
    end
    resultado = (h/3) * (f(a) + 4 * suma1 + 2*suma2 +f(b));
end