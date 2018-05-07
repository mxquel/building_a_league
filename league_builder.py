import csv

#load data from provided csv file into the script
def get_player_info():
    """loads the player information from csv output_file
        returns a list of the information starting with the experienced players
        followed by the unexperienced players"""
    experienced = []
    inexperienced = []

    with open('soccer_players.csv', newline='') as f_obj:
        player_info = csv.DictReader(f_obj, delimiter=',')

        for player in player_info:
            if player['Soccer Experience'] == 'YES':
                experienced.append(player)
            else:
                inexperienced.append(player)

    return experienced + inexperienced


#evenly allocated players to one of three teams
def player_allocation():
    """takes the player information from the csv file and allocates evenly
        compiled lists of players to the three teams. returns a dictionary
        of the three teams"""
    members = get_player_info()
    teams = {'Sharks': [], 'Dragons': [], 'Raptors': []}

    for team, player_list in teams.items():
        while len(player_list) < 6:
            teams[team].append(members.pop(0))
            teams[team].append(members.pop())

    return teams


#assemble text
def team_roster(teams):
    """Takes the collection of allocated players and
        returns a formated string"""
    roster = ''

    for team, player_list in teams.items():
        roster += team.upper() + '\n'

        for item in player_list:
            roster += item['Name'] + ', '
            roster += item['Soccer Experience'] + ', '
            roster += item['Guardian Name(s)']
            roster += '\n'

        roster += '\n\n'

    return roster


#create names for welcome letter files
def generate_file_names(teams):
    """Creates names for welcome letter files from the teams collection
        returns a list of file names"""
    file_names = []

    for team, player_list in teams.items():
        for item in player_list:
            name_parts = item['Name'].split()
            file_name = name_parts[0].lower() + '_' + name_parts[1].lower() + '.txt'

            file_names.append(file_name)

    return file_names


def letter_content(teams):
    """Generates the content for the welcome letter for each player
        returns a list of all messages"""
    messages = []

    for team, player_list in teams.items():
        for item in player_list:
            content = 'Dear '
            guardians = item['Guardian Name(s)']
            player = item['Name']

            content += guardians + ',\n\n'
            content +=  player + ' will be playing for the ' + team + '.'
            content += ' First practice will be held 19 May at 10:00 am.\n\n'
            content += 'Kind regards,\n\n' + 'Coach'

            messages.append(content)

    return messages


if __name__ == '__main__':
    teams = player_allocation()
    file_names = generate_file_names(teams)
    messages = letter_content(teams)
    welcome_letters = [(f, m) for f, m in zip(file_names, messages)]

    #write allocated teams to a text file
    with open('team.txt', 'w') as roster_file:
        roster_file.write(team_roster(teams))

    #create welcome letters to players guardians
    for file_name, message in welcome_letters:
        with open('letters/' + file_name, 'w') as welcome_letter:
            welcome_letter.write(message)
