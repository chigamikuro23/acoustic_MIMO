clear;
close all;

%Create wall corners
walls = [0 0; 0 10; 10 10; 10 0];

%Set up locations of receivers
rx_loc = [10 3.40; 10 3.30; 10 3.20; 10.00 3.10;
10.00 3.00; 10.00 2.90; 10.00 2.80; 10.00 2.70;
10.00 2.60; 10.00 2.50; 10.00 2.40; 10.00 2.30;
10.00 2.20; 10.00 2.10; 10.00 2.00; 10.00 1.90;
10.00 1.80; 10.00 1.70; 10.00 1.60; 10.00 1.50;
10.00 1.40; 10.00 1.30; 10.00 1.20; 10.00 1.10;
10.00 1.00; 10.00 .90; 10.00 .80; 10.00 .70;
10.00 6.0; 10.00 .50; 10.00 .40; 10.00 .30;
];


num_trans = 2048;


%Randomly generate transmitter locations
%tx_locs = [10.*rand(num_trans, 1) 10.*rand(num_trans, 1)];
tx = [10.*rand(1, 1) 10.*rand(1, 1)];
%Instantiate impulse and transmitter vectors for writing
ret_impulses = zeros(32, 1000, num_trans);
transmitters = zeros(num_trans,2);

%Find impulse responses of each transmitter from each receiver
impulse = response(tx, rx, walls);
%for i = 1:num_trans
%    tx_loc = tx_locs(i, :);
%    transmitters(i,:) = tx_loc;
%    impulses = responses(tx_loc, rx_loc, walls);
%    ret_impulses(:,:, i) = impulses;
%end
%Plot one impulse response

rolloff = .25;
span = 6;
sps = 4;

b = rcosdesign(rolloff, span, sps);

fs = 44100;
x = ret_impulses(16,:,1024);
s = upfirdn(x,b, sps);
r = s + randn(size(s))*.01;
y = upfirdn(r,b, 1, sps);
figure;
plot(y);

f_xr = abs(fft(x))/sqrt(length(x));

figure;
xas = linspace(0,fs/2,round(length(f_xr)/2));
plot(xas,f_xr(1:round(length(f_xr)/2)))
xlabel('Frequency [Hz]')
ylabel('Power spectrum [dB]')

figure;
stem(abs(ret_impulses(16,:,1024)));
title('Magnitude of Impulse response with delays')
xlabel('Time (ms) from Signal impulse');
ylabel('Amplitude');

%Save variables to file
save('impulses.mat', 'ret_impulses');
save('tx_locations.mat', 'transmitters');