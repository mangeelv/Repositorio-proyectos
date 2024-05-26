function resultado = difdiv(f,xx)
    if length(xx) == 1
        resultado = f(xx(1));
    else
        resultado = (difdiv(f,xx(1:length(xx)-1)) - difdiv(f,xx(2:length(xx)))) / (xx(1) -xx(length(xx)));
    end
end