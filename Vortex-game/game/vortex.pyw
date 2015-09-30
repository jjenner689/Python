import math, random
from livewires import games, color

games.init(screen_width = 1000, screen_height = 750, fps =50)



class Pacman(games.Sprite):

    SPEED = 2.5
    image_pacman_left = games.load_image("pacman_left.png")
    image_pacman_right = games.load_image("pacman_right.png")
    image_pacman_dead_right = games.load_image("pacman_dead_right.png")
    image_pacman_dead_left = games.load_image("pacman_dead_left.png")
    image_pacman_wall_right = games.load_image("pacman_wall_right.png")
    image_pacman_wall_left = games.load_image("pacman_wall_left.png")
    image_pacman_left_invulnerable = games.load_image("pacman_left_invulnerable.png")
    image_pacman_right_invulnerable = games.load_image("pacman_right_invulnerable.png")

    def __init__(self, game, x = games.screen.width/2,
                 y=games.screen.height/2 + 100, dx = 0, dy = 0):

        super(Pacman, self).__init__(
            image = Pacman.image_pacman_left,
            x = x, y = y, dx = dx, dy = dy)

        self.game = game #Ensure all sprites relate to object game
        self.name = "pacman" 
        self.wall_travel_lifespan = 0 #Time player can travel across the screen
        self.dead = False
        self.game.all_sprites.append(self)
        self.is_invulnerable = False
        self.invulnerable_time = 0 #Time player is invulnerable
        self.speed_time = 0 #Time player has enhanced speed
        self.reverse_time = 0 #Time player has revered controls
        self.speed_constant = 1 #Factor player is faster/slower than normal speed
        self.delay = 400

    def die(self):
        """Function freezes pacman when caught by ghost and shows the white (dead) pacman"""

        if self.image == Pacman.image_pacman_left:
            self.image = Pacman.image_pacman_dead_right

        elif self.image == Pacman.image_pacman_right:
            self.image = Pacman.image_pacman_dead_left

        self.dead = True

    def calc_xdistance(self, target):
        """Function calculates the distance across the x-axis to a target"""
        xdistance = target.x - self.x
        return xdistance

    def calc_ydistance(self, target):
        """Function calculates the distance across the y-axis to a target"""
        ydistance = target.y - self.y
        return ydistance

    def resultant_distance(self, xdistance, ydistance):
        """Function calculates the resultant distance from the x and y components"""
        resultant = (xdistance**2 + ydistance**2)**0.5
        return resultant

    def nearest_vortex_destination(self):
        """Functions shows the destination of the vortex (shown as gold image) closest to pacman when space-bar is pressed"""

        if games.keyboard.is_pressed(games.K_SPACE):
            vortexes = []
            for vortex in self.game.vortexes: #Loops over all vortexes
                xdistance = self.calc_xdistance(vortex)
                ydistance = self.calc_ydistance(vortex)
                total_distance = self.resultant_distance(xdistance = xdistance,
                                                         ydistance = ydistance)
                i = [total_distance, vortex] #Gives vortex and it's associated distance from player
                vortexes.append(i) 
            closest_vortex = min(vortexes)[1] 
            vortex_destination = Vortex_Destination(game = self.game,
                                                    x = closest_vortex.xmirror,
                                                    y = closest_vortex.ymirror)
            games.screen.add(vortex_destination) # Adds image of vortex destination when space bar is held down"""
                

    def control(self, image_pacman_left, image_pacman_right, speed_constant = 1):
        """Function enables player to control pacman using arrow keys"""

        if games.keyboard.is_pressed(games.K_LEFT):
            self.image = image_pacman_left
            self.angle = 0
            self.dx = -Pacman.SPEED*speed_constant
            self.dy = 0
            
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.image = image_pacman_right
            self.angle = 0
            self.dx = Pacman.SPEED*speed_constant
            self.dy = 0

        if games.keyboard.is_pressed(games.K_UP):
            self.image = image_pacman_right
            self.angle = 270
            self.dy = -Pacman.SPEED*speed_constant
            self.dx = 0
            
        if games.keyboard.is_pressed(games.K_DOWN):
            self.image = image_pacman_right
            self.angle = 90
            self.dy = Pacman.SPEED*speed_constant
            self.dx = 0

    def reverse(self, image_pacman_left, image_pacman_right, speed_constant = 1):
        """Function enables player to control pacman using arrow keys although directions are reversed"""

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.image = image_pacman_left
            self.angle = 0
            self.dx = -Pacman.SPEED*speed_constant
            self.dy = 0
            
        if games.keyboard.is_pressed(games.K_LEFT):
            self.image = image_pacman_right
            self.angle = 0
            self.dx = Pacman.SPEED*speed_constant
            self.dy = 0

        if games.keyboard.is_pressed(games.K_DOWN):
            self.image = image_pacman_right
            self.angle = 270
            self.dy = -Pacman.SPEED*speed_constant
            self.dx = 0
            
        if games.keyboard.is_pressed(games.K_UP):
            self.image = image_pacman_right
            self.angle = 90
            self.dy = Pacman.SPEED*speed_constant
            self.dx = 0

        self.reverse_time -= 1
        
    def pacman_wall(self):
        """Allows pacman to travel through the walls (edges) of the games screen"""

        self.control(image_pacman_left = Pacman.image_pacman_wall_left,
                     image_pacman_right = Pacman.image_pacman_wall_right,
                     speed_constant = self.speed_constant)

        if self.top > games.screen.height:
                self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width

        self.wall_travel_lifespan -= 1

    def invulnerability(self):
        """Makes pacman invulnerable"""
        
        self.is_invulnerable = True
        self.invulnerable_time = 500

    def pacman_dead(self):

        self.dx = 0
        self.dy = 0

    def pacman_speed(self):
        """Increases pacman's speed by 1.5x"""

        if self.speed_time > 0:
            self.speed_constant = 1.5
            self.speed_time -= 1
        else:
            self.speed_constant = 1

        
    def pacman_invulnerable(self):
        """Gives Pacman invulnerable image and makes invulnerable"""
        self.control(image_pacman_left = Pacman.image_pacman_left_invulnerable,
                     image_pacman_right = Pacman.image_pacman_right_invulnerable,
                     speed_constant = self.speed_constant)
        if self.invulnerable_time == 0:
            self.is_invulnerable = False
        self.invulnerable_time -= 1

        
    def pacman_normal(self):
        """Normal pacman control and movement when no powerups in effect"""

        self.control(image_pacman_left = Pacman.image_pacman_left,
                     image_pacman_right = Pacman.image_pacman_right,
                     speed_constant = self.speed_constant)

        if self.top < 5:
            self.top = 5

        if self.bottom > games.screen.height-5:
            self.bottom = games.screen.height-5

        if self.left < 5:
            self.left = 5
            
        if self.right > games.screen.width-5:
            self.right = games.screen.width-5

        

    def update(self):

        if self.delay > 0:
            self.delay -= 1
            return None

        self.game.check_powerup() #Random chance of powerup appearing

        self.nearest_vortex_destination() #Enables player to show nearest vortex destination


        if self.dead: #When dead

            self.pacman_dead()

        elif self.wall_travel_lifespan > 0: #When wall-travel powerup activated
            self.pacman_wall()
            

        else:
            
            self.pacman_normal()

        if self.reverse_time > 0: #When reverse control powerup activated
            self.reverse(image_pacman_left = Pacman.image_pacman_left,
                         image_pacman_right = Pacman.image_pacman_right)


        self.pacman_speed() #When speed powerup activated

        if self.is_invulnerable: #When invulnerable powerup activated
            self.pacman_invulnerable()


        

            

        

