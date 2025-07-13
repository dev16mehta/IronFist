## IRON FIST
REPORT By Dev Mehta

Introduction:
This report documents how the game “Iron Fist” came into existence, by using
the simple GUI library. It also exhibits the comprehension and application of
important ideas covered in the course, such as collisions, the use of the Vector
class, and many more.
This report includes the key contents of the game, how the code works, and the
communication, dynamics, and work ethic of the group.

Game:
This game was inspired by a pre-existing game:
https://poki.com/en/g/iron-snout
The objective of this game is to kill the enemies by jumping and punching them.
The player is a character who can jump, punch left, and punch right.
The enemies fly in from multiple angles and the player has to eliminate them as
they randomly appear. Over time in the game, the difficulty increases as the
overall speed at which the enemies enter the screen increases which creates a
more demanding environment for the player to thrive in a highly pressured
scenario.
There are certain problems that the player may encounter while playing the
game, this can include things such as too many enemies entering the screen
which can cause all 3 lives to be finished quickly. The sprites are also animated,
meaning that both the character and the enemies will be moving on the screen,
providing a better user experience.

USER MANUAL:
To run the code you will need to open
https://py3.codeskulptor.org/#user309_Kpn6EU8Sx2Sg8GK_0.py in the browser.
To start the game you will need to press the start button in the center of the
screen.
This is the welcome screen and shows the start page of the game, providing the
user with instructions on how to play the game and what keys do on the actual
game screen.
Once the ‘Start’ button has been pressed it loads up the game page, which looks
like this:
This is the game screen that is visible as soon as the start button is pressed, and
On this screen, there is:
- The player sprite in the center of the screen
- The number of lives which is displayed at the top right of the screen, every
time the game starts, the player is given 3 lives, and each time the enemy
sprite comes in contact with the player sprite the number of lives
decreases
- At the top left of the screen there is the ‘score’ which increments every
second, so the score will keep getting higher
- In the top middle there is a ‘hits’ column which increments every time the
player sprite hits the enemy sprite. Each time the player hits the enemy the
‘hits’ is reset to 0
To control the player, you use the arrow keys to move in the pressed direction. If
the number of lives is 0 then you die, meaning that the enemy sprite has touched
you 3 times and the game is now over. To try again press the play again button at
the end screen.
The next screenshot displays the game in the process of playing.
Here we can see that:
- The number of lives in 1 which means that the enemy sprite has hit the
player twice
- The score on the top left is 25 which means that the player has been alive
for 25 seconds
- There are also 2 more enemies which are entering the screen randomly
The next two screenshots of the game show the character attack, which is
in the air. There are 2 different animations that happen thus the two
screenshots:
This next screen shows the end screen.
- The simple plain black background gives a better feel
- Prints “Game Over” in the center of the screen
- Displays the final score in the center
- There is a play again button which allows the user to start the game again
and gives it another turn



Key Concepts:
A library for Python called SimpleGUI offers a simple method for making games
and graphical user interfaces. It was mainly created with education in mind,
especially for inexperienced Python programmers.
CodeSkulptor, a web-based Python environment created by Scott Rixner for Rice
University's basic computer science courses, served as the model for SimpleGUI.
CodeSkulptor was perfect for interactive learning because it let students write
Python code directly in a web browser and see the results right away.
As a component of CodeSkulptor, SimpleGUI was created to offer a user-friendly
GUI toolkit designed with teaching in mind. With the help of minimum code, users
may effortlessly construct windows, buttons, text inputs, and other GUI elements
by abstracting away much of the complexity associated with GUI development.
The frame module, which we utilized for this game, lets us build a canvas and
serves as a container for controls, a program can only have one frame created.
The constants module is an additional instance where event handlers can be
configured; the mouse click event handler is one such example that we have
implemented in our game.
This code adds a start button to the frame and configures event handlers for
keystrokes, mouse clicks, and canvas drawings. Moreover, a variable to monitor
the game's status over the screen is initialised.
We had to perform some research to deepen our understanding of collisions to
cope with them in our game.


