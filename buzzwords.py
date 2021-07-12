################################################
##BUZZWORDS - my version of the NTY Spelling Bee
################################################

import random, pygame

MIN_ANSWER = 20
MIN_SCORE = 50

class puzzle:
    def __init__(self, string):
        self.string = string
        self.letter_set = set(string)
        self.letter_list =list(set(string))
        self.key_letter = random.choice(string)
        self.answer_list = []
        self.max_score = 0
        self.current_score = 0
        self.found_words = []

    def __str__(self):
        return f"{self.string} {self.key_letter} | Words: {len(self.answer_list)} | High Score: {self.max_score}"

class region:
    def __init__(self, rect, bg_color, font, font_color):
        self.rect = rect
        self.bg_color = bg_color
        self.font = font
        self.font_color = font_color

    def __str__(self):
        return f"{self.rect} of {self.bg_color} with text of {self.font_color}"

class layout:
    pygame.font.init()
    colors = {"black": pygame.Color("black"),
             "white": pygame.Color("white"),
             "gray": pygame.Color("gray"),
             "lgray": pygame.Color("lightgray"),
              "gold": pygame.Color("gold")
             }
    message_box = region(pygame.Rect(5, 315, 275, 25),
                              colors["white"],
                              pygame.font.SysFont('arialblack', 16),
                              colors["black"])
    progress_box = region(pygame.Rect(5, 340, 275, 18),
                                   colors["gold"],
                                   pygame.font.SysFont('arialblack', 12),
                                   colors["black"])
    solve_box = region(pygame.Rect(4,3, 39, 19),
                                colors["lgray"],
                                pygame.font.SysFont('arialblack', 12),
                                colors["black"])
    status_box = region(pygame.Rect(0, 260, 275, 25),
                                 colors["white"],
                                 pygame.font.SysFont('arialblack', 16),
                                 colors["black"])
    answer_box = region(pygame.Rect(300, 0, 675, 360),
                                 colors["white"],
                                 pygame.font.SysFont('arial', 16),
                                 colors["black"])
    input_box = region(pygame.Rect(5, 290, 275, 25),
                                colors["lgray"],
                                pygame.font.SysFont('arialblack', 16),
                                colors["black"])
    outline_box = region(pygame.Rect(1,1, 45, 23),
                                  colors["gray"],
                                  None,
                                  None)
        

    
    def __init__(self):
        self.screen = pygame.display.set_mode((975, 360))
                                                    
    def text_blit(self, string, box):
        pygame.draw.rect(self.screen, box.bg_color, box.rect)
        font_type = box.font
        text = font_type.render(string, True, box.font_color)
        self.screen.blit(text, (box.rect.x+1, box.rect.y+1))

    def box_blit(self, box):
        pygame.draw.rect(self.screen, box.bg_color, box.rect)
                        
    def draw_board(self):
        pygame.display.set_caption("Buzzwords")
        self.screen.fill(self.colors["white"])
        board = pygame.image.load("hive_board.bmp")
        self.screen.blit(board, (0,0))
        pygame.display.update()

    def draw_hive(self, hive):
        center = (145,130)
        font = pygame.font.SysFont('arialblack', 36) 
        center_letter = font.render(hive.key_letter, True, self.colors["black"])
        cl_rect = center_letter.get_rect()
        cl_rect.center = center
        self.screen.blit(center_letter, cl_rect)
        
        hive_letters = hive.letter_list
        if hive.key_letter in hive_letters:
            hive_letters.remove(hive.key_letter)
        hive_spots = [(145, 48),(145, 210),(75, 88),(75, 168),(215, 88),(215, 168)]
        hive_centers = []
        hive_text = []
        for i, c in enumerate(hive_letters):
            letter = font.render(c, True, self.colors["black"])
            letter_box = letter.get_rect()
            letter_box.center=hive_spots[i]
            hive_text.append(letter)
            hive_centers.append(letter_box)
    
        hive_dict = zip(hive_text, hive_centers)
        for item in hive_dict:
            self.screen.blit(item[0], item[1])

        pygame.display.update()

    def shuffle(self, hive):
        random.shuffle(hive.letter_list)
        return hive
    

def main():
    pygame.init() ##gotta do this every time
    pygame.key.set_repeat(750, 200)
    viz = layout()
    while True:   
        hive = gen_puzzle()
        win, viz = play_puzzle(hive, viz)
        if win:
            viz.text_blit("You win!", viz.message_box)
            
        viz.text_blit("Play again? (y/n)", viz.status_box)
        q = get_word(None, viz, True)
        if q == "N":
            break
    pygame.quit()
    sys.exit()
            

##Generates an answer list for a randomly selected hive
def gen_puzzle():
    total_answers = 0
    total_score = 0

    ##while loop validates the puzzle:
    ##start over if there are too few answers or too low score
    while total_answers < MIN_ANSWER or total_score < MIN_SCORE:
        ##choose a pangram and a central letter
        hive = set_hive()
        ##generate answer list and scores
        hive = answer_gen(hive)
        total_answers = len(hive.answer_list)
        total_score = hive.max_score

    print(hive)
    return hive

##opens the pangram list
##returns a random hive and a key letter
def set_hive():
    with open("pangrams.txt", "r") as pangrams:
        hive_list = [set(w.strip()) for w in pangrams]
        hive = puzzle(''.join(set(random.choice(hive_list))))
    return hive

def answer_gen(hive):
    with open("bee_dict.txt", "r") as bee_dict:
        all_words = [w.strip() for w in bee_dict]

        hive.answer_list = [a for a in all_words if set(a).issubset(hive.letter_set) and hive.key_letter in a]        
        
        for a in hive.answer_list:
            hive.max_score += score_word(a)
    return hive

