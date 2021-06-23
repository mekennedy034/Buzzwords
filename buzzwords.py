################################################
##BUZZWORDS - my version of the NTY Spelling Bee
################################################

import random, pygame, time


MIN_ANSWER = 20
MIN_SCORE = 50

def main():
    pygame.init() ##gotta do this every time
    status_box = pygame.Rect(0, 260, 275, 25)
    font =  pygame.font.SysFont('arialblack', 18)

    while True:   
        answers, hive, key_letter = gen_puzzle()
        win, screen = play_puzzle(answers, hive, key_letter)
        if win:
            screen.fill(pygame.Color('white'), rect=status_box)
            again = font.render("Play again? (y/n)", True, pygame.Color('black'))
            screen.blit(again, status_box)
            q = get_word(None, None, screen, True)
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
        hive, key_letter = set_hive()
        ##generate answer list and scores
        answer_list, top_score = answer_gen(hive, key_letter)
        total_answers = len(answer_list)
        total_score = top_score

    print(hive, key_letter, top_score, len(answer_list))
    return answer_list, hive, key_letter

##opens the pangram list
##returns a random hive and a key letter
def set_hive():
    pangrams = open("pangrams.txt", "r")
    hive_list = [set(w.strip()) for w in pangrams]
    hive = ''.join(set(random.choice(hive_list)))
    key_letter = random.choice(hive)
    pangrams.close()
    return hive, key_letter

def answer_gen(hive, key_letter):
    bee_dict = open("bee_dict.txt", "r")
    all_words = [w.strip() for w in bee_dict]
    hive_set = set(hive)

    answer_list = [a for a in all_words if set(a).issubset(hive_set) and key_letter in a]        
        
    top_score = 0
    for a in answer_list:
        letters = set(a)
        if len(a) == 4:
            top_score += 1
        else:
            top_score += len(a)
        if len(letters) == 7:
            top_score += 7
            
    return answer_list, top_score

##the code that actually plays the puzzle
def play_puzzle(answers, hive, key_letter):
    ##set up the pygames window
    screen = pygame.display.set_mode((750, 345))
    pygame.display.set_caption("Buzzwords")
    font = pygame.font.SysFont('arialblack', 16)
    message_box = pygame.Rect(5, 315, 275, 25)


    ##blank variables
    score = 0
    found_words = []

    ##gameplay loop: get word, check word, score
    while len(found_words) < len(answers):
        display_hive(hive, key_letter, screen)   
        display_status(len(answers), score, found_words, screen)

        word = get_word(key_letter, hive, screen, False)
        if word in answers and word not in found_words:
            score += score_word(word)
            found_words.append(word)
        elif word in found_words:
            error_display(4, screen)
        elif word not in answers:
            error_display(5, screen)
    
    display_status(len(answers), score, found_words, screen)
    win = font.render("You win!", True, pygame.Color('black'))
    screen.blit(win, (message_box.x+1, message_box.y+1))
    pygame.display.update()
    return True, screen
    
    
##shows the board in a PyGames window
def display_hive(hive, key_letter, screen):
    screen.fill((255,255,255))
    board = pygame.image.load("hive_board.bmp")
    screen.blit(board, (0,0))

    hive_list = [c for c in hive]
    hive_list.remove(key_letter)
    
    font = pygame.font.SysFont('arialblack', 36)
    center_letter = font.render(key_letter, True, (0,0,0))
    cl_rect = center_letter.get_rect()
    cl_rect.center = (145, 130)
    screen.blit(center_letter, cl_rect)
    
    hive_letters = []
    hive_spots = [(146, 48),(146, 210),(75, 88),(75, 168),(215, 88),(215, 168)]
    hive_centers = []
    for i in range(len(hive_list)):
        c = hive_list[i]
        letter = font.render(c, True, (0,0,0))
        letter_box = letter.get_rect()
        letter_box.center=hive_spots[i]
        hive_letters.append(letter)
        hive_centers.append(letter_box)

    hive_dict = zip(hive_letters, hive_centers)

    for item in hive_dict:
        screen.blit(item[0], item[1])

    pygame.display.update()

## blits a status bar with current score and number of words found
## blits a list of found words (for reference)
def display_status(answer_no, score, found_words, screen):

    font2 = pygame.font.SysFont('arialblack', 18)
    s = "Words: " + str(len(found_words))+ "/" + str(answer_no) + "     Score:" + str(score)
    info = font2.render(s, True, pygame.Color('black'))
    info_box = info.get_rect()
    info_box.center = (146, 270)
    screen.blit(info, info_box)

    font3 = pygame.font.SysFont('arial', 16)
    found_words = sorted(found_words)

    widest = 0
    all_found = []
    for i in range(len(found_words)):
        w = found_words[i]
        word = font3.render(w, True, (0,0,0))
        word_box = word.get_rect()
        if word_box.width > widest:
            widest = word_box.width
        all_found.append((word, word_box))

    for i in range(len(all_found)):
        word = all_found[i][0]
        word_box = all_found[i][1]
        word_box.topleft = (300 + ((widest+10)*(i//14)), ((i % 14)*24))
        screen.blit(word, word_box)

    pygame.display.update()

##blits out an error message when the input is wrong
def error_display(error_number, screen):
    font = pygame.font.SysFont('arialblack', 16)
    message_box = pygame.Rect(5, 315, 275, 25)
    error = {1: font.render("Missing center letter", True, pygame.Color('black')),
             2: font.render("Too short", True, pygame.Color('black')),
             3: font.render("Invalid characters", True, pygame.Color('black')),
             4: font.render("Already found", True, pygame.Color('black')),
             5: font.render("Word not in list", True, pygame.Color('black'))
             }

    pygame.draw.rect(screen, pygame.Color('white'), message_box)
    screen.blit(error[error_number], (message_box.x+1, message_box.y+1))

    pygame.display.update()
    pygame.time.wait(750)

##Gets input from player
##validates it
##returns valid input
def get_word(key_letter, hive, screen, win):
    font = pygame.font.SysFont('arialblack', 16)
    clock = pygame.time.Clock()
    text = ""
    input_box = pygame.Rect(5, 290, 275, 25)
    message_box = pygame.Rect(5, 315, 275, 25)
    input_active = True


    while True:    
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        word = text.upper()
                        text = ""
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    else:
                        pygame.draw.rect(screen, pygame.Color('white'), message_box)
                        text += event.unicode
                    

            pygame.draw.rect(screen, pygame.Color('lightgray'), input_box)
            text_surf = font.render(text, True, pygame.Color('black'))
            screen.blit(text_surf, (input_box.x+1, input_box.y+1))
            pygame.display.flip()
            clock.tick(20)
            
        if win:
            return word
        elif set(word).issubset(set(hive)):
            if len(word) >= 4:
                if key_letter in word:
                    return word.upper()
                else:
                    error_display(1, screen)
                    input_active = True
            else:
                error_display(2, screen)
                input_active = True
        else:
            error_display(3, screen)
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
