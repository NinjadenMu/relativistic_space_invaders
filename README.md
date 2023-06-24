# Relativistic Space Invaders
Relativistic Space Invaders is a spin-off of the classic space invaders game (and my AP Physics C final project).  The player controls a ship capable of speeds up to 0.9c, so the effects of special relativity can be observed.  
You can view the gameplay of level 1 here:
https://drive.google.com/file/d/1j__0-WCqRcV4ePAUkw7cJ4bmUe_t6P_u/view?usp=sharing
<br>
<br>
The relativistic effects are rendered by treating the player's ship as a stationary observer with everything else moving relative to it.  Lorentz time dilation and length contraction follow the exact mathematical models a real-world object would.  
<br>
The relative velocities between entities, which the time dilation and length contraction formulas need, are also modeled by the real-world relativistic velocity addition magnitude formulas (velocities near the speed of light can't simply be added - otherwise, a ball thrown at 0.3c from a train cart moving at 0.8c would have a velocity of 1.1c).  Because the player and the aliens move along parallel lines, we know their direction is simply parallel to the line they move along (direction is important because length contraction only occurs in the direction of relative velocity).  However, because the velocity vectors between the player and the projectiles aren't parallel or antiparallel, there's no easy way to calculate the direction of their relative velocity vector.  Therefore, the effects are rendered as if the direction is parallel to the line of motion of the player, even though this is not strictly physically accurate.
<br>
<br>
Time Dilation and Length Contraction Formulas
<br>
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/656eea02-d364-4f9b-b143-f82921d33ae5">
<br>
<br>
Velocity Addition Magnitude Formulas:
<br>
Parallel:
<br>
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/d448a753-f5ec-4cd6-8433-2a1783c5c54b">
<br>
<br>
Perpendicular:
<br>
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/bebb3809-711c-4c2b-bc6a-69b289439142">
<br>
<br>
Observe Length contraction in action - notice how the aliens and bullets appear "squished":
<br>
<img width="600" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/2614262a-882d-437d-a960-85f5e5917673">
<br>
<br>
In addition to realistic relativistic effects, the player-controlled spaceship also obeys Newton's laws and basic kinematics.  Unlike the original Space Invaders, the player can't instantly start and stop.  Instead, momentum is conserved and the player must slowly accelerate to their max speed.
<br>
The player can choose between 4 difficulty settings (Including the YIKUAN difficulty, made for those who complain that games are too easy).  The difficulty settings vary the amount of health the player starts with, how fast they regain their shield, how fast the enemy regains their shield, and how fast the enemy moves and shoots.
<br>
<img width="600" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/d03892dc-b060-4117-a70e-38766457a2f0">
<br>
<br>
The player will then be able to play through an infinite number of procedurally generated levels that gradually up the difficulty by adding new aliens, upgrading existing aliens, or adding more rows of aliens. 
<br>
<img width="600" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/333e9dde-a9d9-435c-9e2d-20991a3854b5">
<br>


 
 
