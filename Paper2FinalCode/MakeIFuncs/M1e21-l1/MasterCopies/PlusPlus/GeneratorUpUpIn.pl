$N = 5; 
$omega = 0.05; 
$total = $omega*100;
$j_max = $total/$N;
$l = 1; 

$i_biggest = $total -1;

for $j (0..$j_max){
    print "round $j/$j_max: "; system "date";
    $i_max = ($j+1)*$N -1;
    if ($i_max > $i_biggest) {
        $i_max = $i_biggest;
    }
    for $i ($j*$N..$i_max) {
            print "fork $i: "; system "date";
            my $pid = fork();
            if (not $pid) {
                    system("python trialParallelUpUpIn.py $i UpUpIn/trialParallelresulte$i.fits UpUpIn/trialParallelresulto$i.fits $omega $l");
                    exit();
            }
    }
    for $i (0..$N-1) {
            wait();
            print "waited $i/$N: "; system "date";
    }
}
##for $i (0..$N-1) {system("cat trialParallelresulte$i.fits > testingParallele.fits");}
##for $i (0..$N-1) {system("cat trialParallelresulto$i.fits > testingParallelo.fits");}
