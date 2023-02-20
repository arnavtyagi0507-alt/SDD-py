#importing all modules and libraries required for this program 
from ast import Delete, main
from cgitb import text
from http.client import LOCKED
import threading
import time
from tkinter import *
from tkinter import messagebox
from tokenize import String
from turtle import back, color, home
from PIL import ImageTk, Image
from tkinter.font import BOLD, Font
from tkinter import ttk


#creating a root window and defining the geometry and title for the windows
root = Tk()
root.title('Basketball Score Tracker')
width = root.winfo_screenwidth() - 50
height = root.winfo_screenheight()- 50
root.geometry("%dx%d" % (width, height))
root.geometry("1920x1080")
#root.resizable(False,False)
root.state('zoomed')

#creating all the variables that are used in the program
text_box_font=Font(family='Calibiri', size=14)

varcurrentquarter = StringVar()
varminute = StringVar()
varsecond = StringVar()
vartimeperquarter = StringVar()
vartimeperquarter.set('15:00')
vartotalnumberofquarters = StringVar()
vartotalnumberofquarters.set('2')
varhomescore = StringVar()
varhomescore.set('0')
varawayscore = StringVar()
varawayscore.set('0')
varteam1name = StringVar()
varteam1sub = StringVar()
varteam1player = StringVar()
varteam2player = StringVar()
varteam2sub = StringVar()
varteam2name = StringVar()
vartimereamaining = StringVar()
winningteamname = StringVar()

#creating arrays to store team player list, and sub list for home team
team1_player_list = []
team2_player_list = []
team1_sub_list = []
team2_sub_list = []

#creating a dictionary to store team1 player scores and fouls, as well as team2 player scores and fouls
team1_players_scores = dict()
team2_players_scores = dict()
team1_players_fouls = dict()
team2_players_fouls = dict()

#creating a timer using the threading method 
timerThread = threading.Thread()

#defining the command when start button is click
def switch_frame_setup():
   home_screen_frame.pack_forget()
   match_setup_frame.pack(fill='both', expand=True)

#defining the command when player is added in team1
def add_player_team1():
   if(varteam1player.get()==''):
      messagebox.showerror(title="Error", message="Please enter player name to add")
      return
   if(len(team1_player_list)==5):
      messagebox.showerror(title="Error", message="Maximum 5 players allowed.")
      return
   team1_player_list.append(varteam1player.get())
   team1_playinglistbox.insert(END,varteam1player.get())
   varteam1player.set('')

#defining the command when player is added in team2
def add_player_team2():
   if(varteam2player.get()==''):
      messagebox.showerror(title="Error", message="Please enter player name to add")
      return
   if(len(team2_player_list)==5):
      messagebox.showerror(title="Error", message="Maximum 5 players allowed.")
      return
   team2_player_list.append(varteam2player.get())
   team2_playinglistbox.insert(END, varteam2player.get())
   varteam2player.set('')
 
#defining the command when a substitute player is added in team 1
def add_sub_team1():
   if(varteam1sub.get()==''):
      messagebox.showerror(title="Error", message="Please enter substitute name to add")
      return
   if(len(team1_sub_list)==5):
      messagebox.showerror(title="Error", message="Maximum 5 substitutes allowed.")
      return
   team1_sub_list.append(varteam1sub.get())
   team1_substitutebox.insert(END, varteam1sub.get())
   varteam1sub.set('')

#defining the command when a substitute player is added in team 2
def add_sub_team2():
   if(varteam2sub.get()==''):
      messagebox.showerror(title="Error", message="Please enter substitute name to add")
      return
   if(len(team2_sub_list)==5):
      messagebox.showerror(title="Error", message="Maximum 5 substitutes allowed.")
      return
   team2_sub_list.append(varteam2sub.get())
   team2_substitutebox.insert(END, varteam2sub.get())
   varteam2sub.set('')

