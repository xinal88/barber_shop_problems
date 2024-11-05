import pygame
import random

total_chairs = 9
max_chairs_per_row = 5

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Screen
WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Sleeping Barber Simulation")

# Font
font = pygame.font.Font(None, 36)

# Text variables
arrival_text = ""
arrival_text_timer = 0
barber_action_text = ""
done_text = ""
done_text_timer = 0
barber_state_text = "Barber is sleeping"

def update_arrival_text(text, duration=1000):
    global arrival_text, arrival_text_timer
    arrival_text = text
    arrival_text_timer = pygame.time.get_ticks() + duration

def update_barber_action_text(text):
    global barber_action_text
    barber_action_text = text

def update_done_text(text, duration=2000):
    global done_text, done_text_timer
    done_text = text
    done_text_timer = pygame.time.get_ticks() + duration

def update_barber_state_text(text):
    global barber_state_text
    barber_state_text = text

class Add_Customer_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text = "Add Customer"
        self.width = 200
        self.height = 50
        self.font = pygame.font.Font(None, 36)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.border_color = RED
        self.border_width = 5
        self.render_text()

    def render_text(self):
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surf, text_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect.inflate(self.border_width, self.border_width))
        surface.blit(self.image, self.rect)

class Chair(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.occupied = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Customer(pygame.sprite.Sprite):
    def __init__(self, ID, position):
        super().__init__()
        self.image = pygame.image.load("customer_before.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.ID = ID
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        text_surf = self.font.render(str(self.ID), True, BLACK)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 40))
        surface.blit(text_surf, text_rect)

class Barber(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_busy = pygame.image.load("barber.png")
        self.image_busy = pygame.transform.scale(self.image_busy, (50, 50))
        self.image_sleeping = pygame.image.load("barber_sleeping.png")
        self.image_sleeping = pygame.transform.scale(self.image_sleeping, (50, 50))
        self.image = self.image_sleeping
        self.rect = self.image.get_rect()
        self.rect.center = (400, 100)
        self.busy = False
        self.sleeping = True
    
    def update_image(self):
        self.image = self.image_sleeping if self.sleeping else self.image_busy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Create an instance of the button
add_customer_button = Add_Customer_Button()

# List to keep track of customers
customers = []

# List of chairs
chairs = []
for i in range(total_chairs):
    x_position = 100 + (i % max_chairs_per_row) * 150
    y_position = 300 + (i // max_chairs_per_row) * 100
    chair = Chair((x_position, y_position))
    chairs.append(chair)

# Create an instance of the barber
barber = Barber()

# Pointers for chair assignments
assign_customer_pointer = 0
next_customer_pointer = 0

# Main game loop
running = True
next_customer_id = 1

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_customer_button.rect.collidepoint(event.pos):
                customer_id = next_customer_id
                next_customer_id += 1
                update_arrival_text(f"Customer {customer_id} has arrived")
                
                # Check if queue is full
                if assign_customer_pointer == next_customer_pointer and chairs[assign_customer_pointer].occupied:
                    update_arrival_text("No available chairs. Customer leaves.", 2000)
                else:
                    # Assign customer to the next available chair
                    chair = chairs[assign_customer_pointer]
                    chair.occupied = True
                    new_customer = Customer(customer_id, chair.rect.center)
                    customers.append(new_customer)
                    update_arrival_text(f"Customer {customer_id} is seated", 2000)
                    assign_customer_pointer = (assign_customer_pointer + 1) % total_chairs
                
                # Start barber's work if they are free and there is a customer in the queue
                if not barber.busy and chairs[next_customer_pointer].occupied:
                    barber.busy = True
                    barber.sleeping = False
                    barber.update_image()
                    current_customer = customers[0]  # Get the next customer
                    current_customer.rect.center = (barber.rect.center[0] + 60, barber.rect.center[1])
                    update_barber_state_text("Barber is busy")
                    update_barber_action_text(f"Barber is cutting hair for customer {current_customer.ID}")
                    pygame.time.set_timer(pygame.USEREVENT + current_customer.ID, random.randint(5000, 10000))
                    chairs[next_customer_pointer].occupied = False  # Mark the chair as free
                    next_customer_pointer = (next_customer_pointer + 1) % total_chairs

        elif event.type >= pygame.USEREVENT:
            customer_id = event.type - pygame.USEREVENT
            for customer in customers:
                if customer.ID == customer_id:
                    update_done_text(f"Customer {customer_id} is done", 2000)
                    customers.remove(customer)
                    barber.busy = False
                    barber_action_text = ""
                    
                    # Check if there are customers waiting in the queue
                    if chairs[next_customer_pointer].occupied:
                        barber.busy = True
                        barber.sleeping = False
                        barber.update_image()
                        next_customer = customers[0]
                        next_customer.rect.center = (barber.rect.center[0] + 60, barber.rect.center[1])
                        update_barber_action_text(f"Barber is cutting hair for customer {next_customer.ID}")
                        pygame.time.set_timer(pygame.USEREVENT + next_customer.ID, random.randint(5000, 10000))
                        chairs[next_customer_pointer].occupied = False
                        next_customer_pointer = (next_customer_pointer + 1) % total_chairs
                    else:
                        barber.sleeping = True
                        barber.update_image()
                        update_barber_state_text("Barber is sleeping")
                    break

    DISPLAYSURF.fill(WHITE)
    add_customer_button.draw(DISPLAYSURF)
    for chair in chairs:
        chair.draw(DISPLAYSURF)
    for customer in customers:
        customer.draw(DISPLAYSURF)
    barber.draw(DISPLAYSURF)

    if current_time < arrival_text_timer:
        arrival_text_surf = font.render(arrival_text, True, BLACK)
        arrival_text_rect = arrival_text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        DISPLAYSURF.blit(arrival_text_surf, arrival_text_rect)

    barber_action_text_surf = font.render(barber_action_text, True, BLACK)
    barber_action_text_rect = barber_action_text_surf.get_rect(center=(barber.rect.centerx, barber.rect.centery + 60))
    DISPLAYSURF.blit(barber_action_text_surf, barber_action_text_rect)

    if current_time < done_text_timer:
        done_text_surf = font.render(done_text, True, BLACK)
        done_text_rect = done_text_surf.get_rect(center=(barber.rect.centerx, barber.rect.centery + 90))
        DISPLAYSURF.blit(done_text_surf, done_text_rect)

    barber_state_text_surf = font.render(barber_state_text, True, BLACK)
    barber_state_text_rect = barber_state_text_surf.get_rect(topleft=(10, 10))
    DISPLAYSURF.blit(barber_state_text_surf, barber_state_text_rect)

    pygame.display.flip()

pygame.quit()