Class Hurtbox:
It inherits from the Collision_Box class. ‘Owner, offset, and radius’ are
parameters passed to the constructor __init__. Uses super() when calling the
constructor of the parent class.owner, offset, and radius in __init__.
We then used a drawing technique that creates a hurtbox on a canvas. Two
circles are shown, one reflecting the player's position in green and the other the
hurtbox's position in blue, if self.visible is true. The hurt boxes and the player's
positions are established by their pos characteristics.
This is what the character looks like in-game when the circles are
set to visible.
So when the enemy comes within the radius of the hitbox, this will
take a life away from the player.
Vectors were dealt with in the Ghost class.
- The ‘self.accelerator’ is an instance variable representing the current
acceleration of the ghost. It's initialized as a Vector object with components
(0, 0) indicating no acceleration in either the x or y direction.
- The self.accel: Another instance variable representing the acceleration that
will be added to self.accelerator each time step. It's initialised with a value
of Vector(0.04, 0), meaning that during each update, the ghost will
accelerate by 0.04 units in the x-direction.
- The self.max_accel_vel represents the maximum velocity achievable due
to acceleration. It's initialised as a Vector with components (7.5, 0),
indicating a maximum velocity of 7.5 units in the x-direction. This means
that the ghost's acceleration will cease once it reaches this velocity.
Imports the Vector class from a module named user304_rsf8mD0BOQ_1. This
module contains the definition of the Vector class that is going to be used.
- self.pos - the attribute is being initialised as a Vector object, representing
the position of the ghost within the game.
- Vector(self.WIDTH/2, self.HEIGHT/2) creates a new Vector object with the
x-coordinate set to half of the width of the game window (self.WIDTH/2)
and the y-coordinate set to half of the height of the game window
(self.HEIGHT/2).
This attribute is an instance variable representing the velocity of the ghost.



Code Description:
Global variables for our user interface, kinematics, and scoring system are where
our code starts. Next, we load the different background pictures. We first
implemented the ‘StartMenu’ class which loads the GUI for the user.
The start menu is rendered on a canvas by the draw function. It requires a
canvas object as an input.
Within the ‘draw’ method:
- It determines if the game (not self.game.started) has begun.
- It configures a few stylistic factors, such colour and text size.
- It uses the selected font size and colour to draw the title "Iron Fist" in the
center of the canvas.
- It puts "Press Start to Begin" as a subtitle directly beneath the headline.
- It includes a notice about how to jump, fastfall, and punch, along with a
note to avoid the enemies.
We then created our first button called “Start”, this button works and uses
something calle a mouse handler which we also implemented in the game.
The button is a polygon with a fill colour of dark turquoise and a white border.
The coordinates of the button's vertices are specified when drawing the button
using the canvas.draw_polygon() function. The position, width, and height of the
button are used to determine the vertices' formation to create a rectangle.
It creates the word "Start" in the button's center. Button_pos[0] + 25 is used for
horizontal positioning, while button_pos[1] + 30 is used for vertical positioning, to
determine the text's placement.
We then implemented our main “Game” class. This class provides structure and
functionality to manage various aspects of the game such as: initialising, event
handling, and the updating/drawing of the game elements.
In this function, we handle frames
within the spritesheets.
In addition to handling flipping
frames as needed for movements
like walking or running when
flipping frames are necessary for
appropriate animation, both
approaches make sure that the
animation cycles through the
frames in the sprite sheet, looping
back to the beginning when
necessary.


