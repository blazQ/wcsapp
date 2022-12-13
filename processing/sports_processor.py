import csv
import json
import pandas as pd
import numpy as np
import xgboost as xgb

import requests
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def get_wc_matches_csv(file_handle):
    # Recupera i dettagli di ogni match
    response = requests.get("https://worldcupjson.net/matches?details=true")
    # Carica il JSON
    matches = json.loads(response.text)

    with open(file_handle, "a", encoding="utf-8") as f:
        # ottieni un writer per il file csv
        match_writer = csv.writer(f, delimiter=',')
        # scrivi le intestazioni di ogni colonna
        match_writer.writerow(['id',
                               'home_team_country',
                               'away_team_country',
                               'winner',
                               'home_team_goals',
                               'home_team_penalties',
                               'away_team_goals',
                               'away_team_penalties',
                               'home_team_attempts_on_goal',
                               'home_team_on_target',
                               'home_team_corners',
                               'home_team_offsides',
                               'home_team_num_passes',
                               'home_team_passes_completed',
                               'home_team_tackles',
                               'home_team_goal_kicks',
                               'home_team_throw_ins',
                               'home_team_yellow_cards',
                               'home_team_red_cards',
                               'home_team_fouls_committed',
                               'away_team_attempts_on_goal',
                               'away_team_on_target',
                               'away_team_corners',
                               'away_team_offsides',
                               'away_team_num_passes',
                               'away_team_passes_completed',
                               'away_team_tackles',
                               'away_team_goal_kicks',
                               'away_team_throw_ins',
                               'away_team_yellow_cards',
                               'away_team_red_cards',
                               'away_team_fouls_committed']
                              )
        # Per ogni match del  mondiale
        for i in range(0, 58):
            # Recupera l'ID del match
            match_id = matches[i]['id']
            # Squadre che giocano
            match_home_team_country = matches[i]['home_team_country']
            match_away_team_country = matches[i]['away_team_country']
            # Vincitore
            winner = matches[i]['winner']
            # Tabellino
            home_team_goals = matches[i]['home_team']['goals']
            home_team_penalties = matches[i]['home_team']['penalties']
            away_team_goals = matches[i]['away_team']['goals']
            away_team_penalties = matches[i]['away_team']['penalties']

            # Home stats
            home_team_attempts_on_goal = matches[i]["home_team_statistics"]['attempts_on_goal']
            home_team_on_target = matches[i]["home_team_statistics"]['on_target']
            home_team_corners = matches[i]["home_team_statistics"]['corners']
            home_team_offsides = matches[i]["home_team_statistics"]['offsides']
            home_team_num_passes = matches[i]["home_team_statistics"]['num_passes']
            home_team_passes_completed = matches[i]["home_team_statistics"]['passes_completed']
            home_team_tackles = matches[i]["home_team_statistics"]['tackles']
            home_team_goal_kicks = matches[i]["home_team_statistics"]['goal_kicks']
            home_team_throw_ins = matches[i]["home_team_statistics"]['throw_ins']
            home_team_yellow_cards = matches[i]["home_team_statistics"]['yellow_cards']
            home_team_red_cards = matches[i]["home_team_statistics"]['red_cards']
            home_team_fouls_committed = matches[i]["home_team_statistics"]['fouls_committed']

            # Away stats
            away_team_attempts_on_goal = matches[i]["away_team_statistics"]['attempts_on_goal']
            away_team_on_target = matches[i]["away_team_statistics"]['on_target']
            away_team_corners = matches[i]["away_team_statistics"]['corners']
            away_team_offsides = matches[i]["away_team_statistics"]['offsides']
            away_team_num_passes = matches[i]["away_team_statistics"]['num_passes']
            away_team_passes_completed = matches[i]["away_team_statistics"]['passes_completed']
            away_team_tackles = matches[i]["away_team_statistics"]['tackles']
            away_team_goal_kicks = matches[i]["away_team_statistics"]['goal_kicks']
            away_team_throw_ins = matches[i]["away_team_statistics"]['throw_ins']
            away_team_yellow_cards = matches[i]["away_team_statistics"]['yellow_cards']
            away_team_red_cards = matches[i]["away_team_statistics"]['red_cards']
            away_team_fouls_committed = matches[i]["away_team_statistics"]['fouls_committed']

            # Scrivi le informazioni del match nel file
            match_writer.writerow([match_id,
                                   match_home_team_country,
                                   match_away_team_country,
                                   winner,
                                   home_team_goals,
                                   home_team_penalties,
                                   away_team_goals,
                                   away_team_penalties,
                                   home_team_attempts_on_goal,
                                   home_team_on_target,
                                   home_team_corners,
                                   home_team_offsides,
                                   home_team_num_passes,
                                   home_team_passes_completed,
                                   home_team_tackles,
                                   home_team_goal_kicks,
                                   home_team_throw_ins,
                                   home_team_yellow_cards,
                                   home_team_red_cards,
                                   home_team_fouls_committed,
                                   away_team_attempts_on_goal,
                                   away_team_on_target,
                                   away_team_corners,
                                   away_team_offsides,
                                   away_team_num_passes,
                                   away_team_passes_completed,
                                   away_team_tackles,
                                   away_team_goal_kicks,
                                   away_team_throw_ins,
                                   away_team_yellow_cards,
                                   away_team_red_cards,
                                   away_team_fouls_committed]
                                  )