class Ghost(games.Sprite):

    SPEED = 1.5
    REACTION = 80 
    image_ghost = games.load_image("ghost.png")
    image_ghost_wall = games.load_image("ghost_wall.png")
    image_ghost_frozen = games.load_image("ghost_frozen.png")
    image_ghost_gold = games.load_image("ghost_catch.png")
    eaten_sound = games.load_sound("eat_ghost.wav")
    hit_sound = games.load_sound("punch.wav")
    

    def __init__(self, game, x = games.screen.width/2,
                 y=games.screen.height/5, dx = 0, dy = 0, reaction = 400):

        super(Ghost, self).__init__(image = Ghost.image_ghost,
                                    x = x,
                                    y = y,
                                    dx = dx,
                                    dy = dy)

        self.game = game
        self.reaction = reaction #Reaction is the time (number of frames) before ghost makes next decision on where to move
        self.name = "ghost"
        self.game.all_sprites.append(self)
        self.target = self.game.pacman #Sets initial target to the player
        self.freeze_time = 0 #Time ghost is frozen
        self.hit_time = 0 #Time ghost is under the influence of a collision
        self.x_ac = 0 #x-axis deceleration
        self.y_ac = 0#y-axis deceleration
        self.speed_time = 0 #Time ghost has enhanced speed
        self.reaction_constant = 1 #Factor by which reactions are reduced 
        self.reaction_constant_time = 0 #Time reactions are effected for
        self.gold_time = 0 #Time ghost is gold (eatable by pacman)
        self.is_gold = False 
        self.ghost_type = "1" #Primary ghost (ghost1)
    

    def check_collisions(self):
        """Functions handles ghost collisions"""
        if self.overlapping_sprites:
            for i in self.overlapping_sprites:
                if i.name == "pacman": #When collides with pacman
                    if i.is_invulnerable:
                        self.hit_time = 100 #If invulnerable gets hit away
                        Ghost.hit_sound.play()
                    elif self.is_gold:
                        Ghost.eaten_sound.play()
                        for i in range(10):
                            self.game.add_points()
                        if self.ghost_type == "1":
                            self.destroy()
                        else:
                            self.die() #So ghost type 2 (green) are deleted from their existing list
                        gold_message = games.Message(value = "Nice catch.... 100 points!!!",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4,
                                      lifetime = 200,
                                      is_collideable = False)

                        games.screen.add(gold_message)
                        if self.ghost_type == "1": #Only respawn main ghost
                            x = games.screen.height/2
                            y = -40
                            self.game.ghost1 = Ghost(game = self.game, x = x, y = y)
                            games.screen.add(self.game.ghost1)
                        
                    else:
                        self.dx = 0
                        self.dy = 0
                        self.reaction = -1
                        i.game.death() #Pacman dies and ghost also stops moving
                

    def change_reaction(self):
        if self.reaction_constant_time > 0:
            self.reaction_constant = 0.25
            self.reaction_constant_time -= 1
        else:
            self.reaction_constant = 1
        
            

    def eat_powerup(self):
        """Reduced reactions speed when close to powerup so doesn't hover around it"""
        if self.game.powerup != None:
            powerup_distance = self.find_target_distance(self.game.powerup)
            if powerup_distance < 60:
                if self.reaction > 20:
                    self.reaction = 20


    def hit_away(self):
        """Returns speed and direction of travel of pacman""" #Used so ghost is hit away in same direction pacman is travelling
        if self.game.pacman.dx > 0:
            acceleration = 0.05
            return "x", acceleration
        elif self.game.pacman.dx < 0:
            acceleration = -0.05
            return "x", acceleration
        elif self.game.pacman.dy > 0:
            acceleration = 0.05
            return "y", acceleration
        elif self.game.pacman.dy < 0:
            acceleration = -0.05
            return "y", acceleration
        
           

    def calc_xdistance(self, target):
        xdistance = target.x - self.x
        return xdistance

    def calc_ydistance(self, target):
        ydistance = target.y - self.y
        return ydistance

    def calc_xdirection(self, target):
        """returns x direction from ghost to pacman""" #Either +ve or -ve direction
        xdistance = self.calc_xdistance(target)
        
        if 0 <= xdistance <= games.screen.width/2:
            xdirection = 1
            return xdirection

        elif xdistance > games.screen.width/2:
            xdirection = -1
            return xdirection

        elif -games.screen.width/2 <= xdistance < 0:
            xdirection = -1
            return xdirection

        elif xdistance < -games.screen.width/2:
            xdirection = 1
            return xdirection

    def calc_ydirection(self, target):
        """returns y direction from ghost to pacman""" #Either +ve or -ve direction
        ydistance = self.calc_ydistance(target)
        
        if 0 <= ydistance <= games.screen.height/2:
            ydirection = 1
            return ydirection

        elif ydistance > games.screen.height/2:
            ydirection = -1
            return ydirection

        elif -games.screen.height/2 <= ydistance < 0:
            ydirection = -1
            return ydirection

        elif ydistance < -games.screen.height/2:
            ydirection = 1
            return ydirection

    def resultant_distance(self, xdistance, ydistance):
        resultant = (xdistance**2 + ydistance**2)**0.5
        return resultant

    def modulus(self, number):
        """Returns modulus of a number"""
        if number >= 0:
            return number
        else:
            number = number*-1
            return number

    def move(self, target, speed_constant = 1):
        """Function sets velocity of ghost to head towards a given target"""
        xdistance = self.calc_xdistance(target)
        ydistance = self.calc_ydistance(target)
        xdirection = self.calc_xdirection(target)
        ydirection = self.calc_ydirection(target)

        if self.modulus(xdistance) <= self.modulus(ydistance): #Ghost travels across the axis who's distance is furthest from the target 
            self.dx = 0
            self.dy = Ghost.SPEED*ydirection*speed_constant
        else:
            self.dy = 0
            self.dx = Ghost.SPEED*xdirection*speed_constant

    def move_away(self, target, speed_constant = 1):
        """Function sets velocity of ghost to head away from a given target"""
        xdistance = self.calc_xdistance(target)
        ydistance = self.calc_ydistance(target)
        xdirection = self.calc_xdirection(target)
        ydirection = self.calc_ydirection(target)

        if self.modulus(xdistance) <= self.modulus(ydistance): #Ghost travels across the axis who's distance is furthest from the target 
            self.dx = Ghost.SPEED*xdirection*speed_constant*-1
            self.dy = 0
        else:
            self.dy = Ghost.SPEED*ydirection*speed_constant*-1
            self.dx = 0

    def avoid_vortex(self):
        """Function makes ghost travel around vortex when not intending to travel through it"""

        if self.dy == 0:
            ydirection = self.calc_ydirection(target = self.game.pacman)
            if self.dx == Ghost.SPEED: #If x speed is in positive x direction
                for i in range(self.reaction): #Calculates future position of ghost by looping over each frame left before next decision
                    xahead = self.right + self.dx*i #xahead gives the future x position
                    if self.overlaps_vortex(right=xahead): #If future position will collide with the vortex
                        self.dx = 0 #Stop the ghost moving in the current direction
                        self.dy = Ghost.SPEED*ydirection #Make ghost move across other axis
                        
            elif self.dx == -Ghost.SPEED: #Same applies for other all 4 directions of travel
                for i in range(self.reaction): 
                    xahead = self.left + self.dx*i
                    if self.overlaps_vortex(left=xahead):
                        self.dx = 0
                        self.dy = Ghost.SPEED*ydirection
                        
        elif self.dx == 0:
            xdirection = self.calc_xdirection(target = self.game.pacman)
            if self.dy == Ghost.SPEED:
                for i in range(self.reaction):
                    yahead = self.bottom + self.dy*i
                    if self.overlaps_vortex(bottom=yahead):
                        self.dy = 0
                        self.dx = Ghost.SPEED*xdirection
                       
            elif self.dy == -Ghost.SPEED:
                for i in range(self.reaction):
                    yahead = self.top + self.dy*i
                    if self.overlaps_vortex(top=yahead):
                        self.dy = 0
                        self.dx = Ghost.SPEED*xdirection


    def overlaps_vortex(self, left = None,
                        right = None, top = None,
                        bottom = None):
        """Returns true if self position overlaps any of the existing vortexes"""

        if left == None:
            left = self.left
        if right == None:
            right = self.right
        if top == None:
            top = self.top
        if bottom == None:
            bottom = self.bottom

        for vortex in self.game.vortexes: #Looped over all vortexes

            if (left in range(vortex.left, vortex.right + 1) or right in \
                range(vortex.left, vortex.right + 1)) and \
                (top in range(vortex.top, vortex.bottom + 1) or bottom \
                 in range(vortex.top, vortex.bottom + 1)): #If either side of self overlaps a vortex

                if vortex.telespan < 200: #Ghost will travel through freshly spawned (non-active) vortexes

                    return True #Return true if overlap

        

    def portal_target(self, target):
        """Function returns the minimum distance to the target travelling
           via a vortex and the associated vortex it travels through"""

        total_distances = [] #list which will contain the distance to the target via a portal for each existing portal

        for vortex in self.game.vortexes: #loops through all existing portals
            x_self_portal=self.modulus(self.calc_xdistance(vortex)) #x distance from self to portal 
            y_self_portal=self.modulus(self.calc_ydistance(vortex)) #y distance from self to portal
            x_portal_target=self.modulus(vortex.calc_xmirrordistance(target)) #xdistance from portal destination to target
            y_portal_target=self.modulus(vortex.calc_ymirrordistance(target)) #ydistance from portal destination to target
            totalx = x_self_portal + x_portal_target #total x distance from self to target via portal
            totaly = y_self_portal + y_portal_target #total y distance from self to target via portal
            total = self.resultant_distance(xdistance = totalx, #resultant distance to travel from self to target via portal (not totally correct but close)
                                            ydistance = totaly)
            i = [total, vortex] #gives vortex and the associated distance to it
            total_distances.append(i)
        min_total_distance = min(total_distances)
        return min_total_distance #returns the minimum distance to the target and the associated portal it travels through

    def portal_target2(self, target):
        """Function returns the minimum distance to the target travelling
           via 2 vortexes and the associated vortex it travels through next"""

        total_distances = [] #list which will contain the distance to the target via 2 portals for all paired combinations of existing portals

        for vortex in self.game.vortexes:
            distance_1=self.portal_target(vortex)[0] #minimum distance to the second portal travelling via the first portal (loops over all first portals)
            distance_2=vortex.portal_target(target)[0] #distance from second portal destination to target (in this case self == portal travels through)
            total = distance_1 + distance_2 #total distance to travel using both portals
            target_portal = self.portal_target(vortex)[1] #the first portal to travel through (the one the ghost will head to first)
            i = [total, target_portal] #gives distance and the target (first portal)
            total_distances.append(i)
        min_total_distance = min(total_distances) #Finds the minimum route via 2 portals 
        return min_total_distance #returns the route (gives target portal (head to first) and total distance)

    def portal_target3(self, target):
        """Function returns the minimum distance to the target travelling
           via 3 vortexes and the associated vortex it travels through next"""

        total_distances = [] #list which will contain the distance to the target via 3 portals for all paired combinations of existing portals

        for vortex in self.game.vortexes:
            distance_1=self.portal_target2(vortex)[0] #minimum distance to the third portal travelling via the first portal (loops over all first portals)
            distance_2=vortex.portal_target(target)[0] #distance from third portal destination to target (in this case self == portal travels through)
            total = distance_1 + distance_2 #total distance to travel using all three portals
            target_portal = self.portal_target2(vortex)[1] #the first portal to travel through (the one the ghost will head to first)
            i = [total, target_portal] #gives distance and the target (first portal)
            total_distances.append(i)
        min_total_distance = min(total_distances) #Finds the minimum route via 3 portals
        return min_total_distance #returns the route (gives target portal (head to first) and total distance)


    def find_target_distance(self, target):
        """Finds and returns the total distance to a given target"""

        xdistance = self.modulus(self.calc_xdistance(target))
        ydistance = self.modulus(self.calc_ydistance(target))
        target_distance = self.resultant_distance(xdistance = xdistance,
                                                   ydistance = ydistance)
        return target_distance

    def show_vortex_destination(self, target):
        """Shows where ghost will appear from vortex"""

        if target == self.game.pacman:
            return None
        
        elif target.name == "vortex":
            distance_to_target = self.find_target_distance(target)
            
            if distance_to_target < 100:

                destination = Vortex_Destination_Ghost(game = self.game, x =target.xmirror,
                                                       y = target.ymirror)
                games.screen.add(destination)


    def find_target(self):
        """Returns the target the ghost will head towards""" 

        route_distances = []

        no_portal_distance = self.find_target_distance(self.game.pacman) #Distance to pacman travelling via no vortexes

        if self.game.powerup != None:
            powerup_distance = self.find_target_distance(self.game.powerup) #Distance to powerup if available
            route_distances.append(powerup_distance) 
            
            

        one_portal_route = self.portal_target(self.game.pacman) #one_portal_route gives the quickest distance travelling via one vortex and the associated vortex
        one_portal_distance=one_portal_route[0] #The distance of that route
        

        two_portal_route = self.portal_target2(self.game.pacman) #two_portal_route gives the quickest distance travelling via two vortexes and the associated first portal (ghost will find the second once it travels through the first)
        two_portal_distance=two_portal_route[0] #The distance of that route

        #three poral distance is commented out as it requires too much computational power it slows game down at higher levels
        #three_portal_route = self.portal_target3(self.game.pacman)
        #three_portal_distance=three_portal_route[0]

        route_distances.append(no_portal_distance) #Add all the distances to one list
        route_distances.append(one_portal_distance)
        route_distances.append(two_portal_distance)
        #route_distances.append(three_portal_distance)

        min_route_distance = min(route_distances) #Gives the quickest of all previous routes 

        try: #Need to use "try" as if no powerup available error occurs
            #Connects quickest route with the associated target and returns it
            
            if (min_route_distance == one_portal_distance) and (one_portal_route[1].telespan == 0): #Ensure ghost doesn't target portal which has recently spawned
                return one_portal_route[1]

            elif (min_route_distance == two_portal_distance) and (two_portal_route[1].telespan == 0):
                return two_portal_route[1]

            #elif (min_route_distance == three_portal_distance) and (three_portal_route[1].telespan ==0):
                #return three_portal_route[1]
        
            elif min_route_distance == powerup_distance:
                return self.game.powerup

            else:
                return self.game.pacman
        except:
            
            if (min_route_distance == one_portal_distance) and (one_portal_route[1].telespan == 0):
                return one_portal_route[1]

            elif (min_route_distance == two_portal_distance) and (two_portal_route[1].telespan == 0):
                return two_portal_route[1]

            #elif (min_route_distance == three_portal_distance) and (three_portal_route[1].telespan ==0):
                #return three_portal_route[1]

            else:
                return self.game.pacman

    def update(self):


        if (self.bottom > games.screen.height) or (self.top < 0) or \
        (self.right > games.screen.width) or (self.left < 0):
            self.image = Ghost.image_ghost_wall # Shows ghost wall image when travelling across boundaries

        else:
            self.image = Ghost.image_ghost
        #Enables ghost to move across each side of game screen    
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width

        if self.freeze_time > 0:
            self.dx = 0
            self.dy = 0
            self.freeze_time -= 1
            self.image = Ghost.image_ghost_frozen
            return None #Exits update when performed so ghost stays still

        if self.hit_time > 0: #If ghost hit by pacman when invulnerable
            if self.hit_time == 100: #When immediately hit
                self.dx = 0 #Reset speed to 0
                self.dy = 0
                self.direction, self.acceleration = self.hit_away() #Returns direction and accelration from hit_away function
                if self.direction == "x":
                    self.dx = self.game.pacman.dx*2 #Gives initial speed of double pacman's (in same direction)
                elif self.direction == "y":
                    self.dy = self.game.pacman.dy*2
                    

            elif self.hit_time < 100: #After collides with pacman
                if self.direction == "x":
                    self.dx -= self.acceleration #Decelerates ghost
                elif self.direction == "y":
                    self.dy -= self.acceleration
            self.hit_time -= 1
            return None #Exits update so ghost movement only affected by collision

        if self.reaction > 0:
            self.reaction -= 1

        if self.gold_time > 0: #Applies when gold powerup is activated
            self.image = Ghost.image_ghost_gold
            self.is_gold = True
            self.gold_time -=1
            if self.reaction == 0:
                self.move_away(target=self.game.pacman)
                self.reaction = int(Ghost.REACTION*self.reaction_constant) #Resets reaction
            self.avoid_vortex()

        elif self.gold_time == 0:
            self.is_gold = False
            
            if self.reaction == 0: #When reaction reaches 0, ghost makes decision
            
                self.target=self.find_target() #Finds target (pacman, vortex or powerup)

                if self.speed_time > 0:
                    speed_constant = Pacman.SPEED/Ghost.SPEED #Sets speed constant (so that ghost speed will = pacman speed) when powerup activated
                    self.move(target=self.target, speed_constant = speed_constant)
                else:
                    self.move(target=self.target, speed_constant = 1)
                self.reaction = int(Ghost.REACTION*self.reaction_constant) #Resets reaction

        self.eat_powerup() #Ensures doesn't get stuck next to powerup (when reactions are slower)

        self.change_reaction() #Checks for reaction-change powerup

        if self.speed_time > 0:
                self.speed_time -= 1

        self.check_collisions() #Handles ghost collisions

        if self.target == self.game.pacman: #Avoids travelling through vortex if targeting pacman
            self.avoid_vortex()

        self.show_vortex_destination(target = self.target) #Shows destination if ghost about to travel through vortex

