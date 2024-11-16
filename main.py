import inOutData
import pandas as pd
import pygame, sys

stopWords = inOutData.inputStopWords("vietnamese-stopwords.txt")
database = inOutData.readData()

# print(stopWords)

for document in database.documents:
    document.processData(stopWords)
    
database.calculateTFIDF()

print("TF-IDF DataFrame:") 
print(database.df)

# print(database.searchWord("ba"))

pygame.init() # Set up display 
WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Search Bar Example") 

# Set up font 
font_path = "font/OpenSans-VariableFont_wdth,wght.ttf"
FONT = pygame.font.Font(font_path, 20) 

# Define colors 
LIGHT_SKIN = (255, 228, 196)
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
GRAY = (200, 200, 200) 

# Set up input box
input_box = pygame.Rect(220, 100, 140, 32) 
color_inactive = GRAY 
color_active = BLACK 
color = color_inactive 
active = False 
text = '' 
search_results = []

#Check box
checkbox_word_rect = pygame.Rect(500, 80, 20, 20)
checkbox_word_color = BLACK 
checkbox_word_checked = True

checkbox_phrase_rect = pygame.Rect(500, 130, 20, 20)
checkbox_phrase_color = BLACK 
checkbox_phrase_checked = False

# Main loop 
running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            # If the user clicked on the input box, toggle active state 
            if input_box.collidepoint(event.pos): 
                active = not active 
                
            elif checkbox_word_rect.collidepoint(event.pos):
                checkbox_word_checked = not checkbox_word_checked
                checkbox_phrase_checked = False
                
            elif checkbox_phrase_rect.collidepoint(event.pos):
                checkbox_phrase_checked = not checkbox_phrase_checked
                checkbox_word_checked = False
                
            else:
                active = False 
            
            # Change the current color of the input box 
            color = color_active if active else color_inactive 
            
        if event.type == pygame.KEYDOWN: 
            if active: 
                if event.key == pygame.K_RETURN:
                    print("Search:", text) 
                    if (checkbox_word_checked):
                        search_results = database.searchWord(text)
                    elif (checkbox_phrase_checked):
                        search_results = database.searchPhrase(text)
                    else: search_results = []
                    
                    text = '' 
                elif event.key == pygame.K_BACKSPACE: 
                    text = text[:-1] 
                else: 
                    text += event.unicode
    # Draw everything 
    screen.fill(LIGHT_SKIN) 
    # Render the current text. 
    txt_surface = FONT.render(text, True, color) 
    # Resize the box if the text is too long. 
    width = max(200, txt_surface.get_width() + 10) 
    input_box.w = width 
    # Blit the text. 
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5)) 
    # Blit the input box rect. 
    pygame.draw.rect(screen, color, input_box, 2) 
    
    pygame.draw.rect(screen, BLACK, checkbox_word_rect, 2) 
    if checkbox_word_checked: 
        pygame.draw.rect(screen, BLACK, checkbox_word_rect.inflate(-4, -4))
    
    pygame.draw.rect(screen, BLACK, checkbox_phrase_rect, 2) 
    if checkbox_phrase_checked: 
        pygame.draw.rect(screen, BLACK, checkbox_phrase_rect.inflate(-4, -4))
        
    title = "Searching..."
    title_checkbox1 = "Word"
    title_checkbox2 = "Phrase"
    
    title_surface = FONT.render(title, True, BLACK)
    screen.blit(title_surface, (250, 70))
    
    title_checkbox1_surface = FONT.render(title_checkbox1, True, BLACK)
    screen.blit(title_checkbox1_surface, (550, 75))
    
    title_checkbox2_surface = FONT.render(title_checkbox2, True, BLACK)
    screen.blit(title_checkbox2_surface, (550, 125))
    
    # Draw search results table 
    for i, result in enumerate(search_results): 
        result_surface = FONT.render(result, True, BLACK) 
        screen.blit(result_surface, (50, 200 + i * 40))
    
    pygame.display.flip() 
pygame.quit() 
sys.exit()

    