# Questa funzione prende in input una dataframe relativo a una singola partita e lo splitta in due dataframe,
# uno per la squadra di casa E uno per la squadra fuori casa. Toglie colonne che non servono e ne aggiunge di nuove
# per il corretto funzionamento del modello

def game_data(game_df):
    try:
        away_team_df = game_df[['away_team_country',
                                'away_team_goals',
                                'away_team_penalties',
                                'away_team_attempts_on_goal',
                                'away_team_on_target',
                                'away_team_corners',
                                'away_team_offsides',
                                'away_team_num_passes',
                                'away_team_passes_completed',
                                'away_team_tackles',
                                'away_team_goal_kicks',
                                'away_team_throw_ins',
                                'away_team_yellow_cards',
                                'away_team_red_cards',
                                'away_team_fouls_committed']].rename(columns={'away_team_country':
                                                                                  'team_country',
                                                                              'away_team_goals':
                                                                                  'team_goals',
                                                                              'away_team_penalties':
                                                                                  'team_penalties',
                                                                              'away_team_attempts_on_goal':
                                                                                  'team_attempts_on_goal',
                                                                              'away_team_on_target':
                                                                                  'team_on_target',
                                                                              'away_team_corners':
                                                                                  'team_corners',
                                                                              'away_team_offsides':
                                                                                  'team_offsides',
                                                                              'away_team_num_passes':
                                                                                  'team_num_passes',
                                                                              'away_team_passes_completed':
                                                                                  'team_passes_completed',
                                                                              'away_team_tackles':
                                                                                  'team_tackles',
                                                                              'away_team_goal_kicks':
                                                                                  'team_goal_kicks',
                                                                              'away_team_throw_ins':
                                                                                  'team_throw_ins',
                                                                              'away_team_yellow_cards':
                                                                                  'team_yellow_cards',
                                                                              'away_team_red_cards':
                                                                                  'team_red_cards',
                                                                              'away_team_fouls_committed':
                                                                                  'team_fouls_committed'})

        home_team_df = game_df[['home_team_country',
                                'home_team_goals',
                                'home_team_penalties',
                                'home_team_attempts_on_goal',
                                'home_team_on_target',
                                'home_team_corners',
                                'home_team_offsides',
                                'home_team_num_passes',
                                'home_team_passes_completed',
                                'home_team_tackles',
                                'home_team_goal_kicks',
                                'home_team_throw_ins',
                                'home_team_yellow_cards',
                                'home_team_red_cards',
                                'home_team_fouls_committed']].rename(columns={'home_team_country': 'team_country',
                                                                              'home_team_goals': 'team_goals',
                                                                              'home_team_penalties': 'team_penalties',
                                                                              'home_team_attempts_on_goal':
                                                                                  'team_attempts_on_goal',
                                                                              'home_team_on_target':
                                                                                  'team_on_target',
                                                                              'home_team_corners':
                                                                                  'team_corners',
                                                                              'home_team_offsides':
                                                                                  'team_offsides',
                                                                              'home_team_num_passes':
                                                                                  'team_num_passes',
                                                                              'home_team_passes_completed':
                                                                                  'team_passes_completed',
                                                                              'home_team_tackles':
                                                                                  'team_tackles',
                                                                              'home_team_goal_kicks':
                                                                                  'team_goal_kicks',
                                                                              'home_team_throw_ins':
                                                                                  'team_throw_ins',
                                                                              'home_team_yellow_cards':
                                                                                  'team_yellow_cards',
                                                                              'home_team_red_cards':
                                                                                  'team_red_cards',
                                                                              'home_team_fouls_committed':
                                                                                  'team_fouls_committed'})
        try:
            if game_df.loc[0, 'away_team_goals'] > game_df.loc[0, 'home_team_goals']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [1], 'game_lost': [0]}),
                                        left_index=True, right_index=True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [1]}),
                                        left_index=True, right_index=True)
            elif game_df.loc[0, 'away_team_goals'] < game_df.loc[0, 'home_team_goals']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [1]}),
                                        left_index=True, right_index=True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [1], 'game_lost': [0]}),
                                        left_index=True, right_index=True)
            else:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [0]}),
                                        left_index=True, right_index=True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [0]}),
                                        left_index=True, right_index=True)
        except TypeError:
            away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [np.nan], 'game_lost': [np.nan]}),
                                    left_index=True, right_index=True)
            home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [np.nan], 'game_lost': [np.nan]}),
                                    left_index=True, right_index=True)

    except TypeError:
        away_team_df = pd.DataFrame()
        home_team_df = pd.DataFrame()
    return away_team_df, home_team_df