The parameters for loading an image are url (the image's URL) and
max_attempts (the maximum number of attempts permitted to load the picture).
It sets the tries counter to zero by default. Using simplegui.load_image(URL), it
tries to load the image. The code checks, inside a while loop, whether the
picture's height or width is still 0, which indicates that the image hasn't loaded,
and whether the number of attempts is fewer than or equal to max_attempts.
It retries loading the image and increases the attempts counter if both
requirements are satisfied. The picture returns ‘None’ if it cannot load after the
maximum number of attempts (attempts > max_attempts). The loaded image
object is returned if the image loads successfully in the allotted number of tries.
Next in the ‘Entity’ class, we initiate two methods called:
- Hitbox
- hurtbox
What these do is they manage the radius of impact with the player against the
enemy.
Right now hitbox is ‘none’ but it will
be added to later on in the class.
- hit(self): This method prints "pow" and adds one to the object's score
attribute. It is utilised to control what happens when the enemy is struck.
- hurt(self): "ow" is printed, in the event that the player sustains damage.
- create_hitbox(self,owner,x,y,radius,time,hitlag): The hitbox for the object is
made. It requires several parameters, including radius, duration to live
(before the hitbox is destroyed), x and y offsets (from the entity center),
and hitlag. It uses an instance of the Hitbox class to initialise the owner
object's hitbox attribute.
Our next major class is the ghost class which sets up a ghost entity in the game,
complete with hitboxes, movement attributes, and sprite animations. The ghost is
initially set to be alive and in the "air_attack" state.
The update method controls the movement and behavior of the ghost object in
the game, including its velocity, position, animation, and state transitions.
This class provides functionality for
managing time-related operations
within the game, such as counting
frames, tracking elapsed time, and
determining when transitions
should occur based on frame
duration.


After the main game function, we made the keyboard class which pinpoints how
the player will move the character. The user can use any of the 4 arrow keys or
WASD to move up, down, left, and right.
The next big class is the Interaction class in which we implemented the addition
of multiple enemies on the screen. This makes the game more fun and engaging
for the player. The enemies spawn in randomly using the random function. There
is also the option of the game randomly choosing whether to spawn a ghost on
the left-hand side or the right-hand side.
The ‘Update’ method handles various aspects of the game during each frame:
- Every frame, elapsed_time is increased by 1. The player's score is
increased by one if elapsed time is divided by 60, which denotes that one
second has elapsed.
- Updates are made to entities that are not in the paused state if stop_timer
is larger than 0. Every frame, it reduces stop_timer by 1. An entity adds
itself to the expired set, indicating that it has finished its action, if its state is
not "hurt".
- If the player's lives are 0 then it runs the Game over sequence
- It modifies the player's status based on its detection of different keyboard
inputs. The player can perform a jump or double jump if they meet specific
requirements and push the up arrow key. If the player is in the airborne
condition, using the down arrow key will cause them to plummet quickly.
The left and right arrow keys update the player's direction and, depending
on their current condition, start an attack or air attack action.
When combined, these methods offer the ability to show the game over screen
along with the score at the end and an opportunity to play again. While the
draw_game_over method takes care of displaying the objects on the canvas, the
game_over method controls the creation and configuration of the frame.
This function restarts the game by stopping
the current game instance, creating a new one
with the same dimensions, and starting the
game again, allowing the user to have another
go.
Lastly, we recall ‘Game’ and this will set the
game's initial dimensions and launch the
game loop, enabling it to function and
communicate with the player via the frame's
graphical user interface.
A moment of reflection


Overall, I believe that our group has achieved what we set out to do. There were
lots of high points but there were definitely a few lows as well. We worked well as
a team, regularly having discord calls, and meeting up once a week to discuss
progress and our general communication was excellent. Certain parts of the
game we struggled with such as collisions but after a bit of work and assistance
we managed to overcome those.
If I were to do this project again there are not that many things that I would do
differently other than starting a bit earlier as I feel like we were panicking slightly
to get the game finished but in the end due to hard work, dedication and lots of
resilience we managed to break the barriers and submit a game that we were
happy with.
The hardest part of the game for me personally was the animations that were
implemented. Having to watch numerous videos on how to implement them and
it failed loads of time, but eventually, I got there and assisted my team along the
way. I am glad that our group worked really well together and I would love to work
with them again.


Conclusion
To sum up, our team has successfully incorporated all essential ideas into our 2D
game, ensuring that it functions flawlessly each and every time. We have also
demonstrated intuition in our implementation of intricate algorithms.
Ultimately, we discovered that a little more time is required to completely
integrate important ideas like collisions between multiple objects as we are new
to programming at this level but fortunately, our team worked well together and
finished Iron Fist swiftly.
