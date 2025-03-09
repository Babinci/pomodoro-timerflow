# Progress
    - What works:
    web app and backend server live with docker, there is user crud, timer with settings

 actual plans:
 
 timer problems (current status- implemented changes of those now testing):
 - after long round- there is short break - it should be break from long preset- and i cant change break to long
 - after 1 round and 1 break- i saw "start break" button instead of "start"
 - when working in round and clicking pause- cant resume- screen "freezed"
 - it is very hard to change ot long intervals
 - after 25 short work- i see 10 min short break (it should be 5 min as short in settings)- and cant change during break to short break
 
 
 new problems:
 - when i clicked new browser tab- it reseted to that new- first was counting 49 and then i opened new tab and it was 25 in second and reseted
     - generally, this timer should work even if i close browser so it should have universal source in websockets backend server and so timer should go to break/ end of break and have state, the only thing is that maybe each 5.am local time- it should reset as for new date (with some clever resources management in timer algorithm)
 
 bus:
 - Failed to update task: Failed to update task with increasing number of pomodoros
 - server disconnecting problem
 
 - What's left to build
 - timers tests
 - Wear OS app development (implementation in progress)
 - description field with more options for text formatting like tabs and bold font
 - websockets server and client usage optimization
 - problems with pause time- after long work i can see short break and cant change to long
 - mess with timer
 - after finished session i cant see  it in counter number
 - confetti after finished task
 
 - optional bell ring at end of round
 + google auth
