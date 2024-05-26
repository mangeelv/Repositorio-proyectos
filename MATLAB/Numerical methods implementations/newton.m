function [r,converge] = newton(f,x0)
    h = 10^-8;
    df = @(x) (f(x+h) - f(x)) / h; % aproximación de la derivada
    max_its = 1000000;
    c = 0;
    r_old = x0 - (f(x0) /df(x0));
    converge = false;
    while c < max_its && not(converge)
        r = r_old - (f(r_old) /df(r_old));
        c = c + 1;
        r_old = r;
        converge = (f(r) == 0);


    end
end