class Ghost2(Ghost):

    image_ghost = games.load_image("ghost2.png")

    def __init__(self, game, x, y, dx = 0, dy =0, reaction = 0):

        super(Ghost2, self).__init__(
                                     x = x,
                                     y = y,
                                     dx = dx,
                                     dy = dy,
                                     game= game,
                                     reaction = reaction)

        self.ghost_type = "2" #Secondary ghost (ghost2)
        self.game.ghost2s.append(self)
        

    def update(self):

        super(Ghost2, self).update()

        if (self.bottom > games.screen.height) or (self.top < 0) or \
        (self.right > games.screen.width) or (self.left < 0):
            self.image = Ghost.image_ghost_wall

        else:
            if self.is_gold:
                self.image = Ghost.image_ghost_gold
            else:
                self.image = Ghost2.image_ghost

    def die(self):
        self.game.ghost2s.remove(self)
        self.destroy()
       

class Apple(games.Sprite):

    image = games.load_image("apple.png")
    sound = games.load_sound("bite.wav")

    def __init__(self, game):

        super(Apple,self).__init__(image = Apple.image,
                                   x = random.randint(10, games.screen.width - 10),
                                   y = random.randint(10, games.screen.height - 10),
                                   dx = 0,
                                   dy = 0)

        self.game = game
        self.name = "apple"
        self.game.all_sprites.append(self)

    def eaten(self):

        self.game.add_points() #Give points when apple eaten
        self.destroy()
        self.game.nextapple() #Spawns next apple

    def update(self):

        if self.overlapping_sprites:
            for i in self.overlapping_sprites:
                if i.name == "pacman": #Only reacts with pacman
                    Apple.sound.play()
                    self.eaten()

