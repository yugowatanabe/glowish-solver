# glowish-solver
Python script to find optimal solution to levels of mobile puzzle game Glowish by The One Pixel.

OBJECTIVE OF THE GAME:
Screen displays grid of shapes (either triangles, squares, or circles) which may be different 
colors (purple, yellow, green, pink, blue, or red). At the beginning, they are by default
in an "OFF" state. By tapping one of the shapes, it and all other shapes of the same type 
(triangles, squares, or circles) and all other shapes of the same color switch from "OFF" to 
"ON", or from "ON" to "OFF" depending whether it was "ON" or "OFF" before the press. 
E.g. tapping a purple triangle will switch the value "ON"<->"OFF" of all purple shapes 
(not necessarily just triangles) and all triangles (not necessarily just purple ones). 
The objective is to turn every shape on the grid "ON".

APPROACH:
Describe the "state" of the system (the collection of n shapes) as an array of length n of 0 or 
1s representing whether each shape is ON or OFF. When a specific shape is pressed, it changes 
the state of the system in a deterministic way. By pressing the same shape again immediately 
after, it's clear it "undoes" the transformation, reverting the system back to its last state. 
So we see that two states are related by a single action symetrically. Therefore, every 
realizable state of the system is related by a sequence of presses. We can represent the 
relationship between these states as a graph, with all edges weight=1. If we do so, all we 
have to do for the optimal solution is ask what is the shortest path from the initial state to 
the state where all values are ON. Can use poly-time shortest-path algorithm. 

EVALUATION:
There are 2^n possible states, however, only a fraction of them are realizable (meaning they 
are able to be reached through a sequence of presses given the puzzle). In fact, have found that 
for puzzles of ~10 shapes, number of realizable states is to the order of 10^3. In worst case, 
approach could have to evaluate up to (2^n)^2 edges, where every possible state is directly 
related to every other possible state. Time complexity is O(2^n), but in application is much more 
efficient since realizable states is much much smaller than the possible states.

HOW TO USE:
In a file titled puzzleShapes.txt, input the shapes involved in the puzzle by using the codes:

P (purple), Y (yellow), G (green), K (pink), B (blue), R (red).
T (triangle), S (square), C (circle)

E.g. for a purple triangle, use PT. Separate individual shapes by a space. See example file.

OTHER NOTES:
Not rigorously tested. Please be take care specially in giving the input through the 
puzzleShapes.txt file. Also, looks like the higher-level puzzles also use patterns on top of the 
shapes. Script cannot solve those problems (yet). This was meant only as fun project and an
algorithms problem to tease the brain. This is actually a general algorithm with a handful of 
other applications.
