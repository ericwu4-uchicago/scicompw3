All tests done with parsing all steps between 2 and 19.
For moby.txt, all steps before pool took 0.21 seconds.
Runtime for moby with 2 processes: 32.65
Runtime for moby with 4 processes: 26.80
Runtime for moby with 6 processes: 23.02
Runtime for moby with 9 processes: 24.84

For bible.txt, all steps before pool took 0.79 seconds.
The bible.txt is too bulky to have a process parse multiple parses.
On a notebook, a step size of 2 takes 5 minutes alone.
Runtime for bible with 2 processes: 
Runtime for bible with 4 processes: 
Runtime for bible with 6 processes: 
Runtime for bible with 8 processes: 
Runtime for bible with 9 processes: 

For book-war-and-peace.txt, all steps before pool took 0.50 seconds.
Runtime with 2 processes: 373
Runtime with 4 processes: 
Runtime with 6 processes: 294
Runtime with 8 processes: 
Runtime with 9 processes: 296

The alg has a cost of around O(n^p), p = 2.7.
The Bible does mention Laden with a step size of 2, but so does War and Peace and Moby. It shouldn't be terribly surprising that longer strides resulted in fewer unique words being found. 

The overall approach was to take each text and filter out all non alphabetic characters. Then, ELS is applied and then a search for each of the 10000 most common "words" is performed. This is parallelized by splitting tasks as ELS is applied. In the ideal situation, we could be able to force words to appear in the order they appear in the ELS blob. However, as we already take 5 minutes for a single run on the Bible, the limits of one's patience are already being tested.
This was supposed to run on slurm but I found out less than 24 hours before the due date that numpy in fact does NOT WORK FOR THE LOVE OF CHRIST
THERE. Considering how extensively numpy is used through out, I have decided to settle for using the local results.