class Blank(games.Sprite):
    """Represents the other end (destination) of each vortex"""

    image = games.load_image("blank.png") 

    def __init__(self, game):

        super(Blank, self).__init__(image = Blank.image,
                                    x = random.randint(50, games.screen.width - 50),
                                    y = random.randint(50, games.screen.height - 50),
                                    dx = 0,
                                    dy = 0)
        self.game = game
        self.name = "blank"

    def find_overlap(self):
        """Returns true if overlaps with another vortex or blank (vortex destination)"""

        if self.overlapping_sprites:
            for i in self.overlapping_sprites:
                if (i.name == "vortex") or (i.name == "blank"):
                    return True

class Vortex_Destination(games.Sprite):
    """Gold vortex which shows destination of vortex when space is held down"""
    #Same position as a Blank

    image = games.load_image("vortex_gold.png")

    def __init__(self, game, x, y):

        super(Vortex_Destination, self).__init__(image = Vortex_Destination.image,
                                                 x = x,
                                                 y = y,
                                                 dx = 0,
                                                 dy = 0)

        self.game = game
        self.name = "vortex_destination"
        

    def update(self):

        self.destroy() #Portal disappears once space bar is no longer pressed or pacman moves to a closer portal

class Vortex_Destination_Ghost(games.Sprite):
    """Gold vortex which shows destination of vortex when space is held down"""
    #Same position as a Blank

    image = games.load_image("vortex_red.png")

    def __init__(self, game, x, y):

        super(Vortex_Destination_Ghost, self).__init__(image = Vortex_Destination_Ghost.image,
                                                 x = x,
                                                 y = y,
                                                 dx = 0,
                                                 dy = 0)

        self.game = game
        self.name = "vortex_destination_ghost"
        

    def update(self):

        self.destroy() #Portal disappears once space bar is no longer pressed or pacman moves to a closer portal        

        
                                           
        
    

