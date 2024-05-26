function [L,U] = LU(A)
    [nfilas,ncolumnas] = size(A);
    if not(nfilas == ncolumnas)
        error('La matriz debe ser cuadrada')
    end
    n = nfilas;
    L = eye(n); % inicializamos L como la identidad
    U = subs(eye(n),1,0); % inicializamos U como matriz nula
    for i=1:n % la i va de 1 a n
        for j=i:n
            suma1 = 0;
            for k=1:i-1
                suma1 = suma1 +L(i,k)*U(k,j);
            end
            U(i,j) = A(i,j) - suma1; %primero se actualiza U 
            if j+1 <= n % la j de la L empieza en i+1
                suma2 = 0;
                for k =1:i-1
                    suma2 = suma2 + L(j+1,k)*U(k,i);
                end
                    L(j+1,i) = (1/U(i,i))*(A(j+1,i)-suma2); % luego se actualiza L 
            end
        end
    end 
end