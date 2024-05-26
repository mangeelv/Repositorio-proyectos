function output = rk2(f,xx,alpha)
    h = xx(2) -xx(1);
    output = zeros(1,length(xx));
    output(1) = alpha;
    y_old = alpha; 
    for i=2:length(xx)
        k1 = f(xx(i-1),output(i-1));
        k2 = f(xx(i-1)+h,output(i-1)+h*k1);
        y = y_old + (h/2)*(k1+k2);
        output(i) = y;
    end
end