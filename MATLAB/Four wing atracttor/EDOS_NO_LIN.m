function [] = EDOS_NO_LIN(equations, variables, solution)
    % Definir las variables simbólicas
    syms x y z t ;
    
    % Obtener el número de ecuaciones y variables
    n = length(equations);
    m = length(variables);

    % Inicializar la matriz Jacobiana
    J = sym(zeros(n, m));

    % Calcular las derivadas parciales para formar la matriz Jacobiana
    for i = 1:n
        for j = 1:m
            J(i, j) = diff(equations(i), variables(j));
        end
    end
    
    % Sustituir las variables por las soluciones en la matriz Jacobiana
    substituted_Jacobian_matrix = subs(J, [x, y, z], solution); 
    display(substituted_Jacobian_matrix);
    % Calcular los valores propios de la matriz Jacobiana
eigenvalues = eig(substituted_Jacobian_matrix); 
display(eigenvalues)

% Convertir los valores propios a números
numeric_eigenvalues = double(eigenvalues);

% Analizar la estabilidad según los valores propios
if isreal(numeric_eigenvalues(1))
    if numeric_eigenvalues(1) < 0 && numeric_eigenvalues(2) > 0
        disp('Punto de silla -> Inestable');
    elseif numeric_eigenvalues(1) < 0 && numeric_eigenvalues(2) < 0
        disp('Sumidero -> Asintóticamente Estable');
    elseif numeric_eigenvalues(1) > 0 && numeric_eigenvalues(2) > 0
        disp('Repulsor -> Inestable');
    end
else
    if real(numeric_eigenvalues(1)) < 0
        disp('Foco Atractor (Espiral) -> Asintóticamente Estable')
    elseif real(numeric_eigenvalues(1)) > 0
        disp('Foco Repulsor (Espiral) -> Inestable')
    elseif real(numeric_eigenvalues(1)) == 0
        disp('¡¡¡CRITERIO NO DECIDE!!! -> Usar Lyapunov ')
    end
end