function L = cholesky(A)
    [n, ~] = size(A); % Obtiene el tamaño de la matriz A
    L = zeros(n); % Inicializa la matriz L como una matriz de ceros
    for i = 1:n
        for j = 1:i
            suma = 0;
            for k = 1:j-1
                suma = suma + L(i,k) * L(j,k);
            end
            if i == j
                L(i,j) = sqrt(A(i,j) - suma);
            else
                L(i,j) = (A(i,j) - suma) / L(j,j);
            end
        end
    end
end