def game_data_up_to_week(weeks, file_handle):
    # Crea dataset vuoto
    weeks_games_df = pd.DataFrame()
    # Leggi quante righe quante partite vuoi recuperare
    weeks_games_df_raw = pd.read_csv(file_handle)
    weeks_games_df_raw = weeks_games_df_raw[weeks_games_df_raw.week < weeks]
    # Per ogni riga, calcola il dataset del team away, il dataset del team home e uniscili al risultato.
    for index, row in weeks_games_df_raw.iterrows():
        row_df = row.to_frame().transpose()
        row_df.reset_index(inplace=True)
        away_team_df, home_team_df = game_data(row_df)
        away_team_df['week'] = row.week
        home_team_df['week'] = row.week
        weeks_games_df = pd.concat([weeks_games_df, away_team_df])
        weeks_games_df = pd.concat([weeks_games_df, home_team_df])
    # restituisci il dataset risultante
    return weeks_games_df


def agg_weekly_data(schedule_df, weeks_games_df, current_week, weeks):
    schedule_df = schedule_df[schedule_df.week < current_week]

    agg_games_df = pd.DataFrame()
    for w in range(1, len(weeks)):
        games_df = schedule_df[schedule_df.week == weeks[w]]
        agg_weekly_df = weeks_games_df[weeks_games_df.week < weeks[w]].drop(
            columns=['week', 'game_won', 'game_lost', 'team_goals']).groupby(by=['team_country']).mean().reset_index()
        win_loss_df = weeks_games_df[weeks_games_df.week < weeks[w]][
            ['team_country', 'game_won', 'game_lost']].groupby(by=['team_country']).sum().reset_index()
        win_loss_df['win_perc'] = win_loss_df['game_won'] / (win_loss_df['game_won'] + win_loss_df['game_lost'])
        win_loss_df = win_loss_df.drop(columns=['game_won', 'game_lost'])
        win_loss_df['win_perc'] = win_loss_df['win_perc'].fillna(0)

        try:
            agg_weekly_df['pass_perc'] = agg_weekly_df['team_passes_completed'] / agg_weekly_df['team_num_passes']
        except ZeroDivisionError:
            agg_weekly_df['pass_perc'] = 0
        agg_weekly_df['pass_perc'] = agg_weekly_df['pass_perc'].fillna(0)

        try:
            agg_weekly_df['shot_prec_perc'] = agg_weekly_df['team_on_target'] / agg_weekly_df[
                'team_attempts_on_goal']
        except ZeroDivisionError:
            agg_weekly_df['shot_prec_perc'] = 0
        agg_weekly_df['shot_prec_perc'] = agg_weekly_df['shot_prec_perc'].fillna(0)

        agg_weekly_df = agg_weekly_df.drop(
            columns=['team_passes_completed', 'team_num_passes', 'team_attempts_on_goal', 'team_on_target'])
        agg_weekly_df = pd.merge(win_loss_df, agg_weekly_df, left_on=['team_country'], right_on=['team_country'])

        away_df = pd.merge(games_df, agg_weekly_df, how='inner', left_on=['away_team_country'],
                           right_on=['team_country']).drop(columns=['team_country']).rename(columns={
            'win_perc': 'away_win_perc',
            'shot_prec_perc': 'away_shot_perc',
            'pass_perc': 'away_pass_perc',
            'team_corners': 'away_corners',
            'team_offsides': 'away_offsides',
            'team_tackles': 'away_tackles',
            'team_goal_kicks': 'away_goal_kicks',
            'team_throw_ins': 'away_throw_ins',
            'team_yellow_cards': 'away_yellow_cards',
            'team_red_cards': 'away_red_cards',
            'team_fouls_committed': 'away_fouls_committed'
        })  # Statistiche dal match away

        home_df = pd.merge(games_df, agg_weekly_df, how='inner', left_on=['home_team_country'],
                           right_on=['team_country']).drop(columns=['team_country']).rename(columns={
            'win_perc': 'home_win_perc',
            'shot_prec_perc': 'home_shot_perc',
            'pass_perc': 'home_pass_perc',
            'team_corners': 'home_corners',
            'team_offsides': 'home_offsides',
            'team_tackles': 'home_tackles',
            'team_goal_kicks': 'home_goal_kicks',
            'team_throw_ins': 'home_throw_ins',
            'team_yellow_cards': 'home_yellow_cards',
            'team_red_cards': 'home_red_cards',
            'team_fouls_committed': 'home_fouls_committed'
        })  # Statistiche dal match home

        agg_weekly_df = pd.merge(away_df, home_df, left_on=['away_team_country', 'home_team_country', 'winner', 'week'],
                                 right_on=['away_team_country', 'home_team_country', 'winner', 'week'])  # Merge di
        # away e home
        # Accumula i risultati
        agg_weekly_df['win_perc_dif'] = agg_weekly_df['away_win_perc'] - agg_weekly_df['home_win_perc']
        agg_weekly_df['pass_perc_dif'] = agg_weekly_df['away_pass_perc'] - agg_weekly_df['home_pass_perc']
        agg_weekly_df['shot_perc_dif'] = agg_weekly_df['away_shot_perc'] - agg_weekly_df['home_shot_perc']
        agg_weekly_df['corner_dif'] = agg_weekly_df['away_corners'] - agg_weekly_df['home_corners']
        agg_weekly_df['offsides_dif'] = agg_weekly_df['away_offsides'] - agg_weekly_df['home_offsides']
        agg_weekly_df['tackles_dif'] = agg_weekly_df['away_tackles'] - agg_weekly_df['home_tackles']
        agg_weekly_df['goal_kicks_dif'] = agg_weekly_df['away_goal_kicks'] - agg_weekly_df['home_goal_kicks']
        agg_weekly_df['throw_ins_diff'] = agg_weekly_df['away_throw_ins'] - agg_weekly_df['home_throw_ins']
        agg_weekly_df['yellow_cards_diff'] = agg_weekly_df['away_yellow_cards'] - agg_weekly_df['home_yellow_cards']
        agg_weekly_df['red_cards_diff'] = agg_weekly_df['away_red_cards'] - agg_weekly_df['home_red_cards']
        agg_weekly_df['fouls_committed_diff'] = agg_weekly_df['away_fouls_committed'] - agg_weekly_df[
            'home_fouls_committed']

        agg_weekly_df = agg_weekly_df.drop(columns=['away_win_perc', 'away_shot_perc', 'away_pass_perc', 'away_corners',
                                                    'away_offsides', 'away_tackles', 'away_goal_kicks',
                                                    'away_throw_ins',
                                                    'away_yellow_cards', 'away_red_cards', 'away_fouls_committed',
                                                    'home_win_perc', 'home_shot_perc', 'home_pass_perc', 'home_corners',
                                                    'home_offsides', 'home_tackles', 'home_goal_kicks',
                                                    'home_throw_ins',
                                                    'home_yellow_cards', 'home_red_cards', 'home_fouls_committed'
                                                    ])

        if agg_weekly_df['winner'].isnull().values.any() and weeks[w] > 3:
            agg_weekly_df['result'] = np.nan
            print(f'Week {weeks[w]} games have not finished yet.')
        else:
            agg_weekly_df['result'] = agg_weekly_df['winner'] == agg_weekly_df['away_team_country']
            agg_weekly_df['result'] = agg_weekly_df['result'].astype('float')
        agg_weekly_df = agg_weekly_df.drop(columns=['winner'])
        agg_games_df = pd.concat([agg_games_df, agg_weekly_df])

    agg_games_df = agg_games_df.reset_index().drop(columns='index')
    # agg_games_df = agg_games_df.drop(index=20, axis=0)

    return agg_games_df