class Vortex(games.Sprite):

    image = games.load_image("vortex_white.png")
    sound = games.load_sound("vortex.wav")

    def __init__(self, game, xmirror, ymirror):

        super(Vortex, self).__init__(image = Vortex.image,
                                     x = random.randint(50, games.screen.width - 50),
                                     y = random.randint(50, games.screen.height - 50),
                                     dx = 0,
                                     dy = 0)

        self.game = game
        self.name = "vortex"
        self.telespan = 400 #Time after vortex has spawned before it can be used again
        self.xmirror = xmirror #Position of vortex destination
        self.ymirror = ymirror #Position of vortex destination
        self.x2 = self.x #Use this is store original x position
        self.y2 = self.y #Use this is store original y position
        self.game.vortexes.append(self) #Add to list of vortexes

    def find_overlap(self):
        """Returns true if overlaps another vortex or blank (destination of another vortex)"""

        if self.overlapping_sprites:
            for i in self.overlapping_sprites:
                if (i.name == "vortex") or (i.name == "blank"):
                    return True

    def calc_xdistance(self, target):
        xdistance = target.x - self.x
        return xdistance

    def calc_ydistance(self, target):
        ydistance = target.y - self.y
        return ydistance

    def calc_xmirrordistance(self, target):
        """returns the x distance from the vortex destination to the target"""
        xdistance = target.x - self.xmirror
        return xdistance

    def calc_ymirrordistance(self, target):
        """returns the y distance from the vortex destination to the target"""
        ydistance = target.y - self.ymirror
        return ydistance

    def resultant_distance(self, xdistance, ydistance):
        resultant = (xdistance**2 + ydistance**2)**0.5
        return resultant

    def modulus(self, number):
        if number >= 0:
            return number
        else:
            number = number*-1
            return number

    def update(self):

        self.telespan -= 1
        if self.telespan < 0:
            self.telespan = 0

        if self.overlapping_sprites:
            for i in self.overlapping_sprites:
                if i.name == "apple":
                    i.destroy()
                    self.game.nextapple()

                elif i.name == "powerup":
                    i.die()
                    

                elif i.name == "blank":
                    continue

                elif i.name == "vortex_destination":
                    continue

                elif i.name == "vortex_destination_ghost":
                    continue

                elif i.name == "life":
                    continue

                else: #ghost/pacman
                    if self.telespan == 0:
                        Vortex.sound.play()
                        i.x = self.xmirror #Move ghost/pacman to mirror location
                        i.y = self.ymirror
                        self.x = self.xmirror #Move vortex to mirror location
                        self.y = self.ymirror
                        self.xmirror = self.x2 #Make previous location the mirror location
                        self.ymirror = self.y2
                        self.x2 = self.x #Reset x2 value
                        self.y2 = self.y #Reset y2 value
                        self.telespan = 400

    def portal_target(self, target):
        """Function returns the minimum distance to the target travelling
           via a vortex and the associated vortex it travels through"""

        total_distances = [] #list which will contain the distance to the target via a portal for each existing portal

        for vortex in self.game.vortexes: #loops through all existing portals
            x_self_portal=self.modulus(self.calc_xdistance(vortex)) #x distance from self to portal 
            y_self_portal=self.modulus(self.calc_ydistance(vortex)) #y distance from self to portal
            x_portal_target=self.modulus(vortex.calc_xmirrordistance(target)) #xdistance from portal destination to target
            y_portal_target=self.modulus(vortex.calc_ymirrordistance(target)) #ydistance from portal destination to target
            totalx = x_self_portal + x_portal_target #total x distance from self to target via portal
            totaly = y_self_portal + y_portal_target #total y distance from self to target via portal
            total = self.resultant_distance(xdistance = totalx, #resultant distance to travel from self to target via portal (not totally correct but close)
                                            ydistance = totaly)
            i = [total, vortex] #gives vortex and the associated distance to it
            total_distances.append(i)
        min_total_distance = min(total_distances)
        return min_total_distance #returns the minimum distance to the target and the associated portal it travels through             
                                     
                                     

