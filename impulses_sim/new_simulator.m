corners = [-10 5; 10 5; 10 -5; -10 -5];

walls = [5, 10, -5, -10];

rx = [5 6];
tx = [-3 5];
reflect_ctr = 0;
reflect_max = 2;

reflections = new_room(tx, rx, walls, reflect_ctr, reflect_max);

disp(reflections);