def add_week_columm(file_handle, file_handle_output):
    # Open the input_file in read mode and output_file in write mode
    with open(file_handle, 'r') as read_obj, \
            open(file_handle_output, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj)
        # Read each row of the input csv file as list
        i = 0
        for row in csv_reader:
            if i == 0:
                row.append('week')
            if 0 < i < 17:  # Primo turno
                row.append(1)
            elif 16 < i < 33:  # Secondo turno
                row.append(2)
            elif 32 < i < 49:  # Terzo turno
                row.append(3)
            elif 48 < i < 57:  # Ottavi di finale
                row.append(4)
            elif 56 < i < 61:  # Quarti di finale
                row.append(5)
            elif 60 < i < 63:  # Semifinali
                row.append(6)
            elif 62 < i < 65:  # Finale e finale per il terzo posto
                row.append(7)
            i += 1
            # Add the updated row / list to the output file
            csv_writer.writerow(row)


def change_winner_column(file_handle, file_handle_output):
    # Open the input_file in read mode and output_file in write mode
    with open(file_handle, 'r') as read_obj, \
            open(file_handle_output, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            if row[3] == 'Ecuador':
                row[3] = 'ECU'
            if row[3] == 'Qatar':
                row[3] = 'QAT'
            if row[3] == 'Netherlands':
                row[3] = 'NED'
            if row[3] == 'Senegal':
                row[3] = 'SEN'
            if row[3] == 'England':
                row[3] = 'ENG'
            if row[3] == 'Wales':
                row[3] = 'WAL'
            if row[3] == 'Iran':
                row[3] = 'IRN'
            if row[3] == 'United States':
                row[3] = 'USA'
            if row[3] == 'Mexico':
                row[3] = 'MEX'
            if row[3] == 'Poland':
                row[3] = 'POL'
            if row[3] == 'Argentina':
                row[3] = 'ARG'
            if row[3] == 'Tunisia':
                row[3] = 'TUN'
            if row[3] == 'Australia':
                row[3] = 'AUS'
            if row[3] == 'Denmark':
                row[3] = 'DEN'
            if row[3] == 'France':
                row[3] = 'FRA'
            if row[3] == 'Spain':
                row[3] = 'ESP'
            if row[3] == 'Japan':
                row[3] = 'JAP'
            if row[3] == 'Germany':
                row[3] = 'GER'
            if row[3] == 'Croatia':
                row[3] = 'CRO'
            if row[3] == 'Belgium':
                row[3] = 'BEL'
            if row[3] == 'Morocco':
                row[3] = 'MAR'
            if row[3] == 'Canada':
                row[3] = 'CAN'
            if row[3] == 'Brazil':
                row[3] = 'BRA'
            if row[3] == 'Serbia':
                row[3] = 'SRB'
            if row[3] == 'Cameroon':
                row[3] = 'CMR'
            if row[3] == 'Switzerland':
                row[3] = 'SUI'
            if row[3] == 'Ghana':
                row[3] = 'GHA'
            if row[3] == 'Uruguay':
                row[3] = 'URU'
            if row[3] == 'Portugal':
                row[3] = 'POR'
            if row[3] == 'Saudi Arabia':
                row[3] = 'KSA'
            if row[3] == 'Costa Rica':
                row[3] = 'CRC'
            if row[3] == 'Korea Republic':
                row[3] = 'KOR'
            # Add the updated row / list to the output file
            csv_writer.writerow(row)


def extract_schedule(file_handle=None, file_handle_output=None):
    # Open the input_file in read mode and output_file in write mode
    with open(file_handle, 'r') as read_obj, \
            open(file_handle_output, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            csv_writer.writerow([row[0], row[1], row[2], row[3], row[32]])


def display(y_pred, X_test):
    for g in range(len(y_pred)):
        win_prob = round(y_pred[g], 2)
        away_team = X_test.reset_index().drop(columns='id_x').loc[g, 'away_team_country']
        home_team = X_test.reset_index().drop(columns='id_x').loc[g, 'home_team_country']
        print(f'The {away_team} have a probability of {win_prob} of beating the {home_team}.')


def prep_test_train(current_week, weeks):
    current_week = current_week + 1
    schedule_df = pd.read_csv('schedule.csv')
    weeks_games_df = game_data_up_to_week(current_week, 'matchesFinalVer.csv')
    agg_games_df = agg_weekly_data(schedule_df, weeks_games_df, current_week, weeks)
    # get sentiment
    # merge sentiment

    train_df = agg_games_df[agg_games_df.result.notna()]
    current_week = current_week - 1
    test_df = agg_games_df[agg_games_df.week == current_week]
    return test_df, train_df


current = 6
weeks = list(range(1, current + 1))

pred_games_df, comp_games_df = prep_test_train(current_week=current, weeks=weeks)
msk = np.random.rand(len(comp_games_df)) < 0.8

train_df = comp_games_df[msk]
test_df = comp_games_df[~msk]

X_train = train_df.drop(columns=['away_team_country', 'home_team_country', 'week', 'result'])
print(X_train.isnull().sum())


y_train = train_df[['result']]
X_test = test_df.drop(columns=['away_team_country', 'home_team_country', 'week', 'result'])
y_test = test_df[['result']]

# Primo test usando logistic regression

clf = LogisticRegression(penalty='l1', dual=False, tol=0.001, C=1.0, fit_intercept=True,
                         intercept_scaling=1, class_weight='balanced', random_state=None,
                         solver='liblinear', max_iter=1000, multi_class='ovr', verbose=0)
clf.fit(X_train, np.ravel(y_train.values))
y_pred = clf.predict_proba(X_test)
y_pred = y_pred[:, 1]

# display(y_pred, test_df)
# print(accuracy_score(y_test, np.round(y_pred)))

# Secondo test usando xgboost
dtest = xgb.DMatrix(X_test, y_test, feature_names=X_test.columns)
dtrain = xgb.DMatrix(X_train, y_train, feature_names=X_train.columns)

param = {'verbosity': 1,
         'objective': 'binary:hinge',
         'feature_selector': 'shuffle',
         'booster': 'gblinear',
         'eval_metric': 'error',
         'learning_rate': 0.05}

evallist = [(dtrain, 'train'), (dtest, 'test')]

num_round = 1000
bst = xgb.train(param, dtrain, num_round, evallist)

X_test = pred_games_df.drop(columns=['away_team_country', 'home_team_country', 'week', 'result'])
y_pred = clf.predict_proba(X_test)
y_pred = y_pred[:, 1]

display(y_pred, pred_games_df)