class Powerup(games.Sprite):

    image = games.load_image("powerup.png")
    powerup_sound = games.load_sound("power_up.wav")
    ghost_powerup_sound = games.load_sound("ghost_powerup.wav")


    def __init__(self, game):

        super(Powerup, self).__init__(image = Powerup.image,
                                      x = random.randint(15, games.screen.width - 15),
                                      y = random.randint(15, games.screen.height - 15),
                                      dx = 0,
                                      dy = 0) 
        self.game = game
        self.lifespan = 600
        self.name = "powerup"
        self.game.all_sprites.append(self)
        self.game.powerup = self #Used so only one powerup can appear at a time
        self.telespan = 0 #just so rest works (update in ghost)

    def message_collision(self):
        """Function spaces out messages displayed at same time so they don't overlap"""
        space = 50*self.game.message_count #Space between messages showing simultaneously
        return space

    def reduce_message_count(self):
        self.game.message_count -= 1
        
    def update(self):

        if self.lifespan > 0:
            self.lifespan -= 1

        else:
            self.die()

        if self.overlapping_sprites:
            for i in self.overlapping_sprites: #Pacman (Player) powerups
                if i.name == "pacman":
                    Powerup.powerup_sound.play()
                    self.number = random.randint(1,6) #Make content of powerup random
                            
                    if self.number == 1:
                        i.wall_travel_lifespan = 400
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision() #Creates space between messages if more than one showing 
                        power_message = games.Message(value = "Wall Travel",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)
                    elif self.number == 2:
                        self.game.ghost1.freeze_time =500
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Freeze",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)
                    elif self.number == 3:
                        i.invulnerability()
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Invulnerabilty",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      after_death = self.reduce_message_count,
                                      lifetime = 200,
                                      is_collideable = False)

                        games.screen.add(power_message)
                    elif self.number == 4:
                        i.speed_time = 500
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Extra Fast",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)

                    elif self.number == 5:
                        self.die()
                        for i in range(3):
                            self.game.add_points()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Extra Points!!!",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)

                    elif self.number == 6:
                        self.die()
                        try:
                            for i in self.game.ghost2s:
                                i.gold_time = 600
                        except:
                            continue
                        self.game.ghost1.gold_time = 600

                        if self.game.ghost2s: #Says catch ghosts if more than one
                            self.game.message_count += 1
                            space = self.message_collision()
                            power_message = games.Message(value = "Catch the ghosts!!!",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                            games.screen.add(power_message)

                        else:
                            self.game.message_count += 1
                            space = self.message_collision()
                            power_message = games.Message(value = "Catch the ghost!!!",
                                      size = 45,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,                     
                                      is_collideable = False)

                            games.screen.add(power_message)
                            
                        

                    

                elif i.name =="ghost": #Ghost powerups
                    Powerup.ghost_powerup_sound.play()
                    self.number = random.randint(1,4)
                    if self.number == 1:
                        self.game.pacman.reverse_time = 500
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Reverse Controls!!!",
                                      size = 45,
                                      color = color.red,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)

                    elif self.number == 2:
                        i.speed_time = 500
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Faster Ghost!!!",
                                      size = 45,
                                      color = color.red,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)

                    elif self.number == 3:
                        i.reaction_constant_time = 500
                        
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Faster Ghost reactions!!!",
                                      size = 45,
                                      color = color.red,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)

                    elif self.number == 4:
                        x = games.screen.height/2
                        y = 0
                        ghost2 = Ghost2(game = self.game, x = x, y = y)
                        games.screen.add(ghost2)
                        self.die()
                        self.game.message_count += 1
                        space = self.message_collision()
                        power_message = games.Message(value = "Extra Ghost!!!",
                                      size = 45,
                                      color = color.red,
                                      x=games.screen.width/2,
                                      y=games.screen.height/4 + space,
                                      lifetime = 200,
                                      after_death = self.reduce_message_count,
                                      is_collideable = False)

                        games.screen.add(power_message)
                    
                    
                        

    def die(self):
        self.destroy()
        self.game.powerup = None

