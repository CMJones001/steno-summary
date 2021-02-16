# Steno Summary

## What is stenography

A stenography keyboard, or stenotype, consists of the keys `STKPWHRAO*EUFRPBLGTSDZ`, these keys are known as the steno order. Words are typed by striking keys simltaneously, with most words requiring only a single stroke. 

The keys are laid out in the following order:

    S T P H *   F P L T D    
    S K W R *   R B G S Z    
        A O     E U      
        
Note that the leftmost `S` and `*` are double height keys. 


The words are spelt in the steno order given above (with some exceptions). For instance the stroke,

    S T ▧ ▧     ▧ P ▧ ▧ ▧    
    S ▧ ▧ R     ▧ ▧ ▧ S ▧   
        A ▧     ▧ ▧         

would give the word `straps`. Words are mostly spelled phonetically, or may be given by _briefs_ defined by either the user or imported from a pre-made dictionary of common briefs. 

## What we address

This key order does leave many letters missing, and these are stroked as a combination of two or more letters, for instance, `F` may be stroked as `TP`. However, these merged letters can make it challenging to interpret or remember strokes for a beginner. For instance, the stroke for "Family" is given as
  
    ▧ T P ▧     ▧ P L ▧ ▧ 
    ▧ ▧ ▧ ▧     ▧ ▧ ▧ ▧ ▧  
        A ▧     ▧ ▧        
        
which may be unclear at first. However, this is nothing more than the keys representing the letters "FAM". We provide a means to store not only the keys required for the but the sound groups making up the stroke that are much easier to remember.

More complex groups may also be represented, for instance the sound `Ment` is given by `PLT`, leading to the particularly unclear stroke for "Department" `TKPRAPLT`, however `steno-summary` allows this to be stored as `D + P + A + R + Ment`.

         Department
          DPARMent        
    ▧ T P ▧     ▧ P L T ▧   
    ▧ K ▧ R     ▧ ▧ ▧ ▧ ▧   
        A ▧     ▧ ▧        
        
        
## Commands

We provide a `steno-manager` script for adding or accessing the users dictionary. Currently, the dictionary is pre-filled by briefs that I have used while learning stenography. An example command is

     steno-manager starting-with [-s str]
     
to print all words beginning with a given string `str`. If this is not given on the command line, then an interactive mode is entered. The common commands are `starting-with (starts)`, `contains (cont)`, `print-all (all)` with shortened command included in brackets.

To add an entry `Name` consisting given by the `KEY` groups 

    steno-manager add [-n NAME] [-k KEYS] [-t TAGS [TAGS ...]]
   
or this may also be run interatively, if no arguments are given.

Run `steno-manager -h` for more information on commands.

### Letter sounds and disambiguation 

We have tried to include all letter sounds used in stenography. These are included in `letters.py`. All consist of starting capital letter than may be followed by more lower case letters for complex groups such as `Ment` above or `Ng`. 

We try to retain the steno order given above, however, this may not always be possible with the sound groups, and so a shift to the right hand side of the keyboard may be given by a `-` in the middle of the group. Multiple strokes for the one word are separated by slashes.

See the documentation for more information.  
       
 # See More
 Plover is an awesome open source interpreter for stenography and provides courses for learning stenography, visit 
 [learnplover](https://sites.google.com/site/learnplover/) or see [stenoknight](http://stenoknight.com/plover/haxeploverlearn/) for more exercises.
