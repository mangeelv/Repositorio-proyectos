
function [xs,converge] = gauss_seidel(A,b,x0)
    D = diag(diag(A));
    E = -(tril(A) - D);
    F = -(triu(A) - D);
    converge = false;
    max_its = 1000;
    c = 0;
    tol = 1e-8;
    x_old = x0;
    while c < max_its && not(converge)
        x = (D-E)\F*x_old + (D-E)\b; % forma eficiente de hacer la inversa
        converge = (norm(x-x_old) < tol);
        x_old = x;
        c = c+1;
    end
    xs = x;
end