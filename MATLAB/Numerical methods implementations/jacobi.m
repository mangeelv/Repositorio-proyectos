function [xs,converge] = jacobi(A,b,x0)
    D = diag(diag(A));
    E = -(tril(A) -diag(diag(A)));
    F = -(triu(A) -diag(diag(A)));
    max_its = 1000;
    c = 0;
    x_old = x0;
    tol = 1e-8;
    converge = 0;
    while c<max_its && not(converge)
        x = D\(E+F)*x_old + D\b; % Forma eficiente de calcular la inversa
        c = c+1;
        converge = (norm(x_old-x)<=tol);
        x_old = x; 
    end
    xs = x;
end