#defining the command on what happens when the main_screen_switch command is triggered
def main_screen_switch():
   #validate data on team setup screen
   if(varteam1name.get()==''):
      messagebox.showerror(title="Error", message="Home team name is required")
      return
   if(varteam2name.get()==''):
      messagebox.showerror(title="Error", message="Away team name is required")
      return
   if(len(team1_player_list)<5):
      messagebox.showerror(title="Error", message="Minimum 5 players required for Home team")
      return
   if(len(team2_player_list)<5):
      messagebox.showerror(title="Error", message="Minimum 5 players required for Away team")
      return
   if(len(team1_sub_list)<1):
      messagebox.showerror(title="Error", message="Minimum 1 substitute player required for Home team")
      return
   if(len(team2_sub_list)<1):
      messagebox.showerror(title="Error", message="Minimum 1 substitute player required for Away team")
      return
   if(vartotalnumberofquarters.get()==''):
      messagebox.showerror(title="Error", message="No of Quarters is required")
      return
   if(vartimeperquarter.get()==''):
      messagebox.showerror(title="Error", message="Quarter Time is required")
      return
   #match_setup_frame.pack_forget()
     
   #getting the home player names using listbox and putting them on the screen
   listbox_current_players_main_screen_home.insert(END, *team1_player_list)
   listbox_substitutes_players_main_screen_home.insert(END, *team1_sub_list)
   listbox_current_players_main_screen_away.insert(END, *team2_player_list)
   listbox_substitutes_players_main_screen_away.insert(END, *team2_sub_list)
   #disabling the children widgets in the main_screen_switch when the frame is first opened, and the widgets are enabled when the timer starts 
   for child in main_screen_frame.winfo_children():
      child.configure(state='disable')
   background_main_screen.configure(state='normal')
   vartimereamaining.set("00:00")

   match_setup_frame.pack_forget()
   main_screen_root_frame.pack(fill='both', expand=1)

#defining the switch_quarter function which is linked with the next quarter button
def switch_quarter():
   next_quarter_button.place(relx=-1, rely=-1)
   if(int(varcurrentquarter.get()) == int(vartotalnumberofquarters.get())):
      messagebox.showerror(message="Error , this is last quarter", title="Error")
      next_quarter_button.place_forget()
      return
   varcurrentquarter.set(int(varcurrentquarter.get())+1)
   for child in main_screen_frame.winfo_children():
      child.configure(state='normal')
   vartimereamaining.set(vartimeperquarter.get())
   timerThread = threading.Thread( target= timer_countdown)
   timerThread.setDaemon(True)
   timerThread.start()
 
#defining the update_score_home_team function, which updates home team score with the parameter 'score' coming from the button that is function is attached with
def update_score_home_team(score):
   if(listbox_current_players_main_screen_home.curselection()==()):
        messagebox.showerror(title="Error",message="Please select player")
        return
   varhomescore.set(int(varhomescore.get()) + score)
   pindex = listbox_current_players_main_screen_home.curselection()[0]
   player = listbox_current_players_main_screen_home.get(pindex)
   scorevalue = ''
   if(score==1):
      scorevalue = 'Penalty (1 point)' 
   else:
      scorevalue = str(score) + ' points'
   
   if(player not in team1_players_scores.keys()):
      team1_players_scores[player] = score
   else:
      team1_players_scores[player] = team1_players_scores[player] + score
   
   home_scoring_text.insert(END, f'Player: {player} scored - {scorevalue} \n')

#defining the update_score_away_team function, which updates home team score with the parameter 'score' coming from the button that is function is attached with
def update_score_away_team(score):
   if(listbox_current_players_main_screen_away.curselection()==()):
        messagebox.showerror(title="Error",message="Please select player")
        return
   varawayscore.set(int(varawayscore.get())+score)
   pindex = listbox_current_players_main_screen_away.curselection()[0]
   player = listbox_current_players_main_screen_away.get(pindex)
   scorevalue = ''
   if(score==1):
      scorevalue = 'Penalty (1 point)' 
   else:
      scorevalue = str(score) + ' points'
   
   if(player not in team2_players_scores.keys()):
      team2_players_scores[player] = score
   else:
      team2_players_scores[player] = team2_players_scores[player] + score

   away_scoring_text.insert(END, f'Player: {player} scored - {scorevalue} \n')

#defining the update fouls for home team 
def update_fouls_home_team():
   if(listbox_current_players_main_screen_home.curselection()==()):
      messagebox.showerror(title="Error",message="Please select player")
      return
   pindex = listbox_current_players_main_screen_home.curselection()[0]
   player = listbox_current_players_main_screen_home.get(pindex)

   if(player not in team1_players_fouls.keys()):
      team1_players_fouls[player] = 1
   else:
      team1_players_fouls[player]  = team1_players_fouls[player] + 1
   home_scoring_text.insert(END, f'Player: {player} awared - 1 foul \n')
   if(team1_players_fouls[player] >= 5):
      messagebox.showinfo(title="Substitute",message="Player has 5 or more fouls, please substitute")
   