class Life(games.Sprite):
    image = games.load_image("life.png")

    def __init__(self, game, num): #Num = number of lives

        super(Life, self).__init__(image = Life.image,
                                   x = 20*(num+1) - 5,
                                   y = 15,
                                   dx = 0,
                                   dy = 0)
        self.name = "life"
        self.game = game
        self.game.all_sprites.append(self)

     

class Game(object):

    death_sound = games.load_sound("death.wav")
    game_over_sound = games.load_sound("game_over.wav")
    level_up_sound = games.load_sound("level_up.wav")
    ding_sound = games.load_sound("ding.wav")
    start_sound = games.load_sound("start.wav")

    def __init__(self):

        self.level = 1

        self.lives = 2
        
        
        self.points = games.Text(value = 0,
                                 size = 40,
                                 color = color.white,
                                 top = 5,
                                 right = games.screen.width - 10,
                                 is_collideable = False)
        games.screen.add(self.points)

        self.the_level = games.Text(value = self.level,
                                 size = 40,
                                 color = color.white,
                                 bottom = games.screen.height - 5,
                                 right = games.screen.width - 10,
                                 is_collideable = False)

        games.screen.add(self.the_level)


        self.all_sprites = [] #List of sprites which are deleted on restart (when die)
        self.vortexes = [] #List of vortexes
        self.powerup=None
        self.allow_death = True
        self.ghost2s =[] #List of additional green ghosts
        self.message_count = 0 #Number of messages currently displayed
        


    def play(self):
        """Sets background and mainloop"""

        backgroundy=games.load_image("background.png", transparent = False)
        games.screen.background = backgroundy

        self.create_vortex()

        self.go()

        games.mouse.is_visible = False

        games.screen.mainloop()

    def go(self):
        """Spawns ghost and pacman with number of lives"""

        for i in range(self.lives):
            life = Life(game = self, num = i) #Displays lives in top corner
            games.screen.add(life)

        self.pacman = Pacman(game = self)
        games.screen.add(self.pacman)
        
        self.ghost1 = Ghost(game = self)
        games.screen.add(self.ghost1)

        self.countdown3()

    def check_level(self):
        """Checks points and changes level every 100"""

        self.the_level.right = games.screen.width - 10
        self.points.right = games.screen.width - 10

        if self.points.value%100 == 0:
            self.level += 1
            self.the_level.value = self.level
            self.level_message()

    def level_message(self):
        """Displays new level"""

        Game.level_up_sound.play()

        level = games.Message(value = "Level: " + str(self.level),
                               size = 40,
                               color = color.yellow,
                               x=games.screen.width/2,
                               y=games.screen.height/2,
                               lifetime = 100,
                               after_death = self.next_level,
                               is_collideable = False)

        games.screen.add(level)

    def create_vortex(self):
        """Creates vortex"""
        blank = Blank(game = self)
        games.screen.add(blank)
        vortex = Vortex(game = self, xmirror = blank.x,
                             ymirror = blank.y) #Vortex destination is at blank
        games.screen.add(vortex)
        while blank.find_overlap() or vortex.find_overlap(): #If vortex or it's destination (blank) overlaps previous vortexes, the vortex is deleted and readded until it doesn't overlap
            blank.destroy() 
            vortex.destroy()
            blank = Blank(game = self)
            games.screen.add(blank)
            vortex = Vortex(game = self, xmirror = blank.x,
                            ymirror = blank.y)
            games.screen.add(vortex)
        

    def next_level(self):
        """Moves up the level"""
        if (self.level)%3 == 0: #New vortex is created every 3rd level
           self.create_vortex()
           self.lives += 1
           life = Life(game = self, num = self.lives - 1) #New life is created every 3rd level
           games.screen.add(life)
        Pacman.SPEED += 0.03
        Ghost.SPEED += 0.03
        Ghost.REACTION -= 5
        self.extra_count =0 
        self.gold_count = 0
        if Ghost.REACTION < 1:
            Ghost.REACTION = 1

    def add_points(self):
        """Functions adds points and checks for level-up"""
        self.points.value += 10
        self.check_level()

        

    def death(self):
        """Takes away a life and restarts. If lives at 0 ends the game"""

        if self.allow_death:

            Game.death_sound.play()

            self.allow_death = False #So death message is only displayed once when caught
            

            if self.lives > 0:
                self.lives -= 1
                self.pacman.die()
                death = games.Message(value = "You got caught!!!!",
                                      size = 90,
                                      color = color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/2,
                                      lifetime = 200,
                                      after_death = self.restart,
                                      is_collideable = False)

                games.screen.add(death)
            

            elif self.lives == 0:
                self.end()

    def restart(self):
        """Restarts game keeping score and any vortexes"""

        for i in self.all_sprites: #Destroy all apples, powerups, ghost and pacman
            try:
                i.destroy()
            except:
                continue

        self.all_sprites = [] 

        self.ghost2s = []

        self.allow_death = True

        self.powerup = None

        self.go() #Restart with same points and vortexes

        

        
    def end(self):

        self.pacman.die()

        Game.game_over_sound.play()

        game_over = games.Message(value = "Game Over",
                                  size = 90,
                                  color = color.yellow,
                                  x=games.screen.width/2,
                                  y=games.screen.height/2,
                                  lifetime = 200,
                                  after_death = games.screen.quit,
                                  is_collideable = False)

        games.screen.add(game_over)

    def countdown3(self):

        Game.ding_sound.play()

        count3 = games.Message(value = "3",
                               size = 90,
                               color = color.yellow,
                               x=games.screen.width/2,
                               y=games.screen.height/2,
                               lifetime = 100,
                               after_death = self.countdown2,
                               is_collideable = False)

        games.screen.add(count3)

    def countdown2(self):

        Game.ding_sound.play()

        count2 = games.Message(value = "2",
                               size = 90,
                               color = color.yellow,
                               x=games.screen.width/2,
                               y=games.screen.height/2,
                               lifetime = 100,
                               after_death = self.countdown1,
                               is_collideable = False)

        games.screen.add(count2)

    def countdown1(self):

        Game.ding_sound.play()

        count1 = games.Message(value = "1",
                               size = 90,
                               color = color.yellow,
                               x=games.screen.width/2,
                               y=games.screen.height/2,
                               lifetime = 100,
                               after_death = self.countdowngo,
                               is_collideable = False)

        games.screen.add(count1)

    def countdowngo(self):

        Game.start_sound.play()

        countgo = games.Message(value = "Go!",
                                size = 90,
                                color = color.yellow,
                                x=games.screen.width/2,
                                y=games.screen.height/2,
                                lifetime = 100,
                                after_death = self.nextapple,
                                is_collideable = False)

        games.screen.add(countgo)

    def check_powerup(self):
        """Randomly spawns a powerup"""
        if self.powerup == None: #Ensure only one powerup is spawned at a time
            num = random.randint(0, 1000)
            if num == 1:
                power = Powerup(game = self)
                games.screen.add(power)
        
            

    def nextapple(self):            
        self.apple = Apple(game = self)
        games.screen.add(self.apple)


                                  

def main():
    
    game=Game()
    game.play()

main()

