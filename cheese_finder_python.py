import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up screen and game variables
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cheese Finder")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up Rat
rat_speed = 5
boosted_speed = 8  # Speed bost after collecting candy
speed_boost_duration = 10000  # Duration of 10 second speed boost (in milliseconds) 
current_speed = rat_speed

# Set up items
cheese_radius = 8
cheeses = []
pizzas = []
candies = []
score = 0

# Set up font for score
font = pygame.font.SysFont("Arial", 24)

# Load the item collection sound effects
cheese_sound = pygame.mixer.Sound("point_2.mp3")

pizza_sound = pygame.mixer.Sound("point.mp3")  

candy_sound = pygame.mixer.Sound("point_3.mp3")

# Function to create a new cheese at a random location
def create_cheese():
    x = random.randint(30, WIDTH - 30)
    y = random.randint(30, HEIGHT - 30)
    return [x, y]

# Function to create a new pizza at a random location
def create_pizza():
    x = random.randint(30, WIDTH - 30)
    y = random.randint(30, HEIGHT - 30)
    return [x, y]

# Function to create a new candy at a random location
def create_candy():
    x = random.randint(30, WIDTH - 30)
    y = random.randint(30, HEIGHT - 30)
    return [x, y]

# Load images and resize
# Load rat image
rat_img = pygame.image.load("rat.png")  
rat_img = pygame.transform.scale(rat_img, (90, 90))

# Load background image
background_img = pygame.image.load("backgroundgame_muted_faded.png")  

# Load cheese image
cheese_img = pygame.image.load("cheese.png")  
cheese_img = pygame.transform.scale(cheese_img, (32, 32))  

# Load pizza image
pizza_img = pygame.image.load("pizza.png") 
pizza_img = pygame.transform.scale(pizza_img, (52, 52))  

# Load candy image
candy_img = pygame.image.load("candy.png")
candy_img = pygame.transform.scale(candy_img, (32, 62))

# Load speaker and mute icons
mute_icon = pygame.image.load("mute.png") 
mute_icon = pygame.transform.scale(mute_icon, (32, 32)) 
unmute_icon = pygame.image.load("unmute.png")  
unmute_icon = pygame.transform.scale(unmute_icon, (32, 32))

# Set up game loop
clock = pygame.time.Clock()

# Create initial cheese
cheeses.append(create_cheese())

# Initial rat position
rat_x, rat_y = WIDTH // 2, HEIGHT // 2

# Track the time of the speed boost
boost_end_time = 0  # The time when the speed boost should end

# Spawn pizza less frequently with a cool-down
last_pizza_time = 0  # Time when the last pizza spawned
pizza_spawn_rate = 15000  # Minimum 15 seconds (15000 milliseconds) between pizza spawns

# Spawn candy less frequently with a cool-down
last_candy_time = 0  # Time when the last candy spawned
candy_spawn_rate = 20000  # Minimum 20 seconds (20000 milliseconds) between candy spawns
# Mute control variables
muted = False  # Flag to check if audio is muted

# Set initial volume for sound effects (1.0 is full volume, 0.0 is muted)
cheese_sound.set_volume(1.0)  # Set cheese sound volume to 100%
pizza_sound.set_volume(1.0)  # Set pizza sound volume to 100%
candy_sound.set_volume(1.0)  # Set candy sound volume to 100%

