import random

width = 400
height = 400
game_started = False
user_input = ""
awaiting_answer = False

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.w = width / cols
        self.h = height / rows
        self.grid = [[True for _ in range(cols)] for _ in range(rows)]
        self.threat_positions = []

        self.create_path(1, 1)
        self.grid[1][0] = False
        self.grid[rows - 2][cols - 1] = False
        
        self.place_threats()

    def create_path(self, start_x, start_y):
        stack = [(start_x, start_y)]
        self.grid[start_y][start_x] = False

        while stack:
            x, y = stack[-1]
            neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            unvisited_neighbors = []
            
            for nx, ny in neighbors:
                if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx]:
                    unvisited_neighbors.append((nx, ny))
            
            if unvisited_neighbors:
                nx, ny = random.choice(unvisited_neighbors)
                mx, my = (nx + x) // 2, (ny + y) // 2
                self.grid[my][mx] = False
                self.grid[ny][nx] = False
                stack.append((nx, ny))
            else:
                stack.pop()

    def place_threats(self):
        num_threats = (self.cols * self.rows) // 20 
        for _ in range(num_threats):
            while True:
                x = random.randint(0, self.cols - 1)
                y = random.randint(0, self.rows - 1)
                if not self.grid[y][x]:
                    self.threat_positions.append((x, y))
                    break

    def display(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.grid[j][i]:
                    fill(0, 128, 0)  # Green for healthy areas
                else:
                    fill(150, 75, 0)  # Brown for affected areas
                rect(i * self.w, j * self.h, self.w, self.h)

        for (x, y) in self.threat_positions:
            fill(255, 0, 0)  # Red for environmental threats
            rect(x * self.w, y * self.h, self.w, self.h)

        textSize(14)
        fill(255, 255, 255)
        textAlign(CENTER, CENTER)
        text("Start", self.w / 2 + 8, self.h / 2)
        text("End", width - self.w / 2 - 8, height - self.h / 2 - 5)

class Player:
    def __init__(self, maze, eco_image):
        self.maze = maze
        self.x = 1
        self.y = 1
        self.eco_image = eco_image
        self.w = maze.w
        self.h = maze.h
        self.move_count = 0
        self.message_timer = 0
        self.message_duration = 120
        self.display_message = False
        self.message = ""

    def display(self):
        image(self.eco_image, self.x * self.w, self.y * self.h, self.w, self.h)
        if self.display_message:
            self.message_timer += 1
            if self.message_timer > self.message_duration:
                self.display_message = False
                self.message_timer = 0

            textSize(14)
            fill(0)
            textAlign(CENTER)
            text(self.message, width / 2, height / 4)

    def move(self, dx, dy):
        global awaiting_answer
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and not self.maze.grid[new_y][new_x]:
            self.x = new_x
            self.y = new_y
            self.move_count += 1

            if self.move_count % 5 == 0:
                awaiting_answer = True
                questions.ask_question()

    def show_message(self, message):
        self.message = message
        self.display_message = True
        self.message_timer = 0

class Questions:
    def __init__(self):
        self.questions = [
            "What are some ways to reduce carbon emissions?",
            "How can you contribute to recycling efforts?",
            "What are the effects of deforestation on wildlife?",
            "What is the importance of protecting endangered species?",
            "How can renewable energy sources help combat climate change?"
        ]
        self.possible_answers = {
            "What are some ways to reduce carbon emissions?": [
                "Using public transportation",
                "Increasing meat consumption",
                "Throwing away more food",
                "Ignoring energy-saving tips"
            ],
            "How can you contribute to recycling efforts?": [
                "Sorting recyclables properly",
                "Using more single-use plastics",
                "Littering in public places",
                "Avoiding recycling programs"
            ],
            "What are the effects of deforestation on wildlife?": [
                "Loss of habitat",
                "Increase in biodiversity",
                "Better air quality",
                "More space for wildlife"
            ],
            "What is the importance of protecting endangered species?": [
                "Maintaining biodiversity",
                "Overpopulation of species",
                "Decreasing ecological balance",
                "No impact on the environment"
            ],
            "How can renewable energy sources help combat climate change?": [
                "Reducing greenhouse gas emissions",
                "Increasing fossil fuel use",
                "Polluting the air",
                "Encouraging deforestation"
            ]
        }
        self.current_question = None
        self.options = []
        self.correct_option = None
        self.button_height = 40
        self.button_width = width / 2
        self.button_margin = 10
        self.input_box_y = height / 2 + 70

    def ask_question(self):
        question_index = random.randint(0, len(self.questions) - 1)
        question = self.questions[question_index]
        
        correct_answer = random.choice(self.possible_answers[question])
        
        self.current_question = question
        self.generate_options(correct_answer)

    def generate_options(self, correct_answer):
        self.correct_option = random.randint(0, 3)
        self.options = []
        all_answers = self.possible_answers[self.current_question]
        correct_option = correct_answer
        
        # Ensure the correct answer is included and options are unique
        unique_answers = set([correct_option])
        while len(unique_answers) < 4:
            incorrect_answers = [ans for ans in all_answers if ans != correct_option]
            unique_answers.add(random.choice(incorrect_answers))
        
        self.options = list(unique_answers)
        random.shuffle(self.options)  # Shuffle to place the correct answer in a random position

    def display_question(self):
        if self.current_question:
            question_text = self.current_question
            max_text_width = width - 40
            max_text_length = int(max_text_width / 10)
            
            if len(question_text) > max_text_length:
                font_size = int(18 * max_text_length / len(question_text))
            else:
                font_size = 18
            
            textSize(font_size)
            fill(255)
            textAlign(CENTER)
            text(question_text, width / 2, height / 2 - 50)
            
            for i, option in enumerate(self.options):
                y_position = self.input_box_y + (i * (self.button_height + self.button_margin))
                fill(200)
                rect(width / 4, y_position, self.button_width, self.button_height)
                fill(0)
                textAlign(CENTER, CENTER)
                option_text = "Option {}: {}".format(i + 1, option)
                option_font_size = 12
                while textWidth(option_text) > self.button_width - 10 and option_font_size > 8:
                    option_font_size -= 1
                    textSize(option_font_size)
                text(option_text, width / 4 + self.button_width / 2, y_position + self.button_height / 2)

    def check_answer(self, user_input):
        global awaiting_answer
        if self.current_question:
            try:
                user_choice = int(user_input) - 1
                if user_choice == self.correct_option:
                    player.show_message("Correct! You're helping save the planet!")
                    awaiting_answer = False
                    self.current_question = None
                else:
                    player.show_message("Incorrect! Keep trying to make a difference.")
            except:
                player.show_message("Invalid input!")

def setup():
    global maze, player, questions, background_image
    size(width, height)
    cols, rows = 21, 21
    maze = Maze(cols, rows)
    
    eco_image = loadImage("eco.png")
    player = Player(maze, eco_image)
    questions = Questions()

    background_image = loadImage("background.png")  # Load the background image

def draw():
    global game_started
    background(255)
    
    if game_started:
        maze.display()
        player.display()
        if awaiting_answer:
            questions.display_question()
    else:
        intro_screen()

def intro_screen():
    global background_image
    
    if background_image:
        image(background_image, 0, 0, width, height)  # Display the background image
    
    # Title
    title_text_line1 = "EcoQuest: The Climate"
    title_text_line2 = "Challenge"
    
    textSize(36)
    fill(255, 255, 255)  # White color for the title text for contrast
    textAlign(CENTER, CENTER)
    text(title_text_line1, width / 2, height / 2 - 80)
    text(title_text_line2, width / 2, height / 2 - 40)
    
    # Subtitle
    subtitle_text = "Ready to make a difference?"
    textSize(20)
    fill(255, 255, 255)  # White color for subtitle text
    text(subtitle_text, width / 2, height / 2 + 20)
    
    # Button
    button_width = 120
    button_height = 50
    button_x = width / 2 - button_width / 2
    button_y = height / 2 + 80
    
    fill(0, 200, 0)  # Green color for the button
    rect(button_x, button_y, button_width, button_height, 15)  # Rounded corners
    fill(255)
    textSize(22)
    text("Start", width / 2, height / 2 + 105)
    
    # Add a border around the button for better visibility
    noFill()
    stroke(0)
    strokeWeight(2)
    rect(button_x, button_y, button_width, button_height, 15)

def mousePressed():
    global game_started
    global awaiting_answer
    button_width = 120
    button_height = 50
    button_x = width / 2 - button_width / 2
    button_y = height / 2 + 80
    
    if not game_started and button_x <= mouseX <= button_x + button_width and button_y <= mouseY <= button_y + button_height:
        start_game()
    elif game_started and awaiting_answer:
        for i, option in enumerate(questions.options):
            y_position = questions.input_box_y + (i * (questions.button_height + questions.button_margin))
            if width / 4 <= mouseX <= width / 4 + questions.button_width and y_position <= mouseY <= y_position + questions.button_height:
                user_input = str(i + 1)
                questions.check_answer(user_input)

def start_game():
    global game_started
    game_started = True

def keyPressed():
    global user_input
    global awaiting_answer
    if game_started:
        if not awaiting_answer:
            if key == 'w' or key == 'W' or keyCode == UP:
                player.move(0, -1)
            elif key == 's' or key == 'S' or keyCode == DOWN:
                player.move(0, 1)
            elif key == 'a' or key == 'A' or keyCode == LEFT:
                player.move(-1, 0)
            elif key == 'd' or key == 'D' or keyCode == RIGHT:
                player.move(1, 0)
        else:
            if keyCode == ENTER:
                questions.check_answer(user_input)
                user_input = ""
            else:
                user_input += str(key)

def mouseClicked():
    mousePressed()

if __name__ == '__main__':
    import os
