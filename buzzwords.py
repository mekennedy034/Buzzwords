################################################
##BUZZWORDS - my version of the NTY Spelling Bee
################################################

import random, pygame, time


MIN_ANSWER = 20
MIN_SCORE = 50

def main():
    pygame.init() ##gotta do this every time
    status_box = pygame.Rect(0, 260, 275, 25)
    message_box = pygame.Rect(5, 315, 275, 25)

    font =  pygame.font.SysFont('arialblack', 18)
    font2 = pygame.font.SysFont('arialblack', 16)

    while True:   
        answers, hive, key_letter, top_score = gen_puzzle()
        win, screen = play_puzzle(answers, hive, key_letter, top_score)
        if win:
            congrat = font2.render("You win!", True, pygame.Color('black'))
            screen.blit(congrat, (message_box.x+1, message_box.y+1))
            
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
    return answer_list, hive, key_letter, top_score

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
def play_puzzle(answers, hive, key_letter, max_score):
    ##set up the pygames window
    screen = pygame.display.set_mode((975, 360))
    pygame.display.set_caption("Buzzwords")
    font = pygame.font.SysFont('arialblack', 16)
    message_box = pygame.Rect(5, 315, 275, 25)
    progress_box = pygame.Rect(5, 345, 274, 8)
    solve_box = pygame.Rect(3,3, 39, 19)


    ##blank variables
    score = 0
    found_words = []
    cont = True

    ##gameplay loop: get word, check word, score
    display_hive(hive, key_letter, screen)   
    display_status(len(answers), score, max_score, found_words, screen)
    display_progress(score, screen, max_score)
    while len(found_words) < len(answers):

        word = get_word(key_letter, hive, screen, False)
        if word == "*solve":
            display_solve(answers, found_words, screen)
            return False, screen
        elif word in answers and word not in found_words:
            score += score_word(word)
            found_words.append(word)
        elif word in found_words:
            error_display(4, screen)
        elif word not in answers:
            error_display(5, screen)

        display_hive(hive, key_letter, screen)   
        display_status(len(answers), score, max_score, found_words, screen)
        display_progress(score, screen, max_score)

        if score >= max_score * 0.7 and cont:
            display_progress(score, screen, max_score)
            genius = font.render("Genius! Continue? (y/n)", True, pygame.Color('black'))
            pygame.draw.rect(screen, pygame.Color("white"), message_box)
            screen.blit(genius, (message_box.x+1, message_box.y+1))
            q = get_word(None, None, screen, True)
            if q == "N":
                return True, screen
            else:
                cont = False

    pygame.display.update()
    return True, screen
    
    
##shows the board in a PyGames window
def display_hive(hive, key_letter, screen):
    screen.fill((255,255,255))
    board = pygame.image.load("hive_board.bmp")
    screen.blit(board, (0,0))
    ##add the solve button
    outline_box = pygame.Rect(1,1, 45, 23)
    solve_box = pygame.Rect(4,3, 39, 19)
    font_b = pygame.font.SysFont('arialblack', 12)
    solve_it = font_b.render("Solve", True, pygame.Color('black'))
    pygame.draw.rect(screen, pygame.Color('gray'), outline_box)
    pygame.draw.rect(screen, pygame.Color('lightgray'), solve_box)
    screen.blit(solve_it, (solve_box.x+1, solve_box.y))

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
def display_status(answer_no, score, max_score, found_words, screen):

    font2 = pygame.font.SysFont('arialblack', 16)
    s = "Words: " + str(len(found_words))+ "/" + str(answer_no) + "   Score: " + str(score) + "/" + str(max_score)
    info = font2.render(s, True, pygame.Color('black'))
    info_box = info.get_rect()
    info_box.center = (137, 270)
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
        word_box.topleft = (300 + ((widest+10)*(i//16)), ((i % 16)*22))
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
    pygame.time.wait(600)

def display_progress(score, screen, max_score):
    progress = round(score/max_score, 4)
    progress_box = pygame.Rect(5, 340, 274, 17)
    progress_bar = pygame.Rect(5, 340, 274, 17)
    progress_bar.width = int(progress * progress_box.width)
    pygame.draw.rect(screen, pygame.Color('gold'), progress_bar)

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
    
    font = pygame.font.SysFont('arialblack', 12)
    progress = font.render(str(round(progress*100, 2))+"% " + rank, True, pygame.Color('black'))
    screen.blit(progress, (progress_box.x+1, progress_box.y+1))
    pygame.display.update()

def display_solve(answers, found, screen):
    answer_box = pygame.Rect(300, 0, 675, 360)
    font2 = pygame.font.SysFont('arial', 16)
   
    screen.fill(pygame.Color('white'), answer_box)
    answers = sorted(answers)
    widest = 0
    all_word = []
    for i in range(len(answers)):
        w = answers[i]
        if w in found:
            color = pygame.Color('black')
        else:
            color = pygame.Color('gray')
        word = font2.render(w, True, color)
        word_box = word.get_rect()
        if word_box.width > widest:
            widest = word_box.width
        all_word.append((word, word_box))

    for i in range(len(all_word)):
        word = all_word[i][0]
        word_box = all_word[i][1]
        word_box.topleft = (300 + ((widest+10)*(i//14)), ((i % 14)*24))
        screen.blit(word, word_box)
    pygame.display.update()

##Gets input from player
##validates it
##returns valid input
def get_word(key_letter, hive, screen, win):
    font = pygame.font.SysFont('arialblack', 16)
    clock = pygame.time.Clock()
    text = ""
    input_box = pygame.Rect(5, 290, 275, 25)
    message_box = pygame.Rect(5, 315, 275, 25)
    solve_box = pygame.Rect(3,3, 39, 19)

    input_active = True

    while True:    
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if solve_box.collidepoint(mouse):
                        return "*solve"
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
                    if len(set(word)) == 7:
                        pan = font.render("Pangram!", True, pygame.Color('black'))
                        screen.blit(pan, message_box)
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