#defining update fouls for away team
def update_fouls_away_team():
   if(listbox_current_players_main_screen_away.curselection()==()):
      messagebox.showerror(title="Error",message="Please select player")
      return
   pindex = listbox_current_players_main_screen_away.curselection()[0]
   player = listbox_current_players_main_screen_away.get(pindex)

   if(player not in team2_players_fouls.keys()):
      team2_players_fouls[player] = 1
   else:
      team2_players_fouls[player]  = team2_players_fouls[player] + 1
   away_scoring_text.insert(END, f'Player: {player} awared - 1 foul \n')
   if(team2_players_fouls[player] >= 5):
      messagebox.showinfo(title="Substitute",message="Player has 5 or more fouls, please substitute")
   
#defining the finish current quarter function
def finish_current_quarter():
   for child in main_screen_frame.winfo_children():
      child.configure(state='disable')
   background_main_screen.configure(state='normal')
   #vartimereamaining.set(vartimeperquarter.get())
   next_quarter_button.place(relx=0.67, rely = 0.4)

#defining the final screen switch function which switches frames from main_screen_frame to final frame
def final_screen_switch():
   main_screen_root_frame.pack_forget()
   quarter_frame.place_forget()
   result_frame.pack(fill='both', expand=1)

   hscore = int(varhomescore.get())
   ascore = int(varawayscore.get())
  
   if(hscore > ascore):
      winningteamname.set(f'Winner : {varteam1name.get()}')
      winning_team_name.configure(background='#0C97EF')
   elif(hscore < ascore):
      winningteamname.set(f'Winner : {varteam2name.get()}')
      winning_team_name.configure(background='#EF340C')
   else:
      winningteamname.set("Match Drawn")
      winning_team_name.configure(background='#2e35b3')
      

   for key in team1_players_scores:
      scores_team1_result.insert(END, f'{key} : {team1_players_scores[key]}\n')

   for key in team2_players_scores:
      scores_team2_result.insert(END, f'{key} : {team2_players_scores[key]}\n')
   
   for key in team1_players_fouls:
      fouls_team1_result.insert(END, f'{key} : {team1_players_fouls[key]}\n')
   
   for key in team2_players_fouls:
      fouls_team2_result.insert(END, f'{key} : {team2_players_fouls[key]}\n')

#defining the finish game function
def finish_game():
   next_quarter_button.place(relx=-1, rely=-1)
   for child in main_screen_frame.winfo_children():
      child.configure(state='disable')
   background_main_screen.configure(state='normal')
   finish_button = Button(quarter_frame, text = 'Finish Game', font = text_box_font, command=final_screen_switch)
   finish_button.place(relheight=0.3, relwidth=0.15, relx=0.7, rely = 0.4)

