function h = responses(tx, rx, walls)
%RESPONSES Summary of this function goes here
%   Detailed explanation goes here

%Set up constants
v = 340;
f = 22000;
lambda = v/f;
[L, ~] = size(walls);
[N, ~] = size(rx);

%Initalize impulse response vectors for each receiver based on one
%transmitter
h=zeros(N, 1000);

for i=1:N
    
    
    tr_vector = tx-rx(i, :);
    
    %Get Euclidean distance from receiver to transmitter
    d_0 = sqrt(sum(tr_vector.^2));
    
    %Attenuation constant
    a_0 = 1/d_0;
    
    
    
    for l=1:L
        
        %Get midpoint of walls and distances between them
        if l ~=L
            midpoint = (walls(l, :) + walls(l+1, :))./2;
            dist = (walls(l, :) - walls(l+1, :));
          
        else
            midpoint = (walls(l, :) + walls(l-L+1, :))./2;
            dist = (walls(l, :) - walls(l-L+1, :));
           
        end
        
        
        unit_parallel = dist/norm(dist,2);
        
        %Get unit vector normal to wall
        unit_normal = [unit_parallel(2) -unit_parallel(1)];
        
        %Get distance to source image
        dist_image = 2*norm((midpoint - tx.*unit_normal).*unit_normal);
        new_xy = tx + dist_image*unit_normal;
        new_tr = new_xy - rx(i,:);
        new_dist = sqrt(sum(new_tr.^2));
        
        %Get angle between tr vector and normal vector
        theta = acos(dot(tr_vector,unit_normal)/(norm(tr_vector)*norm(unit_normal)));
        
        %Use law of cosines to get distance between receiver and source
        %image
        d_l =  d_0^2 + dist_image^2 - 2*d_0*dist_image*cos(theta);
        a_l = 1/d_l;
        
        d_l2 = abs(d_l - new_dist);
     
        a_l2 = 1/d_l2;
        
        
        %Calculate time delay of image pulse
        delay = round(d_l/v*1000);
        delay2 = round(d_l2/v*1000);
        amplitude = a_l*exp(-1i*2*pi*d_l/lambda);
        amplitude2 = a_l2*exp(-1i*2*pi*d_l2/lambda);
        if delay+1 <= 1000
      
            h(i, delay+1) = amplitude;
            h(i, delay2+1) = amplitude2;
        end
      
    end
   
    delay = round(d_0/v*1000);
    h(i, delay+1) = a_0*exp(-1i*2*pi*d_0/lambda);
end

end

