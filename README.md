# Relativistic Space Invaders
Relativistic Space Invaders is a spin-off of the classic space invaders game (and my AP Physics C final project).  However, the player controls a ship capable of speeds up to an 0.9c, so the effects of special relativity can be observed.  The relativistic effects are rendered by treating the player's ship as a stationary observer with everything else moving relative to it.  Lorentz time dilation and length contraction follow the exact mathematical models a real-world object would.  The relative velocities between entities, which the time dilation and length contraction formulas need, are also modeled by the real-world relativistic velocity addition magnitude formulas (velocities near the speed of light can't simply be added - otherwise, a ball thrown at 0.3c from a train cart moving at 0.8c would have a velocity of 1.1c).  Because the player and the aliens move along parallel lines, we know their direction is simply parallel to the line they move along.  However, because the velocity vectors between the player and the projectiles aren't parallel or antiparallel, there's no easy way to calculate the direction of their relative velocity vector.  Therefore, the effects are rendered as if their direction is parallel to the line of motion of the player, even though this is not strictly physically accurate.
<br>
Time Dilation and Length Contraction Formulas
<br>
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/656eea02-d364-4f9b-b143-f82921d33ae5">
<br>
Velocity Addition Magnitude Formulas:
<br>
Parallel:
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/d448a753-f5ec-4cd6-8433-2a1783c5c54b">
<br>
Perpendicular:
<img width="363" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/bebb3809-711c-4c2b-bc6a-69b289439142">
<br>
<br>
In addition to realistic relativistic effects, the player-controlled spaceship also obeys Newton's laws and basic kinematics.  Unlike the original Space Invaders, the player can't instantly start and stop.  Instead, momentum is conserved and the player must slowly accelerate to their max speed.
<br>
The player can choose between 4 difficulty settings and then proceed through an infinite number of levels, which get harder each time - adding stronger aliens, more aliens, or different aliens. 
<br>
<img width="848" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/d03892dc-b060-4117-a70e-38766457a2f0">
<br>
<img width="848" alt="image" src="https://github.com/NinjadenMu/relativistic_space_invaders/assets/68563142/333e9dde-a9d9-435c-9e2d-20991a3854b5">

 
 