def toggle_mute():
    global muted
    if muted:
        # Unmute: Restore sound volume for all sound effects
        cheese_sound.set_volume(1.0)  # Full volume for cheese sound effects
        pizza_sound.set_volume(1.0)  # Full volume for pizza sound effects
        candy_sound.set_volume(1.0)  # Full volume for candy sound effects
        muted = False
    else:
        # Mute: Set all sound volumes to 0 (silent)
        cheese_sound.set_volume(0.0)  # Mute cheese sound effects
        pizza_sound.set_volume(0.0)  # Mute pizza sound effects
        candy_sound.set_volume(0.0)  # Mute candy sound effects
        muted = True

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse click to toggle mute
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the mute button is clicked
            if mute_button.collidepoint(mouse_x, mouse_y):
                toggle_mute()

    # Key press handling for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rat_x -= current_speed
    if keys[pygame.K_RIGHT]:
        rat_x += current_speed
    if keys[pygame.K_UP]:
        rat_y -= current_speed
    if keys[pygame.K_DOWN]:
        rat_y += current_speed

    # Prevent rat from going out of bounds
    rat_x = max(0, min(rat_x, WIDTH - rat_img.get_width()))
    rat_y = max(0, min(rat_y, HEIGHT - rat_img.get_height()))

    # Check if speed boost is still active
    current_time = pygame.time.get_ticks()
    if current_time > boost_end_time:
        # Reset speed to normal after 10 seconds
        current_speed = rat_speed

    # Check for collision with cheeses
    for cheese in cheeses[:]:
        distance = math.sqrt((rat_x - cheese[0])**2 + (rat_y - cheese[1])**2)
        if distance < rat_img.get_width() // 2 + cheese_img.get_width() // 2:
            cheeses.remove(cheese)  # Rat collects cheese
            cheeses.append(create_cheese())  # Create a new cheese
            score += 1  # Increase score
            cheese_sound.play() # Sound effect when cheese is collected
 
    # Check for collision with pizzas
    for pizza in pizzas[:]:
        distance = math.sqrt((rat_x - pizza[0])**2 + (rat_y - pizza[1])**2)
        if distance < rat_img.get_width() // 2 + pizza_img.get_width() // 2:
            pizzas.remove(pizza)  # Rat collects pizza
            score += 10  # Increased points (10) for pizza
            pizza_sound.play()  # Sound effect when pizza is collected

   # Check if enough time has passed since the last pizza spawn
    current_time = pygame.time.get_ticks()  # Get current time in milliseconds
    if current_time - last_pizza_time > pizza_spawn_rate:
        # Spawn a pizza with a 40% chance every pizza_spawn_rate milliseconds
        if random.random() < 0.4:  # 40% chance to spawn a pizza
            pizzas.append(create_pizza())
            last_pizza_time = current_time  # Update the time when the last pizza spawned

    # Check for collision with candies
    for candy in candies[:]:
        distance = math.sqrt((rat_x - candy[0])**2 + (rat_y - candy[1])**2)
        if distance < rat_img.get_width() // 2 + candy_img.get_width() // 2:
            candies.remove(candy)  # Rat collects candy
            score += 20  # Increased points (10) for candy
            candy_sound.play()  # Sound effect when candy is collected

            # Increase rat speed and start the speed boost timer
            current_speed = boosted_speed
            boost_end_time = current_time + speed_boost_duration  # Set the end time of the boost

   # Check if enough time has passed since the last candy spawn
    if current_time - last_candy_time > candy_spawn_rate:
        # Spawn a candy with a 30% chance every candy_spawn_rate milliseconds
        if random.random() < 0.3:  # 30% chance to spawn a candy
            candies.append(create_candy())
            last_candy_time = current_time  # Update the time when the last candy spawned

    # Fill the screen with the custom background image
    screen.blit(background_img, (0, 0))  # Draw the background at the top-left corner
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Draw rat image
    screen.blit(rat_img, (rat_x, rat_y))  # Use rat_x, rat_y directly

    # Draw cheeses using the cheese image
    for cheese in cheeses:
        screen.blit(cheese_img, (cheese[0] - cheese_img.get_width() // 2, cheese[1] - cheese_img.get_height() // 2))  # Center the cheese

    # Draw pizzas using the pizza image
    for pizza in pizzas:
        screen.blit(pizza_img, (pizza[0] - pizza_img.get_width() // 2, pizza[1] - pizza_img.get_height() // 2))  # Center the pizza

    # Draw candies using the candy image
    for candy in candies:
        screen.blit(candy_img, (candy[0] - candy_img.get_width() // 2, candy[1] - candy_img.get_height() // 2))  # Center the candy

    # Display the score
    score_text = font.render(f"Collected: {score}", True, WHITE)

    # Display score centered at top of screen
    score_x = (WIDTH - score_text.get_width()) // 2  # Center horizontally
    screen.blit(score_text, (score_x, 20)) 

    # Draw mute/unmute icon
    mute_icon_width, mute_icon_height = mute_icon.get_width(), mute_icon.get_height()
    mute_button = pygame.Rect(WIDTH - mute_icon_width - 20, 10, mute_icon_width, mute_icon_height)
    
    # Display mute or unmute icon based on the muted state
    if muted:
        screen.blit(mute_icon, (WIDTH - mute_icon_width - 20, 10)) 
    else:
        screen.blit(unmute_icon, (WIDTH - mute_icon_width - 20, 10))  


    # Update display
    pygame.display.flip()

    # Set frame rate (FPS)
    clock.tick(60)