##the code that actually plays the puzzle
def play_puzzle(hive, viz):
    ##blank variables
    cont = True
    redraw(hive, viz)
    ##gameplay loop: get word, check word, score
    while len(hive.found_words) < len(hive.answer_list):

        word = get_word(hive, viz, False)
        if word == "*solve":
            display_solve(hive, viz, True)
            return False, viz
        elif word in hive.answer_list and word not in hive.found_words:
            hive.current_score += score_word(word)
            hive.found_words.append(word)
        

        redraw(hive, viz)
    
        if hive.current_score >= int(hive.max_score * 0.7) and cont:
            display_progress(hive, viz)
            viz.text_blit("Genius! Continue? (y/n)", viz.message_box)
            pygame.display.update()
            q = get_word(None, viz, True)
            if q == "N":
                return True, viz
            else:
                cont = False

        pygame.display.update()
    return True, viz

def redraw(hive, viz):
    display_board(hive, viz)   
    display_status(hive, viz), 
    display_progress(hive, viz)
    pygame.display.update()
    
##shows the board in a PyGames window
def display_board(hive, viz):
    viz.draw_board()
    viz.draw_hive(hive)
    ##add the solve button
    viz.text_blit("Solve", viz.solve_box)
    pygame.display.update()
    
## blits a status bar with current score and number of words found
## blits a list of found words (for reference)
def display_status(hive, viz):

    s = f"""Words: {str(len(hive.found_words))}/{str(len(hive.answer_list))}   Score: {str(hive.current_score)}/{str(hive.max_score)}"""
    viz.text_blit(s, viz.status_box)

    display_solve(hive, viz, False)
    
    pygame.display.update()

##blits out an error message when the input is wrong
def error_display(error_number, viz):
    error = {1: "Missing center letter",
             2: "Too short",
             3: "Invalid characters",
             4: "Already found",
             5: "Word not in list"
             }

    viz.text_blit(error[error_number], viz.message_box)

    pygame.display.update()
    pygame.time.wait(600)

##calculates a % of the max score
##displays a progress bar, %, and rank
def display_progress(hive, viz):
    progress = round(hive.current_score/hive.max_score, 4)
    box_width = 275
    viz.progress_box.rect.width = int(progress * box_width)

    rank_points = {.0000: "Beginner",
                   .0200: "Good Start",
                   .0500: "Moving Up",
                   .0800: "Good",
                   .1500: "Solid",
                   .2500: "Nice",
                   .4000: "Great",
                   .5000: "Amazing",
                   .7000: "Genius",
                   1.0000: "Queen Bee"}

    for r in rank_points:
        if progress >= r:
            rank = rank_points[r]

    viz.text_blit(str(round(progress*100, 2))+"% " + rank, viz.progress_box)
    pygame.display.update()

##draws a list of answers in the answer_box to the right of the board
##show_all is a bool; is this printing the full solve or just words so far?
def display_solve(hive, viz, show_all):
    ##do we display unfound answers or nah?
    if show_all: #yeah
        answers = sorted(hive.answer_list)
    else: #nah
        answers = sorted(hive.found_words)

    ##loop over answers object
    ##set color of text
    ##figure out the widest item
    ##keep a list of tuples of the rendered word and its box
    widest = 0
    all_word = []
    for i, w in enumerate(answers):
        if w in hive.found_words:
            color = viz.colors["black"]
        else:
            color = viz.colors["gray"]
        word = viz.answer_box.font.render(w, True, color)
        word_rect = word.get_rect()
        if word_rect.width > widest:
            widest = word_rect.width
        word_box = region(word_rect, "white", viz.answer_box.font, color)
        all_word.append((w, word_box))

    viz.box_blit(viz.answer_box)
    ##loop over the list of tuples
    ##calculate where in answer_box to blit the word
    for i, w in enumerate(all_word):
        word = w[0]
        word_box = w[1]
        word_box.rect.topleft = (viz.answer_box.rect.x + ((widest+10)*(i//16)), ##can only get 16 words per column
                            viz.answer_box.rect.y + ((i % 16)*22)) ##I know answer_box.y=0 but this reads nicely
        viz.text_blit(word, word_box)
    pygame.display.update()

##Gets input from player
##validates it
##returns valid input
def get_word(hive, viz, win):
    clock = pygame.time.Clock()
    text = ""
    input_active = True

    while True:    
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if viz.solve_box.rect.collidepoint(mouse):
                        return "*solve"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        word = text.upper()
                        text = ""
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    elif event.key == pygame.K_SPACE:
                            hive = viz.shuffle(hive)
                            redraw(hive, viz)
                    else:
                        viz.box_blit(viz.message_box)
                        text += event.unicode
                    

            viz.text_blit(text, viz.input_box)
            clock.tick(24)
            pygame.display.update()    
        if win:
            return word
        elif set(word).issubset(hive.letter_set):
            if len(word) >= 4:
                if hive.key_letter in word:
                    if word not in hive.found_words:
                        if word in hive.answer_list:
                            if len(set(word)) == 7:
                                viz.text_blit("Pangram!", viz.message_box)
                            return word.upper()
                        else:
                            error_display(5, viz)
                            input_active = True
                    else:
                        error_display(4, viz)
                        input_active = True
                else:
                    error_display(1, viz)
                    input_active = True
            else:
                error_display(2, viz)
                input_active = True
        else:
            error_display(3, viz)
            input_active = True

##takes in a valid word
##returns the score for that word
def score_word(word):
    if len(word) == 4:
        score = 1
    else:
        score = len(word)
        
    letters = set(word)
    if len(letters) == 7:
        score += 7

    return score

if __name__ == '__main__':
    main()
