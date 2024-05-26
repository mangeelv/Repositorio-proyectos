function output = euler(f,xx,alpha)
    % output es un vector con los valores de la función en el vector xx
    % y' = f(x,y) 
    % alpha es y(xx(1)), la condición inicial 
    y_old = alpha; % se corresponde con xx(1)
    output = zeros(1,length(xx));
    output(1) = alpha;
    for i=2:length(xx)
        y = y_old + (xx(i)-xx(i-1))*f(xx(i-1),y_old);
        output(i) = y;
        y_old = y;
    end
end