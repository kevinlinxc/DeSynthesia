# Intro
This repo takes as input a downloaded YouTube "Piano Tutorial/Synthesia" video and outputs a .mid (midi file) that 
MuseScore can turn into sheet music. It accomplishes this by looking at the notes on screen rather than trying to use audio
and Fourier transforms. So, while the notes can be rigidly timed and may not output good rhythms for playing, it at 
least gets the notes right 100% of the time. This is working with Sheet Music Boss' content especially well because

1. His keys light up when played, making for easier detection than what I tried with Francesco Parrino's work (DeSynthesiaFP.py)
2. He separates left and right hands using green and blue, so I can make two separate tracks so the midi doesn't
confuse which hand is which.
   
This script can't really be generalized to other creators since some creators use different effects like Rousseau, and 
when the keys themself don't light up, there's overlap between flats and natural keys that can be hard to account for.

# Instructions
- Use some downlaoder to download the YouTube video. 
  
- Adjust the seconds_to_skip_at_start and seconds_to_skip_at_end in the script to remove intros and outros
- Run the script with debug = True (click the image window that opens up and click any button to go forward) to make sure notes are being detected (dots will appear on the notes)
- Change the tempo to whatever the actual sheet music says tempo should be

- Run the script with debug = False, and let it run its course. 
- Open the .mid file in Musescore. At the bottom, change the time signature to what it should be and if the staffs
are messed up, try disabling Split staff. 
  
- The script will work poorly for swing songs. You can also adjust the rounding amount and if rounding occurs at all in the script,
but MuseScore does the heavy lifting for simplifying durations.

  



# Ethics
What I'm doing is obviously morally dubious. I am creating a free, albeit strictly worse version of what 
can be bought. However, most people will agree that MusicNotes.com, and monetization of sheet music
in general is a joke. Yes, people should be paid for their work, but 10 dollars per song is a tremendous
ask for a casual piano player who might want to play 10 or 20 pieces, and the predatory techniques that MusicNotes.com uses (e.g. making you
only able to print sheet music x times [it's 2021, we know how to print to pdf]) make supporting the creator much less satisfying. 

The sheet music industry is crusty and needs innovation. What if MusicNotes paid creators (more? at all?) for uploading
content and promoting their site, so the consumers could pay less? What if MusicNotes had an app that was mobile friendly for
performance playback (another problem I try to address in the **flatten** folder). I don't know. I feel like in putting up 
tutorial videos like this, the data is already out there, and I'm just aggregating it really fast, automatically in frustration.