#defining the timer countdown function for timer to countdown 
def timer_countdown(): 
   vartimer = vartimereamaining.get().split(":");
   mins = vartimer[0]
   sec = vartimer[1]
   times = int(mins)*60 + int(sec)
 
   while times > -1:
      minute,second = (times // 60 , times % 60) 
      #Update the time
      #root.update()
      vartimereamaining.set('{:02d}:{:02d}'.format(minute, second))
      time.sleep(1)
      if(times == 0):
         second = 0
         minute =0
         if(int(varcurrentquarter.get()) < int(vartotalnumberofquarters.get())):
            finish_current_quarter()
         else:
            finish_game()
      times -= 1

#defining the substitution for heam function, which swaps home team players from substitute list box to playing list box and vice versa
def substitution_home_team():
   if(listbox_current_players_main_screen_home.curselection() is ()):
      messagebox.showerror(title="error", message="Please select a player to substitute")
      return
   if(listbox_substitutes_players_main_screen_home.curselection() is ()):
      messagebox.showerror(title="error", message="please select a substitute")
      return
   pindex = listbox_current_players_main_screen_home.curselection()[0]
   sindex = listbox_substitutes_players_main_screen_home.curselection()[0]
   subplayer = listbox_substitutes_players_main_screen_home.get(sindex)
   player = listbox_current_players_main_screen_home.get(pindex)

   listbox_current_players_main_screen_home.delete(pindex)
   listbox_substitutes_players_main_screen_home.delete(sindex)
   listbox_current_players_main_screen_home.insert(END, subplayer)
   listbox_substitutes_players_main_screen_home.insert(END, player)
   # message to substitute
   home_scoring_text.insert(END, f'Player :{player} - substituted by: {subplayer}\n')

#defining the substitution for away team function which swaps away team players from substitute list box to playing list box and vice versa.
def substitution_away_team():
   if(listbox_current_players_main_screen_away.curselection() is ()):
      messagebox.showerror(title="error", message="Please select a player to substitute")
      return
   if(listbox_substitutes_players_main_screen_away.curselection() is ()):
      messagebox.showerror(title="error", message="please select a substitute")
      return
   pindex = listbox_current_players_main_screen_away.curselection()[0]
   sindex = listbox_substitutes_players_main_screen_away.curselection()[0]
   subplayer = listbox_substitutes_players_main_screen_away.get(sindex)
   player = listbox_current_players_main_screen_away.get(pindex)

   listbox_current_players_main_screen_away.delete(pindex)
   listbox_substitutes_players_main_screen_away.delete(sindex)
   listbox_current_players_main_screen_away.insert(END, subplayer)
   listbox_substitutes_players_main_screen_away.insert(END, player)
   # message to substitute
   away_scoring_text.insert(END, f'Player :{player} - substituted by: {subplayer}\n')

#creating the first screen 
home_screen_frame = Frame(root)
home_screen_frame.columnconfigure(0, weight=1)
home_screen_frame.rowconfigure(0, weight=2)
home_screen_frame.rowconfigure(1, weight=6)
home_screen_frame.rowconfigure(2, weight=2)
home_screen_frame.pack(fill='both', expand=True)

#background 
img = ImageTk.PhotoImage(file="images/BasketballVector.png")
home_screen_background = Label(home_screen_frame, image=img)
home_screen_background.place(x=0, y=0, relwidth=1, relheight=1)

#title
title_label = Label(home_screen_frame, text = 'BASKETBALL SCORE TRACKER', font = Font(size = 50, weight = 'bold'))
title_label.grid(row=0, column=0)

#defining the command when start button is click
def switch_frame_setup():
   home_screen_frame.pack_forget()
   match_setup_frame.pack(fill='both', expand=True)

#start button in home screen frame without command
start_button = Button(home_screen_frame, text = "Start", font=Font(family='Calibiri', size=40, weight='bold'), height=int((home_screen_frame.winfo_screenheight()/350)), width=int((home_screen_frame.winfo_screenwidth()/60)),activebackground="#FF6A03",  borderwidth=1, highlightthickness=10, command = switch_frame_setup)
start_button.config(background="#FF6A03")
start_button.grid(row=1, column=0, sticky="S")

#exit button without command
exit_button = Button(home_screen_frame, text="Exit", font=Font(family='Calibiri', size=35, weight='bold'), bg="#ffffff",height=int((home_screen_frame.winfo_screenheight()/500)), width=int((home_screen_frame.winfo_screenwidth()/90)),activebackground="#ffffff",  borderwidth=1, highlightthickness=10, command  = root.quit)
exit_button.grid(row=2, column=0)

#creating a match setup frame 
match_setup_frame = Frame(root)

#background for match setup
match_setup_img = ImageTk.PhotoImage(file = 'images/how-to-buy-a-basketball-2.png')
match_setup_background = Label(match_setup_frame, image = match_setup_img)
match_setup_background.place(x=0,y=0, relwidth=1, relheight=1)

#creating a white banner 
white_banner = Label(match_setup_frame, borderwidth=0, bg="#FF6800", text = 'Match Setup', font=Font(family = 'Calibiri', size=100, weight = 'bold'))
white_banner.place(rely=0.025, relwidth=1, relheight=0.18)

#creating team 1 entry boxes 
team1_name = Entry(match_setup_frame, textvariable=varteam1name, font = text_box_font)
team1_name_label = Label(match_setup_frame, text = 'Enter Home Team',font = text_box_font, bg = '#0C97EF')
team1_name_label.place(relheight = 0.05, relwidth = 0.15, relx = 0.1, rely = 0.23)
team1_name.place(relheight=0.05,relwidth=0.15, relx=0.27, rely = 0.23)

total_number_of_quarters_dropdown_label = Label(match_setup_frame, text = 'Total No.of Quarters',font = text_box_font, bg = '#0C97EF')
total_number_of_quarters_dropdown_label.place(relheight=0.05, relwidth=0.15, relx = 0.1, rely = 0.35)
total_number_of_quarters_dropdown = ttk.Combobox(match_setup_frame, textvariable = vartotalnumberofquarters,font = text_box_font)
total_number_of_quarters_dropdown['value'] = ["1", "2","3","4"]
total_number_of_quarters_dropdown['state'] = 'readonly'
total_number_of_quarters_dropdown.place(relx=0.27, rely=0.35, relwidth=0.15, relheight=0.05)

time_per_quarter_label = Label(match_setup_frame, text = "Time per quarter (min): ", bg ='#EF340C', font=text_box_font )
time_per_quarter_label.place(relheight=0.05, relwidth=0.15,relx = 0.53, rely = 0.35)
time_per_quarter = ttk.Combobox(match_setup_frame, textvariable=vartimeperquarter, font = text_box_font)
time_per_quarter['value'] = ['5:00','10:00','15:00','20:00','25:00']
time_per_quarter['state'] = 'readonly'
time_per_quarter.place(relheight=0.05, relwidth=0.15, relx = 0.69, rely =0.35)


#team 1 entry box player list
team1_player_entry_box = Entry(match_setup_frame,textvariable = varteam1player, font = text_box_font)
team1_player_entry_box.place(relx=0.27, rely = 0.45, relwidth=0.15)
team1_player_entry_button = Button(match_setup_frame, text = 'Add', command =add_player_team1, font = text_box_font )
team1_player_entry_button.place(relx = 0.43, rely = 0.45, relwidth=0.075)
team1_playinglistbox = Listbox(match_setup_frame, height=5, font = text_box_font)
team1_playinglistbox.place(relx = 0.1, rely=0.5,relwidth = 0.15)
team1_team_player_list_label = Label(match_setup_frame, text = 'Home Team Players: ', font=text_box_font, bg = '#0C97EF')
team1_team_player_list_label.place(relx = 0.1, rely = 0.45, relwidth= 0.15, relheight=0.05)

#creating team1_list labels
team1_substitute_player_list_label = Label(match_setup_frame, text = 'Home Team Subs: ', background='#0C97EF', font = text_box_font)
team1_substitute_player_list_label.place(relx = 0.1, rely = 0.65, relheight=0.05, relwidth=0.15)

#creating team1_substitute entry box which is a listbox that stores the substitute player list
team1_player_substitute_entry_box = Entry(match_setup_frame, textvariable = varteam1sub, font = text_box_font)
team1_player_substitute_entry_box.place(relx=0.27, rely = 0.65, relwidth=0.15)
team1_substitute_player_list_add_button = Button(match_setup_frame, text = 'Add', command = add_sub_team1, font = text_box_font)
team1_substitute_player_list_add_button.place(relx = 0.43, rely = 0.65, relwidth=0.075)
team1_substitutebox = Listbox(match_setup_frame, height = 5, font = text_box_font)
team1_substitutebox.place(relx = 0.1, rely = 0.7, relwidth= 0.15)

#creating team 2 entry boxes
team2_entry_label = Label(match_setup_frame, text = "Enter Away Team Name: ", font=text_box_font, bg= '#EF340C')
team2_entry_label.place(relheight=0.05, relwidth=0.15,relx = 0.53, rely = 0.23)

#creating team 2 name entry box for the user to enter short text in there
team2_name = Entry(match_setup_frame, textvariable=varteam2name, font=text_box_font)
team2_name.place(relheight=0.05, relwidth=0.15, relx = 0.69, rely = 0.23)

#creating team 2 entering name label
team2_team_entering_label = Label(match_setup_frame, text = 'Away Team Players: ', font = text_box_font, bg = '#EF340C')
team2_team_entering_label.place(relx = 0.53, rely = 0.45, relwidth= 0.15, relheight=0.05)
team2_input_player_list = Entry(match_setup_frame, textvariable=varteam2player,font = text_box_font)
team2_input_player_list.place(relx=0.69, rely = 0.45, relwidth=0.15)

#creating the team 2 add player button 
team2_player_list_add_button = Button(match_setup_frame, text = 'Add', command = add_player_team2, font=text_box_font )
team2_player_list_add_button.place(relx = 0.85, rely= 0.45, relwidth=0.075)


team2_playinglistbox = Listbox(match_setup_frame, height = 5, font = text_box_font )
team2_playinglistbox.place(relx = 0.53, rely=0.5,relwidth = 0.15)

#creating team 2 subsittute player list and listbox to display players that have been added to the team
team2_substitute_player_list_label = Label(match_setup_frame, text = 'Away Team Subs: ', background='#EF340C', font = text_box_font)
team2_substitute_player_list_label.place(relx = 0.53, rely = 0.65, relheight=0.05, relwidth=0.15)
team2_player_substitute_entry_box = Entry(match_setup_frame, textvariable = varteam2sub, font = text_box_font)
team2_player_substitute_entry_box.place(relx=0.69, rely = 0.65, relwidth=0.15)
team2_substitute_player_list_add_button = Button(match_setup_frame, text = 'Add', command = add_sub_team2, font = text_box_font)
team2_substitute_player_list_add_button.place(relx = 0.85, rely = 0.65, relwidth=0.075)
team2_substitutebox = Listbox(match_setup_frame, height = 5, font = text_box_font)
team2_substitutebox.place(relx = 0.53, rely = 0.7, relwidth= 0.15)


#creating the next button which switches frames from match_setup_screen to main_screen
next_button = Button(match_setup_frame, text = 'Next', font = text_box_font, command = main_screen_switch)
next_button.place(relheight=0.05, relwidth=0.15, relx= 0.80, rely = 0.90)

#creating the main screen 
main_screen_root_frame = Frame(root)
main_screen_root_frame.columnconfigure(0, weight=1)
main_screen_root_frame.rowconfigure(0,weight=9)
main_screen_root_frame.rowconfigure(1, weight=1)

#creating the main_screen_frame
main_screen_frame = Frame(main_screen_root_frame)


main_screen_image = ImageTk.PhotoImage(file = 'images/how-to-buy-a-basketball-2.png')
background_main_screen = Label(main_screen_frame, image=main_screen_image)
background_main_screen.place(x=0, y=0, relwidth=1, relheight=1)

#getting and putting the team 1 name as a lable
home_team_name = Label(main_screen_frame, textvariable = varteam1name,font = Font(weight = 'bold', size = 30), bg= '#0C97EF')
home_team_name.place(relwidth=0.25, relheight=0.05, relx = 0.00, rely = 0.010)
#getting and putting the team 2 name as a label
away_team_name = Label(main_screen_frame, textvariable = varteam2name, font = Font(weight = 'bold', size = 30), bg = '#EF340C')
away_team_name.place(relwidth=0.25, relheight=0.05, relx = 0.75, rely = 0.010)

scorelabel_home_team1 = Label(main_screen_frame, bg = '#0C97EF', textvariable=varhomescore, font=Font(family="Calibri", size=192),borderwidth=2)
scorelabel_home_team1.place(relheight=0.4, relwidth=0.25, relx = 0.25, rely=0.010)

scorelabel_home_team2 = Label(main_screen_frame, bg = '#EF340C',textvariable=varawayscore, font = Font(family='Calibri', size = 192),borderwidth=2)
scorelabel_home_team2.place(relheight=0.4, relwidth=0.25, relx = 0.5, rely=0.010)

#creating a label for players 
player_playing_label_home = Label(main_screen_frame, text = 'Playing: ', font = Font(weight = 'bold'))
player_playing_label_home.place(relx=0.01,rely=0.08,relwidth=0.23)

#creating another list of players playing 
listbox_current_players_main_screen_home = Listbox(main_screen_frame, height=5, exportselection=0, font=text_box_font)
listbox_current_players_main_screen_home.place(relx=0.01,rely=0.12,relwidth=0.23)

#creating a label for Substitutes 
player_substitutes_label_home = Label(main_screen_frame, text = 'Substitutes: ', font = Font(weight = 'bold'))
player_substitutes_label_home.place(relx=0.01,rely=0.25,relwidth=0.23)

#creating another list of players playing 
listbox_substitutes_players_main_screen_home = Listbox(main_screen_frame, height=5, exportselection=0, font=text_box_font)
listbox_substitutes_players_main_screen_home.place(relx=0.01,rely=0.29,relwidth=0.23)

#creating a list of players playing for opposing team

player_playing_label_away = Label(main_screen_frame, text = 'Playing: ', font = Font(weight = 'bold'))
player_playing_label_away.place(relx = 0.76, rely =0.08, relwidth=0.23)

listbox_current_players_main_screen_away = Listbox(main_screen_frame, height=5, exportselection=0, font=text_box_font)
listbox_current_players_main_screen_away.place(relx=0.76,rely=0.12,relwidth=0.23)

player_playing_label_away = Label(main_screen_frame, text = 'Substitutes: ', font = Font(weight = 'bold'))
player_playing_label_away.place(relx=0.76,rely=0.25, relwidth=0.23)

listbox_substitutes_players_main_screen_away = Listbox(main_screen_frame, height=5, exportselection=0, font=text_box_font)
listbox_substitutes_players_main_screen_away.place(relx=0.76,rely=0.29,relwidth=0.23)



#points for home team 
points_for_home_team_label = Label(main_screen_frame, text = 'Points: ', font = Font(weight = 'bold'))
points_for_home_team_label.place(relx = 0.01, rely = 0.41, relwidth=0.23)

one_pointer_home_team = Button(main_screen_frame, text = '+1', command = lambda:update_score_home_team(1),font = Font(weight = 'bold'))
one_pointer_home_team.place(relx=0.01, rely = 0.46)
two_pointer_home_team = Button(main_screen_frame, text = '+2', command = lambda:update_score_home_team(2),font = Font(weight = 'bold'))
two_pointer_home_team.place(relx=0.045, rely = 0.46)
three_pointer_home_team = Button(main_screen_frame, text = '+3', command = lambda:update_score_home_team(3),font = Font(weight = 'bold'))
three_pointer_home_team.place(relx=0.08, rely = 0.46)
foul_home_team = Button(main_screen_frame, text = 'Foul', font = Font(weight = 'bold'), command=update_fouls_home_team)
foul_home_team.place(relx=0.115, rely = 0.46)
substitute_for_home_team_button = Button(main_screen_frame, text='Substitute', command = substitution_home_team,font = Font(weight = 'bold'))
substitute_for_home_team_button.place(relx = 0.165, rely=0.46)

#Scoring for home team
home_scoring_text = Text(main_screen_frame,font=text_box_font)
home_scoring_text.bind("<Key>", lambda a: "break")
home_scoring_text.place(relx=0.01, rely=0.53, relwidth=0.23, relheight=0.35)

#points for away team 
points_for_away_team_label = Label(main_screen_frame,text = 'Points: ', font = Font(weight='bold'))
points_for_away_team_label.place(relx = 0.76, rely = 0.41,relwidth=0.23) 
one_pointer_away_team = Button(main_screen_frame, text = '+1', command= lambda: update_score_away_team(1),font = Font(weight = 'bold'))
one_pointer_away_team.place(relx = 0.76, rely = 0.46)
two_pointer_away_team = Button(main_screen_frame, text = '+2', command = lambda: update_score_away_team(2),font = Font(weight = 'bold'))
two_pointer_away_team.place(relx = 0.795, rely= 0.46)
three_pointer_away_team = Button(main_screen_frame, text = '+3', command = lambda: update_score_away_team(3),font = Font(weight = 'bold'))
three_pointer_away_team.place(relx = 0.83, rely= 0.46)
foul_away_team = Button(main_screen_frame, text = 'Foul', font = Font(weight = 'bold'), command=update_fouls_away_team)
foul_away_team.place(relx=0.865, rely = 0.46)
substitute_for_away_team_button = Button(main_screen_frame, text='Substitute', command = substitution_away_team,font = Font(weight = 'bold'))
substitute_for_away_team_button.place(relx = 0.915, rely=0.46)

#Scoring for away team
away_scoring_text = Text(main_screen_frame,font=text_box_font)
away_scoring_text.bind("<Key>", lambda a: "break")
away_scoring_text.place(relx=0.76, rely=0.53, relwidth=0.23, relheight=0.35)

#timer 
timer_label_box = Label(main_screen_frame, bg ='#ffffff', textvariable=vartimereamaining, font = Font(size = 200))
timer_label_box.place(relx= 0.25, rely = 0.42, relwidth=0.50, relheight=0.3)


#creating the total number of quarters 
quarter_frame = Frame(main_screen_root_frame, bg = '#ffffff')

#quarter_frame.place(relx=-1, rely=-1, relheight=0.1, relwidth=1)
total_number_of_quarters_label = Label(quarter_frame, text = "Total Number of Quarters: ", bg = '#ffffff', font = Font(weight = 'bold'))
total_number_of_quarters_label.place(relx = 0.2, rely=0.4)
total_number_of_quarters = Label(quarter_frame, textvariable= vartotalnumberofquarters, bg = '#ffffff', font = Font(weight = 'bold'))
total_number_of_quarters.place(relx = 0.39, rely = 0.4)

#creating current quarter
current_quarter_label = Label(quarter_frame, text = 'Current Quarter: ', background='#ffffff', font= Font(weight = 'bold'))
current_quarter_label.place(relx= 0.45, rely = 0.4)
current_quarter = Label(quarter_frame, bg = '#ffffff', textvariable=varcurrentquarter, font= Font(weight = 'bold'))
current_quarter.place(relx = 0.6, rely = 0.4)
varcurrentquarter.set('0')

next_quarter_button = Button(quarter_frame, text = 'Next Quarter', font = text_box_font, command = switch_quarter)
next_quarter_button.place(relheight=0.3, relwidth=0.15, relx=0.7, rely = 0.4)

main_screen_frame.grid(row=0, column=0, sticky='nsew')
quarter_frame.grid(row=1, column=0, sticky='nsew')

#creating the results frame, with results showing the team that won, along with points and fouls scored from players of respective teams
result_frame = Frame(root)

result_screen_image = ImageTk.PhotoImage(file = 'images/how-to-buy-a-basketball-2.png')
background_result_screen = Label(result_frame, image=result_screen_image)
background_result_screen.place(x=0, y=0, relwidth=1, relheight=1)

winning_team_name = Label(result_frame, textvariable = winningteamname,font = Font(weight = 'bold', size = 30), bg= '#0C97EF')
winning_team_name.place(relx = 0.01, rely = 0.01, relwidth=.98, relheight=0.1)

player_scores_team1_result = Label(result_frame, text="Scores",font = text_box_font, bg= '#0C97EF')
player_scores_team1_result.place(relx=0.01, rely=0.11, relwidth=0.245, relheight=0.06)

home_team_name_result = Label(result_frame, textvariable = varteam1name,font = Font(weight = 'bold', size = 30), bg= '#0C97EF')
home_team_name_result.place(relx=0.255, rely=0.11, relwidth=0.245, relheight=0.06)

away_team_name_result = Label(result_frame, textvariable = varteam2name,font = Font(weight = 'bold', size = 30), bg= '#EF340C')
away_team_name_result.place(relx=0.50, rely=0.11, relwidth=0.245, relheight=0.06)

player_scores_team2_result = Label(result_frame, text="Scores",font = text_box_font,bg = '#EF340C')
player_scores_team2_result.place(relx=0.745, rely=0.11, relwidth=0.245, relheight=0.06)

scores_team1_result = Text(result_frame, font=text_box_font)
scores_team1_result.place(relx = 0.01, rely=0.17,relheight=0.4, relwidth=0.23)

scorelabel_team1_result = Label(result_frame, bg = '#0C97EF',textvariable=varhomescore, font = Font(family='Calibri', size = 192),borderwidth=2)
scorelabel_team1_result.place(relheight=0.4, relwidth=0.245, relx = 0.255, rely=0.17)

scorelabel_team2_result = Label(result_frame, bg = '#EF340C',textvariable=varawayscore, font = Font(family='Calibri', size = 192),borderwidth=2)
scorelabel_team2_result.place(relheight=0.4, relwidth=0.245, relx = 0.5, rely=0.17)

scores_team2_result = Text(result_frame, font=text_box_font)
scores_team2_result.place(relx = 0.76, rely=0.17,relheight=0.4, relwidth=0.23)

player_fouls_team1_result = Label(result_frame, text="Fouls",font = text_box_font, bg = '#0C97EF')
player_fouls_team1_result.place(relx=0.01, rely=0.58, relwidth=0.23, relheight=0.06)

player_fouls_team2_result = Label(result_frame, text="Fouls",font = text_box_font, bg = '#EF340C')
player_fouls_team2_result.place(relx=0.76, rely=0.58, relwidth=0.23, relheight=0.06)

fouls_team1_result = Text(result_frame, font=text_box_font)
fouls_team1_result.place(relx = 0.01, rely=0.65,relheight=0.3, relwidth=0.23)

fouls_team2_result = Text(result_frame, font=text_box_font)
fouls_team2_result.place(relx = 0.76, rely=0.65,relheight=0.3, relwidth=0.23)

exit_game_result = Button(result_frame, text = 'Exit', font = Font(family='Calibri', size = 50), command = root.quit)
exit_game_result.place(relheight=0.2, relwidth=0.49, relx=0.255, rely = 0.65)

root.mainloop()
#end 