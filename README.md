# Columns-Arcade-Game
Game Mechanics as well as GUI for the classic arcade game columns. GUI is run through a virtual environment.

To run simply the mechanics and view game through console verstion. Run the project4 file itself.

Once game is running, the first few lines of input will need to be given.

First line: Specify number of rows in playing field. Must be greater than 3
Second line: Specify number of columns in playing field. Must be greater than 2
Third Line: If field is to begin empty, input "EMPTY". If there is to be contents on the field input "CONTENTS". Given there are r rows and c columns there will then follow r lines of input which contains exactly c characters. Each character will represent a cell on the board. Valid colors for the board are: "S, T, V, W, X, Y, Z".

After setting up the board, the inputs will be as follows:

Valid inputs or commands are:
A blank line, which will act as a passage of time. The board will move as if time has passed. 
If there is a faller present, it falls; if there is a faller that has landed (and has not been moved so that it is no longer in a landed position), it freezes; and so on.
You can also input a F, followed by an integer that is a column number (the columns are numbered 1 through c, if there are c columns), followed by a space, followed by three uppercase letters (representing colors), each of these things separated by spaces (e.g., F 1 S T V). This means to create a faller in column 1, with a jewel of color S on the top, a jewel of color T below it, and a jewel of color V below that.
The faller begins with only the bottommost of the three jewels visible. See the example outputs below for more details.
Note that there can only be one faller at a time, so this command has no effect if there is a faller that has not already been frozen.
R alone on a line, which rotates the faller, if there is one. If there is no faller currently, this command has no effect. Note, though, that it is possible to rotate a faller that has landed but not yet frozen.
< alone on a line, which moves the faller one column to the left, if there is one (and if it not blocked by jewels already frozen on the field or by the edge of the field). If there is no faller or the faller can't be moved to the left, this command has no effect. Note, though, that it is possible to move a faller that has landed but not yet frozen, which can take it out of its "landed" status (if it moves to a column with nothing underneath it).
> alone on a line, which moves the faller one column to the right, if there is one (and if it not blocked by jewels already frozen on the field or by the edge of the field). If there is no faller or the faller can't be moved to the right, this command has no effect. Note, though, that it is possible to move a faller that has landed but not yet frozen, which can take it out of its "landed" status (if it moves to a column with nothing underneath it).
Q alone on a line, which means that to quit the program.
