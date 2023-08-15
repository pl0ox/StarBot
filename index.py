import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
import re
import datetime
import time
import os
import datetime
import sys
import asyncio
from collections import defaultdict, OrderedDict  # Add this line
from operator import itemgetter
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all(), case_insensitive=True)
# Dictionary to store user wins
user_wins = {}
user_profiles = {}



team_emojis = {
    'REVBOUNTY': '<:revbounty:1085300248290791604>',
    'EX': '<:EX:1137171566044663908>',
    'VALOR': '<:valor:1085302902362476677>',
    'UNTB': '<:untb:1102624693015547914>',
    'Clanless': '<:No:108530289930065104>',
    'RXSPECT': '<:Rx:1130568134223483031>'
}

country_flags = {
        'Not assigned': ":x:",
        'AUSTRALIA': ":flag_au:",
        'AFGHANISTAN': ":flag_af:",
        'ALBANIA': ":flag_al:",
        'ALGERIA': ":flag_dz:",
        'ANDORRA': ":flag_ad:",
        'ANGOLA': ":flag_ao:",
        'ANTIGUA AND BARBUDA': ":flag_ag:",
        'ARGENTINA': ":flag_ar:",
        'ARMENIA': ":flag_am:",
        'ARUBA': ":flag_aw:",
        'AUSTRIA': ":flag_at:",
        'AZERBAIJAN': ":flag_az:",
        'BAHAMAS': ":flag_bs:",
        'BAHRAIN': ":flag_bh:",
        'BANGLADESH': ":flag_bd:",
        'BARBADOS': ":flag_bb:",
        'BELARUS': ":flag_by:",
        'BELGIUM': ":flag_be:",
        'BELIZE': ":flag_bz:",
        'BENIN': ":flag_bj:",
        'BERMUDA': ":flag_bm:",
        'BHUTAN': ":flag_bt:",
        'BOLIVIA': ":flag_bo:",
        'BOSNIA AND HERZEGOVINA': ":flag_ba:",
        'BOTSWANA': ":flag_bw:",
        'BRAZIL': ":flag_br:",
        'BRUNEI': ":flag_bn:",
        'BULGARIA': ":flag_bg:",
        'BURKINA FASO': ":flag_bf:",
        'BURUNDI': ":flag_bi:",
        'CAMBODIA': ":flag_kh:",
        'CAMEROON': ":flag_cm:",
        'CANADA': ":flag_ca:",
        'CAPE VERDE': ":flag_cv:",
        'CENTRAL AFRICAN REPUBLIC': ":flag_cf:",
        'CHAD': ":flag_td:",
        'CHILE': ":flag_cl:",
        'CHINA': ":flag_cn:",
        'COLOMBIA': ":flag_co:",
        'COMOROS': ":flag_km:",
        'CONGO': ":flag_cg:",
        'COOK ISLANDS': ":flag_ck:",
        'COSTA RICA': ":flag_cr:",
        'CROATIA': ":flag_hr:",
        'CUBA': ":flag_cu:",
        'CYPRUS': ":flag_cy:",
        'CZECH REPUBLIC': ":flag_cz:",
        'DEMOCRATIC REPUBLIC OF THE CONGO': ":flag_cd:",
        'DENMARK': ":flag_dk:",
        'DJIBOUTI': ":flag_dj:",
        'DOMINICA': ":flag_dm:",
        'DOMINICAN REPUBLIC': ":flag_do:",
        'EAST TIMOR': ":flag_tl:",
        'ECUADOR': ":flag_ec:",
        'EGYPT': ":flag_eg:",
        'EL SALVADOR': ":flag_sv:",
        'EQUATORIAL GUINEA': ":flag_gq:",
        'ERITREA': ":flag_er:",
        'ESTONIA': ":flag_ee:",
        'ESWATINI': ":flag_sz:",
        'ETHIOPIA': ":flag_et:",
        'FIJI': ":flag_fj:",
        'FINLAND': ":flag_fi:",
        'FRANCE': ":flag_fr:",
        'GABON': ":flag_ga:",
        'GAMBIA': ":flag_gm:",
        'GEORGIA': ":flag_ge:",
        'GERMANY': ":flag_de:",
        'GHANA': ":flag_gh:",
        'GREECE': ":flag_gr:",
        'GRENADA': ":flag_gd:",
        'GUATEMALA': ":flag_gt:",
        'GUINEA': ":flag_gn:",
        'GUINEA-BISSAU': ":flag_gw:",
        'GUYANA': ":flag_gy:",
        'HAITI': ":flag_ht:",
        'HONDURAS': ":flag_hn:",
        'HUNGARY': ":flag_hu:",
        'ICELAND': ":flag_is:",
        'INDIA': ":flag_in:",
        'INDONESIA': ":flag_id:",
        'IRAN': ":flag_ir:",
        'IRAQ': ":flag_iq:",
        'IRELAND': ":flag_ie:",
        'ISRAEL': ":flag_il:",
        'ITALY': ":flag_it:",
        'JAMAICA': ":flag_jm:",
        'JAPAN': ":flag_jp:",
        'JORDAN': ":flag_jo:",
        'KAZAKHSTAN': ":flag_kz:",
        'KENYA': ":flag_ke:",
        'KIRIBATI': ":flag_ki:",
        'NORTH KOREA': ":flag_kp:",
        'SOUTH KOREA': ":flag_kr:",
        'KOSOVO': ":flag_xk:",
        'KUWAIT': ":flag_kw:",
        'KYRGYZSTAN': ":flag_kg:",
        'LAOS': ":flag_la:",
        'LATVIA': ":flag_lv:",
        'LEBANON': ":flag_lb:",
        'LESOTHO': ":flag_ls:",
        'LIBERIA': ":flag_lr:",
        'LIBYA': ":flag_ly:",
        'LIECHTENSTEIN': ":flag_li:",
        'LITHUANIA': ":flag_lt:",
        'LUXEMBOURG': ":flag_lu:",
        'MADAGASCAR': ":flag_mg:",
        'MALAWI': ":flag_mw:",
        'MALAYSIA': ":flag_my:",
        'MALDIVES': ":flag_mv:",
        'MALI': ":flag_ml:",
        'MALTA': ":flag_mt:",
        'MARSHALL ISLANDS': ":flag_mh:",
        'MAURITANIA': ":flag_mr:",
        'MAURITIUS': ":flag_mu:",
        'MEXICO': ":flag_mx:",
        'MICRONESIA': ":flag_fm:",
        'MOLDOVA': ":flag_md:",
        'MONACO': ":flag_mc:",
        'MONGOLIA': ":flag_mn:",
        'MONTENEGRO': ":flag_me:",
        'MOROCCO': ":flag_ma:",
        'MOZAMBIQUE': ":flag_mz:",
        'MYANMAR': ":flag_mm:",
        'NAMIBIA': ":flag_na:",
        'NAURU': ":flag_nr:",
        'NEPAL': ":flag_np:",
        'NETHERLANDS': ":flag_nl:",
        'NEW ZEALAND': ":flag_nz:",
        'NICARAGUA': ":flag_ni:",
        'NIGER': ":flag_ne:",
        'NIGERIA': ":flag_ng:",
        'NORTH MACEDONIA': ":flag_mk:",
        'NORWAY': ":flag_no:",
        'OMAN': ":flag_om:",
        'PAKISTAN': ":flag_pk:",
        'PALAU': ":flag_pw:",
        'PALESTINE': ":flag_ps:",
        'PANAMA': ":flag_pa:",
        'PAPUA NEW GUINEA': ":flag_pg:",
        'PARAGUAY': ":flag_py:",
        'PERU': ":flag_pe:",
        'PHILIPPINES': ":flag_ph:",
        'POLAND': ":flag_pl:",
        'PORTUGAL': ":flag_pt:",
        'QATAR': ":flag_qa:",
        'ROMANIA': ":flag_ro:",
        'RUSSIA': ":flag_ru:",
        'RWANDA': ":flag_rw:",
        'SAINT KITTS AND NEVIS': ":flag_kn:",
        'SAINT LUCIA': ":flag_lc:",
        'SAINT VINCENT AND THE GRENADINES': ":flag_vc:",
        'SAMOA': ":flag_ws:",
        'SAN MARINO': ":flag_sm:",
        'SAO TOME AND PRINCIPE': ":flag_st:",
        'SAUDI ARABIA': ":flag_sa:",
        'SENEGAL': ":flag_sn:",
        'SERBIA': ":flag_rs:",
        'SEYCHELLES': ":flag_sc:",
        'SIERRA LEONE': ":flag_sl:",
        'SINGAPORE': ":flag_sg:",
        'SLOVAKIA': ":flag_sk:",
        'SLOVENIA': ":flag_si:",
        'SOLOMON ISLANDS': ":flag_sb:",
        'SOMALIA': ":flag_so:",
        'SOUTH AFRICA': ":flag_za:",
        'SOUTH SUDAN': ":flag_ss:",
        'SPAIN': ":flag_es:",
        'SRI LANKA': ":flag_lk:",
        'SUDAN': ":flag_sd:",
        'SURINAME': ":flag_sr:",
        'SWEDEN': ":flag_se:",
        'SWITZERLAND': ":flag_ch:",
        'SYRIA': ":flag_sy:",
        'TAIWAN': ":flag_tw:",
        'TAJIKISTAN': ":flag_tj:",
        'TANZANIA': ":flag_tz:",
        'THAILAND': ":flag_th:",
        'TOGO': ":flag_tg:",
        'TONGA': ":flag_to:",
        'TRINIDAD AND TOBAGO': ":flag_tt:",
        'TUNISIA': ":flag_tn:",
        'TURKEY': ":flag_tr:",
        'TURKMENISTAN': ":flag_tm:",
        'TUVALU': ":flag_tv:",
        'UGANDA': ":flag_ug:",
        'UKRAINE': ":flag_ua:",
        'UNITED ARAB EMIRATES': ":flag_ae:",
        'UNITED KINGDOM': ":flag_gb:",
        'UNITED STATES': ":flag_us:",
        'URUGUAY': ":flag_uy:",
        'UZBEKISTAN': ":flag_uz:",
        'VANUATU': ":flag_vu:",
        'VATICAN CITY': ":flag_va:",
        'VENEZUELA': ":flag_ve:",
        'VIETNAM': ":flag_vn:",
        'YEMEN': ":flag_ye:",
        'ZAMBIA': ":flag_zm:",
        'ZIMBABWE': ":flag_zw:",
        'AF': ":flag_af:",
        'AL': ":flag_al:",
        'DZ': ":flag_dz:",
        'AD': ":flag_ad:",
        'AO': ":flag_ao:",
        'AG': ":flag_ag:",
        'AR': ":flag_ar:",
        'AM': ":flag_am:",
        'AW': ":flag_aw:",
        'AU': ":flag_au:",
        'AT': ":flag_at:",
        'AZ': ":flag_az:",
        'BS': ":flag_bs:",
        'BH': ":flag_bh:",
        'BD': ":flag_bd:",
        'BB': ":flag_bb:",
        'BY': ":flag_by:",
        'BE': ":flag_be:",
        'BZ': ":flag_bz:",
        'BJ': ":flag_bj:",
        'BM': ":flag_bm:",
        'BT': ":flag_bt:",
        'BO': ":flag_bo:",
        'BA': ":flag_ba:",
        'BW': ":flag_bw:",
        'BR': ":flag_br:",
        'BN': ":flag_bn:",
        'BG': ":flag_bg:",
        'BF': ":flag_bf:",
        'BI': ":flag_bi:",
        'KH': ":flag_kh:",
        'CM': ":flag_cm:",
        'CA': ":flag_ca:",
        'CV': ":flag_cv:",
        'CF': ":flag_cf:",
        'TD': ":flag_td:",
        'CL': ":flag_cl:",
        'CN': ":flag_cn:",
        'CO': ":flag_co:",
        'KM': ":flag_km:",
        'CG': ":flag_cg:",
        'CK': ":flag_ck:",
        'CR': ":flag_cr:",
        'HR': ":flag_hr:",
        'CU': ":flag_cu:",
        'CY': ":flag_cy:",
        'CZ': ":flag_cz:",
        'CD': ":flag_cd:",
        'DK': ":flag_dk:",
        'DJ': ":flag_dj:",
        'DM': ":flag_dm:",
        'DO': ":flag_do:",
        'TL': ":flag_tl:",
        'EC': ":flag_ec:",
        'EG': ":flag_eg:",
        'SV': ":flag_sv:",
        'GQ': ":flag_gq:",
        'ER': ":flag_er:",
        'EE': ":flag_ee:",
        'SZ': ":flag_sz:",
        'ET': ":flag_et:",
        'FJ': ":flag_fj:",
        'FI': ":flag_fi:",
        'FR': ":flag_fr:",
        'GA': ":flag_ga:",
        'GM': ":flag_gm:",
        'GE': ":flag_ge:",
        'DE': ":flag_de:",
        'GH': ":flag_gh:",
        'GR': ":flag_gr:",
        'GD': ":flag_gd:",
        'GT': ":flag_gt:",
        'GN': ":flag_gn:",
        'GW': ":flag_gw:",
        'GY': ":flag_gy:",
        'HT': ":flag_ht:",
        'HN': ":flag_hn:",
        'HU': ":flag_hu:",
        'IS': ":flag_is:",
        'IN': ":flag_in:",
        'ID': ":flag_id:",
        'IR': ":flag_ir:",
        'IQ': ":flag_iq:",
        'IE': ":flag_ie:",
        'IL': ":flag_il:",
        'IT': ":flag_it:",
        'JM': ":flag_jm:",
        'JP': ":flag_jp:",
        'JO': ":flag_jo:",
        'KZ': ":flag_kz:",
        'KE': ":flag_ke:",
        'KI': ":flag_ki:",
        'KP': ":flag_kp:",
        'KR': ":flag_kr:",
        'XK': ":flag_xk:",
        'KW': ":flag_kw:",
        'KG': ":flag_kg:",
        'LA': ":flag_la:",
        'LV': ":flag_lv:",
        'LB': ":flag_lb:",
        'LS': ":flag_ls:",
        'LR': ":flag_lr:",
        'LY': ":flag_ly:",
        'LI': ":flag_li:",
        'LT': ":flag_lt:",
        'LU': ":flag_lu:",
        'MG': ":flag_mg:",
        'MW': ":flag_mw:",
        'MY': ":flag_my:",
        'MV': ":flag_mv:",
        'ML': ":flag_ml:",
        'MT': ":flag_mt:",
        'MH': ":flag_mh:",
        'MR': ":flag_mr:",
        'MU': ":flag_mu:",
        'MX': ":flag_mx:",
        'FM': ":flag_fm:",
        'MD': ":flag_md:",
        'MC': ":flag_mc:",
        'MN': ":flag_mn:",
        'ME': ":flag_me:",
        'MA': ":flag_ma:",
        'MZ': ":flag_mz:",
        'MM': ":flag_mm:",
        'NA': ":flag_na:",
        'NR': ":flag_nr:",
        'NP': ":flag_np:",
        'NL': ":flag_nl:",
        'NZ': ":flag_nz:",
        'NI': ":flag_ni:",
        'NE': ":flag_ne:",
        'NG': ":flag_ng:",
        'MK': ":flag_mk:",
        'NO': ":flag_no:",
        'OM': ":flag_om:",
        'PK': ":flag_pk:",
        'PW': ":flag_pw:",
        'PS': ":flag_ps:",
        'PA': ":flag_pa:",
        'PG': ":flag_pg:",
        'PY': ":flag_py:",
        'PE': ":flag_pe:",
        'PH': ":flag_ph:",
        'PL': ":flag_pl:",
        'PT': ":flag_pt:",
        'PR': ":flag_pt:",
        'QA': ":flag_qa:",
        'RO': ":flag_ro:",
        'RU': ":flag_ru:",
        'RW': ":flag_rw:",
        'KN': ":flag_kn:",
        'LC': ":flag_lc:",
        'VC': ":flag_vc:",
        'WS': ":flag_ws:",
        'SM': ":flag_sm:",
        'ST': ":flag_st:",
        'SA': ":flag_sa:",
        'SN': ":flag_sn:",
        'RS': ":flag_rs:",
        'SC': ":flag_sc:",
        'SL': ":flag_sl:",
        'SG': ":flag_sg:",
        'SK': ":flag_sk:",
        'SI': ":flag_si:",
        'SB': ":flag_sb:",
        'SO': ":flag_so:",
        'ZA': ":flag_za:",
        'SS': ":flag_ss:",
        'ES': ":flag_es:",
        'LK': ":flag_lk:",
        'SD': ":flag_sd:",
        'SR': ":flag_sr:",
        'SE': ":flag_se:",
        'CH': ":flag_ch:",
        'SY': ":flag_sy:",
        'TW': ":flag_tw:",
        'TJ': ":flag_tj:",
        'TZ': ":flag_tz:",
        'TH': ":flag_th:",
        'TG': ":flag_tg:",
        'TO': ":flag_to:",
        'TT': ":flag_tt:",
        'TN': ":flag_tn:",
        'TR': ":flag_tr:",
        'TM': ":flag_tm:",
        'TV': ":flag_tv:",
        'UG': ":flag_ug:",
        'UA': ":flag_ua:",
        'AE': ":flag_ae:",
        'UK': ":flag_gb:",
        'GB': ":flag_gb:",
        'US': ":flag_us:",
        'UY': ":flag_uy:",
        'UZ': ":flag_uz:",
        'VU': ":flag_vu:",
        'VA': ":flag_va:",
        'VE': ":flag_ve:",
        'VN': ":flag_vn:",
        'YE': ":flag_ye:",
        'ZM': ":flag_zm:",
        'ZW': ":flag_zw:"
    }


# JSON file paths
seasons_folder = "seasons_data"
current_season_file = "config.json"
profiles_file = "user_profiles.json"
games_played_file = "games_played.json"

# Load games played data
def load_games_played():
    try:
        with open(games_played_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Save games played data to JSON file
def save_games_played(games_played_data):
    with open(games_played_file, "w") as file:
        json.dump(games_played_data, file)

# Function to handle the "Join" button click




# Initialize the master leaderboard as a regular dictionary to hold all-time wins
master_leaderboard = {}

# Initialize the seasons dictionary to hold data for each season
seasons = {}
def load_kills_data():
    if os.path.exists("kills.json"):
        with open("kills.json", "r") as file:
            return json.load(file)
    return {}

# Function to save the kills data to the JSON file
def save_kills_data(kills_data):
    with open("kills.json", "w") as file:
        json.dump(kills_data, file)



def load_user_profiles():
    try:
        with open(profiles_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Save user profiles to JSON file
def save_user_profiles():
    with open(profiles_file, "w") as file:
        json.dump(user_profiles, file)


def load_1v1_wins():
    try:
        with open("1v1wins.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file is not found, return an empty dictionary
        return {}



def save_1v1_wins(data):
    with open("1v1wins.json", "w") as file:
        json.dump(data, file)



def load_master_leaderboard():
    return master_leaderboard


def load_season_leaderboard(season):
    try:
        with open(f"{seasons_folder}/{season}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}



def save_season_leaderboard(season):
    with open(f"{seasons_folder}/{season}.json", "w") as file:
        json.dump(seasons[season], file)



def load_current_season():
    try:
        with open(current_season_file, "r") as file:
            data = json.load(file)
            return data.get("current_season", None)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def get_total_wins(user_id):
    return sum(sum(seasons[season][user_id].values()) for season in seasons)



def add_wins(user_id, category, wins):
    seasons[current_season].setdefault(user_id, initialize_user_wins(user_id))
    seasons[current_season][user_id][category] += wins

def reset_wins(user_id, category):
    seasons[current_season].setdefault(user_id, initialize_user_wins(user_id))
    seasons[current_season][user_id][category] = 0

def remove_wins(user_id, category, wins):
    seasons[current_season].setdefault(user_id, initialize_user_wins(user_id))
    seasons[current_season][user_id][category] = max(0, seasons[current_season][user_id][category] - wins)

def initialize_user_wins(user_id):
    return {
        "solo": 0,
        "duo": 0,
        "trio": 0,
        "squad": 0,
    }

def update_master_leaderboard():
    global master_leaderboard
    master_leaderboard = {}

    # Loop through all files in the seasons_data folder
    for filename in os.listdir(seasons_folder):
        if filename.endswith(".json"):
            season_name = os.path.splitext(filename)[0]
            season_data = load_season_leaderboard(season_name)

            # Update the master leaderboard with the season's wins
            for user_id, user_data in season_data.items():
                if user_id not in master_leaderboard:
                    master_leaderboard[user_id] = initialize_user_wins(user_id)

                for category, wins in user_data.items():
                    master_leaderboard[user_id][category] += wins


def save_current_season(season):
    with open(current_season_file, "w") as file:
        json.dump({"current_season": season}, file)


                    

def get_medal_emoji(rank):
    medal_emojis = {
        1: "<:1stMedal:1135314244011831387> ",  
        2: "<:2ndMedal:1135314247442759814> ",  
        3: "<:3rdMedal:1135314249422491678> ",
    }

    return medal_emojis.get(rank, f"{rank}.")



log_channel_id = 1139925704570572872

class ErrorLogStream:
    def write(self, message):
        if "error" in message.lower():
            asyncio.ensure_future(self.send_message(message))

    async def send_message(self, message):
        if message.strip():  # Check if the message is not empty after stripping whitespace
            log_channel = bot.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(f"Error: {message}")
            else:
                print(f"Log channel with ID {log_channel_id} not found.")

sys.stderr = ErrorLogStream()

@bot.event
async def on_ready():
    print("Bot has logged in as {0.user}".format(bot))

    # Load the current season from the config file
    global current_season, league_standings, kills_data, one_v_one_wins_data,games_played
    kills_data = load_kills_data()
    games_played = load_games_played()
    one_v_one_wins_data = load_1v1_wins()
    current_season = load_current_season()
    # Load all seasons leaderboards from the JSON files in the seasons_data folder
    global seasons
    seasons = {} 

    global user_profiles
    user_profiles = load_user_profiles()

    for filename in os.listdir(seasons_folder):
        if filename.endswith(".json"):
            season_name = os.path.splitext(filename)[0]
            seasons[season_name] = load_season_leaderboard(season_name)
    await bot.tree.sync()

    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"Bot ID: {bot.user.id}")
    else:
        print(f"Log channel with ID {log_channel_id} not found.")
        
    # Rest of your on_ready code here

# Capture standard output
class LogStream:
    def write(self, message):
        asyncio.ensure_future(self.send_message(message))

    async def send_message(self, message):
        if message.strip():  # Check if the message is not empty after stripping whitespace
            log_channel = bot.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(message)
            else:
                print(f"Log channel with ID {log_channel_id} not found.")

sys.stdout = LogStream()


















@bot.tree.command(name="team-leaderboard", description="Displays the team leaderboard for the current season.")
async def team_leaderboard(Interaction: discord.Interaction):
    if not current_season or current_season not in seasons:
        await Interaction.response.send_message("No data available for the current season.")
        return

    # Create a dictionary to store the total wins for each user
    total_wins = {}

    # Calculate the total wins for each user by summing their wins from all seasons
    for season_data in seasons.values():
        for user_id, wins in season_data.items():
            total_wins[user_id] = total_wins.get(user_id, 0) + sum(wins.values())

    # Create a dictionary to store the total wins for each team
    team_wins = {}

    # Calculate the total wins for each team
    for user_id, wins in total_wins.items():
        user_profile = user_profiles.get(user_id)
        team = user_profile.get('team', 'Not assigned') if user_profile else ''

        # Update the total wins for the team
        team_wins[team] = team_wins.get(team, 0) + wins

    # Sort the teams based on their total wins
    sorted_teams = sorted(team_wins.items(), key=lambda item: item[1], reverse=True)

    # Create an embed to display the team leaderboard
    embed = discord.Embed(title=f"Team Leaderboard - Season {current_season}", color=0x00FF98)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.set_thumbnail(url="https://example.com/team_leaderboard_icon.png")  # Set the thumbnail URL if you have one

    for rank, (team, total_wins_team) in enumerate(sorted_teams, start=1):
        team_emoji = team_emojis.get(team, "")

        embed.add_field(name=f'**Rank {rank} | {team_emoji} {team}**',
                        value=f'Total Wins: **{total_wins_team}**',
                        inline=False)

    # Add the "Last Updated" timestamp in the footer of the embed
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    embed.set_footer(text=f"Last Updated: {current_time} UTC")

    await Interaction.response.defer()
    await Interaction.followup.send(embed=embed)

@bot.tree.command(name="1v1-leaderboard", description="Displays the leaderboard for 1v1 wins.")
async def v1_leaderboard(Interaction: discord.Interaction, page: int = None):
    items_per_page = 10
    sorted_users = sorted(one_v_one_wins_data.items(), key=lambda item: item[1], reverse=True)

    # Calculate the current page based on the user's position
    user_id = str(Interaction.user.id)
    user_position = next((i for i, (id, _) in enumerate(sorted_users) if id == user_id), -1)
    current_page = (user_position // items_per_page) + 1

    if page is None:
        page = current_page
    else:
        # Make sure the requested page is within bounds
        page = max(1, min(page, (len(sorted_users) - 1) // items_per_page + 1))

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    leaderboard_items = sorted_users[start_index:end_index]


    # Create an embed to display the leaderboard
    leaderboard_embed = discord.Embed(title=f"🤺 1V1 Leaderboard", color=0x00FF98)
    leaderboard_embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    leaderboard_embed.set_thumbnail(url="https://example.com/leaderboard_icon.png")  # Set the thumbnail URL if you have one

    medal_emojis = {
        1: "<:1stMedal:1135314244011831387> ",  # Gold medal
        2: "<:2ndMedal:1135314247442759814> ",  # Silver medal
        3: "<:3rdMedal:1135314249422491678> ",
    }


    for i, (user_id, wins_data) in enumerate(leaderboard_items, start=start_index + 1):
        user = await bot.fetch_user(int(user_id))
        medal = medal_emojis.get(i, "")

        user_profile = user_profiles.get(user_id)
        username = user_profile.get('ign', 'Not assigned') if user_profile else user.name
        country = user_profile.get('nationality', 'Not assigned') if user_profile else 'Not assigned'
        team = user_profile.get('team', 'Not assigned') if user_profile else 'Not assigned'
        team_emoji = team_emojis.get(team, "❌")
        country_flag = country_flags.get(country.upper(), "❌")

        # Retrieve the 1v1 wins for the user from the one_v_one_wins_data dictionary
        # one_v_one_wins_data contains the wins for all users, so we need to get the specific user's wins
        v1_wins = one_v_one_wins_data.get(user_id, 0)

        # Highlight the user who requested the message on the leaderboard in bold
        if i == user_position + 1:
            leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                        value=f'{country_flag} | {team_emoji} | **{username} | Wins: {v1_wins}**',
                                        inline=False)
        else:
            leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                        value=f'{country_flag} | {team_emoji} | {username} | Wins: {v1_wins}',
                                        inline=False)

    leaderboard_embed.set_footer(icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty, text=f"Your rank is #{user_position + 1} | Page {page}/{(len(sorted_users) - 1) // items_per_page + 1}")

    await Interaction.response.defer()
    await Interaction.followup.send(embed=leaderboard_embed)



@bot.tree.command(name="leaderboard", description="Displays the leaderboard for the current season.")
async def leaderboard(Interaction: discord.Interaction, page: int = None):
    if not current_season or current_season not in seasons:
        await Interaction.response.send_message("No data available for the current season.")
        return

    items_per_page = 10
    sorted_users = sorted(seasons[current_season].items(), key=lambda item: sum(item[1].values()), reverse=True)

    # Calculate the current page based on the user's position
    user_id = str(Interaction.user.id)

    if user_id not in seasons[current_season]:
        seasons[current_season][user_id] = {
            'solo': 0,
            'duo': 0,
            'trio': 0,
            'squad': 0,
        }

    user_position = next((i for i, (id, _) in enumerate(sorted_users) if id == user_id), -1)
    current_page = (user_position // items_per_page) + 1

    if page is None:
        page = current_page
    else:
        # Make sure the requested page is within bounds
        page = max(1, min(page, (len(sorted_users) - 1) // items_per_page + 1))

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    leaderboard_items = sorted_users[start_index:end_index]


    # Create an embed to display the leaderboard
    leaderboard_embed = discord.Embed(title=f"📊 Wins leaderboard - Season {current_season}", color=0x00FF98)
    leaderboard_embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    leaderboard_embed.set_thumbnail(url="https://example.com/leaderboard_icon.png")  # Set the thumbnail URL if you have one

    medal_emojis = {
        1: "<:1stMedal:1135314244011831387> ",  # Gold medal
        2: "<:2ndMedal:1135314247442759814> ",  # Silver medal
        3: "<:3rdMedal:1135314249422491678> ",
    }

    for i, (user_id, wins_dict) in enumerate(leaderboard_items, start=start_index + 1):
        user = await bot.fetch_user(int(user_id))
        medal = medal_emojis.get(i, "")

        user_profile = user_profiles.get(user_id)
        username = user_profile.get('ign', 'Not assigned') if user_profile else user.name
        country = user_profile.get('nationality', 'Not assigned') if user_profile else 'Not assigned'
        team = user_profile.get('team', 'Not assigned') if user_profile else 'Not assigned'
        team_emoji = team_emojis.get(team, "❌")
        country_flag = country_flags.get(country.upper(), "❌")

        # Get wins for each category (solo, duo, trio, squad, 1v1)
        solo_wins = wins_dict.get('solo', 0)
        duo_wins = wins_dict.get('duo', 0)
        trio_wins = wins_dict.get('trio', 0)
        squad_wins = wins_dict.get('squad', 0)
        total_wins = solo_wins+duo_wins+trio_wins+squad_wins
        # Highlight the user who requested the message on the leaderboard in bold
        if i == user_position + 1:
            leaderboard_embed.add_field(name=f'➡️ **Rank {i} {medal}**',
                                        value=f'**{country_flag} | {team_emoji} | {username} | Solo: {solo_wins} | Duo: {duo_wins} | Trio: {trio_wins} | Squad: {squad_wins} | Total: {total_wins}**',
                                        inline=False)
        else:
            leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                        value=f'{country_flag} | {team_emoji} | {username} | Solo: {solo_wins} | Duo: {duo_wins} | Trio: {trio_wins} | Squad: {squad_wins} | Total: {total_wins}',
                                        inline=False)

    leaderboard_embed.set_footer(icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty, text=f"Your rank is #{user_position + 1} | Page {page}/{(len(sorted_users) - 1) // items_per_page + 1}")

    # Edit the original "Please wait" message with the actual leaderboard data
    await Interaction.response.defer()
    await Interaction.followup.send(embed=leaderboard_embed)



@bot.tree.command(name="members", description="Displays members for a certain role.")
async def display_members_by_role(interaction: discord.Interaction, role: discord.Role):
    if not role:
        await interaction.response.send_message(f"Role '{role}' not found in the server.")
        return

    members_with_role = [member.mention for member in interaction.guild.members if role in member.roles]
    if not members_with_role:
        await interaction.response.send_message(f"No members have the role '{role.name}'.")
        return

    # Create an embed to display the members with the role
    embed = discord.Embed(title=f"Members with the '{role.name}' Role", color=0x00FF98)
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else discord.Embed.Empty)

    # Split the member list into chunks of 25 members (Discord's limit for a single field)
    for chunk in [members_with_role[i:i + 25] for i in range(0, len(members_with_role), 25)]:
        members_text = "\n".join(chunk)
        embed.add_field(name="\u200B", value=members_text, inline=False)

    await interaction.response.send_message(embed=embed)


# Helper function to sum wins for a specific category from all seasons
def sum_wins_for_category(user_id, category):
    total_wins = 0
    for season in seasons.values():
        user_data = season.get(user_id)
        if user_data:
            total_wins += user_data.get(category, 0)
    return total_wins

@bot.tree.command(name="master-leaderboard", description="Displays the master leaderboard with all-time wins.")
async def master_leaderboard(Interaction: discord.Interaction, page: int = None):
    update_master_leaderboard()

    server = Interaction.guild
    members = server.members
    members_dict = {str(member.id): member for member in members}
    items_per_page = 10
    sorted_users = sorted(master_leaderboard.items(), key=lambda item: sum(item[1].values()), reverse=True)
    # Calculate the current page based on the user's position
    user_id = str(Interaction.user.id)
    user_position = next((i for i, (id, _) in enumerate(sorted_users) if id == user_id), -1)
    current_page = (user_position // items_per_page) + 1

    if page is None:
        page = current_page
    else:
        # Make sure the requested page is within bounds
        page = max(1, min(page, (len(sorted_users) - 1) // items_per_page + 1))

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    leaderboard_items = sorted_users[start_index:end_index]


    # Create an embed to display the master leaderboard
    leaderboard_embed = discord.Embed(title="📊 Master Leaderboard - All-Time Wins", color=0x00FF98)
    leaderboard_embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    leaderboard_embed.set_thumbnail(url="https://example.com/master_leaderboard_icon.png")  # Set the thumbnail URL if you have one

    medal_emojis = {
        1: "<:1stMedal:1135314244011831387> ",  # Gold medal
        2: "<:2ndMedal:1135314247442759814> ",  # Silver medal
        3: "<:3rdMedal:1135314249422491678> ",
    }

    for i, (user_id, user_data) in enumerate(leaderboard_items, start=start_index + 1):
        user = members_dict.get(user_id)
        if user:
            medal = medal_emojis.get(i, "")
            user_profile = user_profiles.get(user_id)
            username = user_profile.get('ign', 'Not assigned') if user_profile else user.name
            team = user_profile.get('team', 'Not assigned') if user_profile else 'Not assigned'
            country = user_profile.get('nationality', 'Not assigned') if user_profile else 'Not assigned'

            team_emoji = team_emojis.get(team, "❌")
            country_flag = country_flags.get(country.upper(), "❌")

            # Calculate total wins for each user
            total_wins = 0
            wins_text = ""
            for category, wins in user_data.items():
                wins_text += f"{category.title()}: {wins} | "
                total_wins += wins

            # Highlight the user who requested the message on the leaderboard in bold
            if i == user_position + 1:
                leaderboard_embed.add_field(name=f'➡️ **Rank {i} {medal}**',
                                            value=f'{country_flag} | {team_emoji} | **{username} | {wins_text[:-3]} | Total: {total_wins}**',
                                            inline=False)
            else:
                leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                            value=f'{country_flag} | {team_emoji} | {username} | {wins_text[:-3]} | Total: {total_wins}',
                                            inline=False)
        else:
            # User not found in members list (probably a user who left the server)
            user = await bot.fetch_user(int(user_id))
            username = user.name
            # Calculate total wins for each user
            total_wins = 0
            wins_text = ""
            for category, wins in user_data.items():
                wins_text += f"{category.title()}: {wins} | "
                total_wins += wins

            leaderboard_embed.add_field(name=f'**Rank {i}**',
                                        value=f'Not in server | {wins_text[:-3]} | User: {username} | Total: {total_wins}',
                                        inline=False)


    leaderboard_embed.set_footer(icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty, text=f"Your rank is #{user_position + 1} | Page {page}/{(len(sorted_users) - 1) // items_per_page + 1}")

    await Interaction.response.defer()
    await Interaction.followup.send(embed=leaderboard_embed)







@bot.tree.command(name="create-season", description="Creates a new season and switches to another empty seasonal leaderboard.")
@commands.is_owner()
async def create_season(Interaction: discord.Interaction, season_name: str):
    global current_season

    # Check if the season name is valid and not existing
    if not re.match(r'^[a-zA-Z0-9_]+$', season_name):
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        embed.add_field(name="", value=f"Invalid season name. The season name can only contain letters, numbers, and underscores.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    if season_name in seasons:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        embed.add_field(name="", value=f"A season with that name exists already!", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    # Save the current season leaderboard to a separate file if current_season is not None
    if current_season:
        save_season_leaderboard(current_season)

    # Create a new leaderboard for the new season
    seasons[season_name] = {}
    save_season_leaderboard(season_name)

    # Update the current season variable
    current_season = season_name
    save_current_season(current_season)  # Save the updated current_season to the config.json file

    # Switch to another empty JSON file for the seasonal leaderboard
    seasonal_leaderboard_file = f"{seasons_folder}/{season_name}.json"
    if not os.path.exists(seasonal_leaderboard_file):
        with open(seasonal_leaderboard_file, "w") as file:
            json.dump({}, file)

    # Update the master leaderboard with all-time wins
    update_master_leaderboard()

    embed=discord.Embed(title="Season created!", color=0x00FF00)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.add_field(name="", value=f"The new season '{season_name}' has been created, old season's leaderboards still remain in the database.", inline=True)
    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="reset-season", description="Resets the current season leaderboard.")
@commands.is_owner()
async def reset_season(Interaction: discord.Interaction):
    seasons[current_season] = {}
    save_season_leaderboard(current_season)

    # Update the master leaderboard with all-time wins
    update_master_leaderboard()

    embed=discord.Embed(title="Leaderboard reset", color=0x00FF00)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.add_field(name="", value=f"The current season's leaderboard has been reset.", inline=True)
    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="winsadd", description="Add wins to the current season's leaderboard for a specific user. Defaults to your own wins.")
async def winsadd(Interaction: discord.Interaction, wins: int, category: str, user: discord.User = None):
    if not current_season or current_season not in seasons:
        embed = discord.Embed(title="❌ Error", description="No data available for the current season.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return

    # Use the invoking user if no user is specified
    user = user or Interaction.user
    user_id = str(user.id)

    if category.lower() == "1v1":
        # Load 1v1 wins data from the JSON file

        # Update the 1v1 wins for the user
        one_v_one_wins_data[user_id] = one_v_one_wins_data.get(user_id, 0) + wins

        # Save the updated 1v1 wins data to the JSON file
        save_1v1_wins(one_v_one_wins_data)

    elif category.lower() in ["solo", "duo", "trio", "squad"]:
        # Add the specified number of wins to the user's entry in the current season's leaderboard
        add_wins(user_id, category.lower(), wins)

        # Save the updated season leaderboard to the JSON file
        save_season_leaderboard(current_season)

    else:
        embed = discord.Embed(title="❌ Error", description="Invalid category. Valid categories are: solo, duo, trio, squad and 1v1.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(title=f"✅ Wins Added **{category}**", description=f"{wins} wins have been added to {user.mention}'s leaderboard entry for {category} category in the current season.", color=0x00FF00)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="winsremove", description="Remove wins from the current season's leaderboard for a specific user. Defaults to your own wins.")
async def winsremove(Interaction: discord.Interaction, wins: int, category: str, user: discord.User = None):
    if not current_season or current_season not in seasons:
        embed = discord.Embed(title="❌ Error", description="No data available for the current season.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return

    # Use the invoking user if no user is specified
    user = user or Interaction.user
    user_id = str(user.id)

    if category.lower() == "1v1":
        # Load 1v1 wins data from the JSON file

        # Get the current 1v1 wins for the user (defaults to 0 if the user has no 1v1 wins)
        current_one_v_one_wins = one_v_one_wins_data.get(user_id, 0)

        if current_one_v_one_wins < wins:
            embed = discord.Embed(title="❌ Error", description=f"{user.mention} has only {current_one_v_one_wins} 1v1 wins. Cannot remove {wins} wins.", color=0xFF0000)
            embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
            await Interaction.response.send_message(embed=embed)
            return

        # Update the 1v1 wins for the user
        one_v_one_wins_data[user_id] = current_one_v_one_wins - wins

        # Save the updated 1v1 wins data to the JSON file
        save_1v1_wins(one_v_one_wins_data)

    elif category.lower() in ["solo", "duo", "trio", "squad"]:
        # Get the current wins for the user in the specified category (defaults to 0 if the user has no wins in that category)
        current_wins = seasons[current_season].get(user_id, {}).get(category.lower(), 0)

        if current_wins < wins:
            embed = discord.Embed(title="❌ Error", description=f"{user.mention} has only {current_wins} wins in the {category} category. Cannot remove {wins} wins.", color=0xFF0000)
            embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
            await Interaction.response.send_message(embed=embed)
            return

        # Remove the specified number of wins from the user's entry for the specified category in the current season's leaderboard
        remove_wins(user_id, category.lower(), wins)

        # Save the updated season leaderboard to the JSON file
        save_season_leaderboard(current_season)

    else:
        embed = discord.Embed(title="❌ Error", description="Invalid category. Valid categories are: solo, duo, trio, squad and 1v1.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(title=f"✅ Wins Removed **{category}**", description=f"{wins} wins have been removed from {user.mention}'s leaderboard entry for {category} category in the current season.", color=0x00FF00)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    await Interaction.response.send_message(embed=embed)



@bot.tree.command(name="winsreset", description="Reset wins for the current season's leaderboard for a specific user. Defaults to your own wins.")
async def winsreset(Interaction: discord.Interaction, category: str, user: discord.User = None):
    if not current_season or current_season not in seasons:
        embed = discord.Embed(title="Error", description="No data available for the current season.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return
    
    # Use the invoking user if no user is specified
    user = user or Interaction.user
    user_id = str(user.id)
    
    if category.lower() == "1v1":
        # Load 1v1 wins data from the JSON file

        # Reset the user's 1v1 wins to 0
        one_v_one_wins_data[user_id] = 0

        # Save the updated 1v1 wins data to the JSON file
        save_1v1_wins(one_v_one_wins_data)

    elif category.lower() in ["solo", "duo", "trio", "squad"]:
        # Reset the user's wins for the specified category in the current season's leaderboard
        reset_wins(user_id, category.lower())

        # Save the updated season leaderboard to the JSON file
        save_season_leaderboard(current_season)

    else:
        embed = discord.Embed(title="❌ Error", description="Invalid category. Valid categories are: solo, duo, trio, squad and 1v1.", color=0xFF0000)
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        await Interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(title=f"✅ Wins Reset **{category}**", description=f"{user.mention}'s wins have been reset to 0 for {category} category in the current season.", color=0x00FF00)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    await Interaction.response.send_message(embed=embed)






@bot.tree.command(name="profile", description="Display the user's profile information.")
async def profile(Interaction: discord.Interaction, user: discord.User = None):
    update_master_leaderboard()

    if user is None:
        user = Interaction.user

    user_id = str(user.id)
    user_profile = user_profiles.get(user_id)

    if not user_profile or 'ign' not in user_profile or 'nationality' not in user_profile or 'team' not in user_profile:
        embed = discord.Embed(title=f"{user.name}'s Profile", color=0xFF0000, description="***❌ You must setup your profile in order to view your wins.***")  # Set embed color to red
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        else:
            pass
        embed.set_footer(text="💬 Do /profilesetup.")
    else:
        ign = user_profile.get('ign', 'Not assigned')
        nationality = user_profile.get('nationality', 'Not assigned')
        team = user_profile.get('team', 'Not assigned')
        team_emoji = team_emojis.get(team, "")
        country_flag = country_flags.get(nationality.upper(), "")

        sorted_season_users = sorted(seasons[current_season].items(), key=lambda item: sum(item[1].get(category, 0) for category in ["solo", "duo", "trio", "squad"]), reverse=True)
        seasonal_rank = next((i + 1 for i, (id, _) in enumerate(sorted_season_users) if id == user_id), None)

        embed = discord.Embed(title=f"🤺 {user.name}'s Profile", color=0x00FF98)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        else:
            pass
        embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
        embed.add_field(name="IGN", value=ign, inline=True)
        embed.add_field(name="Nationality", value=f"{country_flag}", inline=True)
        embed.add_field(name="Team", value=f"{team_emoji} {team}", inline=True)
        embed.add_field(name="Seasonal Rank", value=f"{seasonal_rank}/{len(sorted_season_users)}", inline=True)

        solo_wins = seasons[current_season].get(user_id, {}).get('solo', 0)
        duo_wins = seasons[current_season].get(user_id, {}).get('duo', 0)
        trio_wins = seasons[current_season].get(user_id, {}).get('trio', 0)
        squad_wins = seasons[current_season].get(user_id, {}).get('squad', 0)
        v1_wins = one_v_one_wins_data.get(user_id, 0)

        total_wins = solo_wins + duo_wins + trio_wins + squad_wins

        games_played = load_games_played()
        games_played_count = games_played.get(user_id, 0)
        
        # Calculate winrate
        winrate = int(total_wins / games_played_count * 100) if games_played_count != 0 else 0

        embed.add_field(name="Solo Wins", value=solo_wins, inline=True)
        embed.add_field(name="Duo Wins", value=duo_wins, inline=True)
        embed.add_field(name="Trio Wins", value=trio_wins, inline=True)
        embed.add_field(name="Squad Wins", value=squad_wins, inline=True)
        embed.add_field(name="1v1 Wins", value=v1_wins, inline=True)

        if Interaction.user == user or Interaction.user.id == 762757288598437889:
            embed.add_field(name="Winrate", value=f"{winrate}%", inline=True)
            embed.add_field(name="Games played", value=games_played_count, inline=True)
        else:
            embed.add_field(name="Winrate", value="**Hidden**", inline=True)
            embed.add_field(name="Games played", value="**Hidden**", inline=True)

        embed.add_field(name="Total wins (excluding 1v1)", value=total_wins, inline=True)

        embed.set_footer(icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty, text=f"Requested by {user} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    await Interaction.response.send_message(embed=embed, ephemeral=True)







@bot.tree.command(name="profilesetup", description="Setup your server profile")
async def profilesetup(Interaction: discord.Interaction):
    user_id = str(Interaction.user.id)
    user_profile = user_profiles.get(user_id, {})

    if "nationality" in user_profile and "ign" in user_profile and "team" in user_profile:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value="❌ Your profile is already complete.", inline=True)
        await Interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value="✉️ I have sent you a DM. Please check your messages.", inline=True)
    await Interaction.response.send_message(embed=embed, ephemeral=True)

    dm_channel = await Interaction.user.create_dm()
 
    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="🌍 Nationality", value="What is your nationality (Two-Letter country code)?", inline=False)
    embed.add_field(name="", value="Ex: UK, US, United States, United Kingdom (DONT USE EMOJIS)", inline=False)
    await dm_channel.send(embed=embed)

    try:
        nationality_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        nationality = nationality_msg.content
        user_profile["nationality"] = nationality
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0x00FF98)
        embed.add_field(name="⏱️ Timeout", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    embed = discord.Embed(color=0x00FF98)
    embed.add_field(name="🔥 IGN", value="What is your Blast Royale IGN (in-game name)?", inline=False)
    await dm_channel.send(embed=embed)

    try:
        ign_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        ign = ign_msg.content
        user_profile["ign"] = ign
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0x00FF98)
        embed.add_field(name="⏱️ Timeout", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="🚀 Team", value="What Blast Royale team do you associate with (REVBOUNTY, EX, UNTB, VALOR, RXSPECT)?\nType 'none' for no team affiliation.", inline=False)
    await dm_channel.send(embed=embed)

    try:
        team_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        team = team_msg.content.upper()
        if team == "NONE":
            user_profile["team"] = "None"
        elif team not in ["REVBOUNTY", "EX", "VALOR", "UNTB", "RXSPECT"]:
            embed = discord.Embed(color=0x00FF98)
            embed.add_field(name="❌ Invalid Team", value="Invalid team name. Available teams: REVBOUNTY, EX, UNTB, VALOR, RXSPECT\nType 'none' for no team affiliation.", inline=True)
            await dm_channel.send(embed=embed)
            return
        else:
            user_profile["team"] = team
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="⏱️ Timeout", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    user_profiles[user_id] = user_profile
    save_user_profiles()

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value="✅ Profile setup complete!", inline=True)
    await dm_channel.send(embed=embed)




@bot.tree.command(name="resetprofile", description="Reset your server profile")
async def resetprofile(Interaction: discord.Interaction):
    user_id = str(Interaction.user.id)
    user_profile = user_profiles.get(user_id)

    if not user_profile:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value=f"⁉️⁉️ Your profile is not set. There's nothing to reset.", inline=True)
        await Interaction.response.send_message(embed=embed,ephemeral=True)
        return

    user_profiles.pop(user_id)
    save_user_profiles()

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value=f"✅ Your profile has been reset. You can run the profile setup command again to set up a new profile.", inline=True)
    await Interaction.response.send_message(embed=embed,ephemeral=True)

@bot.tree.command(name="stopbot", description="Stops the bot")
@commands.is_owner()
async def stopbot(Interaction: discord.Interaction):
    await Interaction.response.send_message("Stopping the bot..‼️")
    await bot.close()


@bot.tree.command(name="ping",description="bot ping")
async def ping(Interaction: discord.Interaction):
    latency = bot.latency
    embed = discord.Embed(title="Pong! 🏓", description=f"Latency: {latency * 1000:.2f} ms", color=discord.Color.green())
    await Interaction.response.send_message(embed=embed)

BOT_OWNER_ID = 762757288598437889

@bot.command()
async def sendmsg(ctx, channel_id: int, *, msg: str):
    # Check if the command is being used in DMs
    if not isinstance(ctx.channel, discord.DMChannel):
        return await ctx.send("This command can only be used in DMs.")

    # Check if the command is being used by the bot owner
    if ctx.author.id != BOT_OWNER_ID:
        return await ctx.send("You are not authorized to use this command.")

    try:
        # Fetch the specified channel
        channel = bot.get_channel(channel_id)

        if channel is None:
            return await ctx.send("Invalid channel ID. Make sure the bot has access to the channel.")

        # Send the message to the specified channel
        await channel.send(msg)
        await ctx.send(f"Message sent to channel {channel.mention} successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


team_roles = {
    1133089484934754305: "The Raptors",
    1133091395909984306: "SPARTA",
    1133090521473097838: "Destined2Rise",
    1133090620207017984: "Galaxy Collapse",
    1133089136778162306: "The Saints",
    1133088758103810059: "Enigma Squad",
    1133089334820605965: "Team Elegance",
    1133089686584311930: "Velocity Squad"
}


@bot.tree.command(name="addkill", description="Add kills for a user")
async def add_kill(Interaction: discord.Interaction, kills: int, target_user: discord.User):
    user_id = str(target_user.id)

    # Update the kills for the target user
    kills_data[user_id] = kills_data.get(user_id, 0) + kills

    # Save the updated kills data
    save_kills_data(kills_data)

    embed = discord.Embed(color=discord.Color.green())
    embed.description = f"✅ {kills} kills have been added to {target_user.mention}'s total kills. Their total kills: {kills_data[user_id]}"
    await Interaction.response.send_message(embed=embed)


@bot.command()
@commands.is_owner()
async def send_data(ctx):
    MAX_MESSAGE_LENGTH = 1024
    
    # Load data from the JSON file for the current season
    current_season_data = load_season_leaderboard(current_season)

    # Convert data to JSON format with indentation
    current_season_json = json.dumps(current_season_data, indent=4)

    # Split the JSON data into chunks to fit within the Discord message limit
    current_season_chunks = [current_season_json[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(current_season_json), MAX_MESSAGE_LENGTH)]

    # Send each chunk in a separate message
    for chunk in current_season_chunks:
        await ctx.send(f"```json\n{chunk}\n```")


@bot.tree.command(name="removekill", description="Remove kills from the current user")
async def remove_kill(Interaction: discord.Interaction, kills: int):
    user_id = str(Interaction.user.id)

    current_kills = kills_data.get(user_id, 0)
    if current_kills < kills:
        embed = discord.Embed(color=discord.Color.red())
        embed.description = f"⁉️❌ You cannot remove more kills than you currently have."
        await Interaction.response.send_message(embed=embed)
        return

    # Update the kills for the current user
    kills_data[user_id] -= kills

    # Save the updated kills data
    save_kills_data(kills_data)

    embed = discord.Embed(color=discord.Color.green())
    embed.description = f"✅ {kills} kills have been removed. Your total kills: {kills_data[user_id]}"
    await Interaction.response.send_message(embed=embed)

    

@bot.tree.command(name="kill-leaderboard", description="Displays the kill leaderboard for the current season.")
async def kill_leaderboard(Interaction: discord.Interaction, page: int = None):
    items_per_page = 10
    sorted_users = sorted(kills_data.items(), key=lambda item: item[1], reverse=True)

    user_id = str(Interaction.user.id)
    if user_id not in kills_data:
        kills_data[user_id] = 0

    sorted_users = sorted(kills_data.items(), key=lambda item: item[1], reverse=True)

    user_position = next((i for i, (id, _) in enumerate(sorted_users) if id == user_id), -1)
    current_page = (user_position // items_per_page) + 1

    if page is None or page < 1 or page > (len(sorted_users) - 1) // items_per_page + 1:
        page = 1

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    leaderboard_items = sorted_users[start_index:end_index]


    # Create an embed to display the leaderboard
    leaderboard_embed = discord.Embed(title=f"⚔️ Kill Leaderboard - Season {current_season}", color=0x00FF98)
    leaderboard_embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    leaderboard_embed.set_thumbnail(url="https://example.com/leaderboard_icon.png")  # Set the thumbnail URL if you have one

    medal_emojis = {
        1: "<:1stMedal:1135314244011831387> ",  # Gold medal
        2: "<:2ndMedal:1135314247442759814> ",  # Silver medal
        3: "<:3rdMedal:1135314249422491678> ",
    }

    for i, (user_id, kills) in enumerate(leaderboard_items, start=start_index + 1):
        # Check if the user is still a member of the server
        member = Interaction.guild.get_member(int(user_id))
        if not member:  # Skip users who have left the server
            continue

        user = member  # Use the member as the user object

        medal = medal_emojis.get(i, "")

        # Get additional user profile data from the kills_data and user_profiles dictionaries if available
        username = user.name
        team = "Not assigned"
        user_profile = user_profiles.get(user_id)
        if user:
            medal = medal_emojis.get(i, "")
            user_profile = user_profiles.get(user_id)
            username = user_profile.get('ign', 'Not assigned') if user_profile else user.name
            team_role = next((role_id for role_id, teamname in team_roles.items() if role_id in [role.id for role in member.roles]), None)
            team = team_roles.get(team_role, "Not assigned")
            country = user_profile.get('nationality', 'Not assigned') if user_profile else 'Not assigned'
            country_flag = country_flags.get(country.upper(), "❌")


        # Highlight the user who requested the message on the leaderboard in bold
        if i == user_position + 1:
            leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                        value=f'{country_flag} **{username} | Kills: {kills} | Team: {team}**',
                                        inline=False)
        else:
            leaderboard_embed.add_field(name=f'**Rank {i} {medal}**',
                                        value=f'{country_flag} {username} | Kills: {kills} | Team: {team}',
                                        inline=False)

    leaderboard_embed.set_footer(icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty, text=f"Your rank is #{user_position + 1} | Page {page}/{(len(sorted_users) - 1) // items_per_page + 1}")

    await Interaction.response.defer()
    await Interaction.followup.send(embed=leaderboard_embed)

@bot.tree.command(name="gamesadd", description="Add games to the games played count for a specific user. Defaults to yourself.")
async def gamesadd(Interaction: discord.Interaction, games: int, user: discord.User = None):
    user_id = str(user.id) if user else str(Interaction.user.id)  # Convert user ID to string
    games_played_data = load_games_played()  # Load the data at the beginning

    if user and user_id not in games_played_data:
        embed = discord.Embed(color=discord.Color.red())
        embed.description = f"❌ User has no games played."
        await Interaction.response.send_message(embed=embed)
        return

    if user_id not in games_played_data:
        games_played_data[user_id] = 0

    games_played_data[user_id] += games
    save_games_played(games_played_data)

    user_mention = user.mention if user else "your"
    embed = discord.Embed(color=discord.Color.green())
    embed.description = f"✅ {games} games have been added to {user_mention} games played count."
    await Interaction.response.send_message(embed=embed)

@bot.tree.command(name="gamesremove", description="Remove games from the games played count for a specific user. Defaults to yourself.")
async def gamesremove(Interaction: discord.Interaction, games: int, user: discord.User = None):
    user_id = str(user.id) if user else str(Interaction.user.id)  # Convert user ID to string
    games_played_data = load_games_played()  # Load the data at the beginning

    if user and user_id not in games_played_data:
        embed = discord.Embed(color=discord.Color.red())
        embed.description = f"❌ User has no games played."
        await Interaction.response.send_message(embed=embed)
        return

    if user_id not in games_played_data:
        games_played_data[user_id] = 0

    if games_played_data[user_id] < games:
        embed = discord.Embed(color=discord.Color.red())
        embed.description = f"❌ User doesn't have enough games played to remove that many."
        await Interaction.response.send_message(embed=embed)
        return

    games_played_data[user_id] -= games
    save_games_played(games_played_data)

    user_mention = user.mention if user else "your"
    embed = discord.Embed(color=discord.Color.green())
    embed.description = f"✅ {games} games have been removed from {user_mention} games played count."
    await Interaction.response.send_message(embed=embed)



joined_users = {}

class JoinButton(discord.ui.Button):
    def __init__(self, user_id, scrim_code, label="Join", style=discord.ButtonStyle.green):
        super().__init__(style=style, label=label)
        self.user_id = user_id
        self.scrim_code = scrim_code

    async def callback(self, interaction: discord.Interaction):
        global joined_users
        if self.scrim_code not in joined_users:
            joined_users[self.scrim_code] = []
        
        original_author_id = int(self.user_id)
        joining_user_id = interaction.user.id

        
        if joining_user_id == original_author_id:
            await interaction.response.send_message("❌ You're the host, you're already in!", ephemeral=True)
            return

        if joining_user_id in joined_users[self.scrim_code]:
            await interaction.response.send_message("❌ You have already joined the game.", ephemeral=True)
        else:
            joined_users[self.scrim_code].append(joining_user_id)
            
            games_played_data = load_games_played()

            user_id_str = str(joining_user_id)
            if user_id_str not in games_played_data:
                games_played_data[user_id_str] = 0
            games_played_data[user_id_str] += 1
            save_games_played(games_played_data)

            user = await bot.fetch_user(joining_user_id)
            embed = discord.Embed(title="✅ You have joined! Here's your code.", color=discord.Color.green())
            embed.add_field(name="Code:", value=f"**{self.scrim_code}**")
            await user.send(embed=embed)
            
            channel = bot.get_channel(1137461518657658932)
            await channel.send(f"➡️ **{interaction.user.display_name}** has joined")

            # Send the interaction response only once after processing
            await interaction.response.send_message("✅ You joined the game! Check your DMs for the code.", ephemeral=True)




@bot.event
async def on_message(message):
    global seasons
    if message.channel.id == 1085298584192286730:
        # Check if the message contains a 6-digit number (scrim code)
        if any(word.isdigit() and len(word) == 6 for word in message.content.split()):
            # Delete the original message
            
            await message.delete()
            await message.channel.send("@here")
            channel = bot.get_channel(1137461518657658932)
            await channel.send(f"-------------------------------------------------")
            await channel.send(f"➡️A new scrim has been hosted by {message.author}!⬅️")
            # Split the message content to extract the scrim code and other details
            parts = message.content.split()
            scrim_code = next((word for word in parts if word.isdigit() and len(word) == 6), None)
            team = parts[parts.index(scrim_code) + 1]
            mode = " ".join(parts[parts.index(team) + 1:])


            games_played_data = load_games_played()
            str_author = str(message.author.id)
            if str_author not in games_played_data:
                games_played_data[str_author] = 0
            games_played_data[str_author] += 1
            save_games_played(games_played_data)
            # Create and send the embed with the JoinButton
            embed = discord.Embed(title="Scrim Details", description="Press join to get the code in DMs", color=0x00FF98)
            embed.set_author(name=message.guild.name, icon_url=message.guild.icon.url if message.guild.icon else discord.Embed.Empty)

            embed.add_field(name="Team", value=team)
            embed.add_field(name="Mode", value=mode)
            embed.set_footer(text=f"Scrim Host: {message.author} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Create the JoinButton for the message author
            join_button = JoinButton(user_id=str(message.author.id), scrim_code=scrim_code)
            view = View(timeout=100)
            view.add_item(join_button)

            # Send the embed with the JoinButton
            await message.channel.send(embed=embed, view=view)

        await bot.process_commands(message)

        if message.mentions:
            mentioned_players = ", ".join(member.mention for member in message.mentions)

            current_season = load_current_season()
            if not current_season or current_season not in seasons:
                await message.channel.send("No data available for the current season.")
                return

            for member in message.mentions:
                user_id = str(member.id)

                if current_season not in seasons:
                    seasons[current_season] = {}  
                if user_id not in seasons[current_season]:
                    seasons[current_season][user_id] = initialize_user_wins(user_id)

                num_mentions = len(message.mentions)
                if num_mentions == 1:
                    category = "solo"
                elif num_mentions == 2:
                    category = "duo"
                elif num_mentions == 3:
                    category = "trio"
                elif num_mentions == 4:
                    category = "squad"
                else:
                    await message.channel.send("Invalid number of mentions. Wins can only be added for solo, duo, trio, or squad.")
                    return

                # Increment the win count for the specified category for the player
                seasons[current_season][user_id][category] += 1

            # Save the updated season leaderboard to the JSON file
            save_season_leaderboard(current_season)

            # Delete the original mentions message
            await message.delete()

            # Create and send the wins added embed
            wins_added_embed = discord.Embed(title="Scrim Winner(s)", color=0x00FF98)
            wins_added_embed.add_field(name="Player(s)", value=mentioned_players)
            wins_added_embed.set_footer(text=f"Wins have been added. Thank you for joining us! | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await message.channel.send(embed=wins_added_embed)

    await bot.process_commands(message)

    if message.channel.id == 1136772447832645661:
        parts = message.content.split()
        if len(parts) >= 2 and parts[0].isdigit() and len(parts[0]) == 6:
            code = parts[0]
            mode = " ".join(parts[1:])
            await message.delete()
            creator = message.author
            view = discord.ui.View(timeout=100)

            claimed_by = None

            async def accept_button_callback(interaction: discord.Interaction):
                nonlocal claimed_by

                if claimed_by is None and interaction.user != creator:
                    
                    claimed_by = interaction.user.name
                    await interaction.response.send_message("The code has been sent to your DMs", ephemeral=True)
                    
                    embed = discord.Embed(title="1v1 Request Claimed",
                                          color=discord.Color.green())
                    embed.add_field(name="Code:",value=f"**{code}**")
                    await interaction.user.send(embed=embed)
                    accept_button.disabled = True
                    
                    embed.set_field_at(0, name="Status", value=f"Claimed by {claimed_by}")
                    embed.color = discord.Color.red()
                    await msg.edit(embed=embed, view=view)
                elif interaction.user == creator:
                    # The original message sender can't accept their own 1v1 request
                    await interaction.response.send_message("You can't accept your own 1v1 request.", ephemeral=True)
                else:
                    # The 1v1 request has already been claimed by someone else
                    await interaction.response.send_message("Someone already claimed it.", ephemeral=True)

            # Add the accept button to the view
            accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept_1v1")
            accept_button.callback = accept_button_callback
            view.add_item(accept_button)

            # Create the initial embed with "OPEN" status
            embed = discord.Embed(title="1v1 Request", description=f"1v1 Creator: {creator.mention}", color=0x00FF98)
            embed.set_author(name=message.guild.name, icon_url=message.guild.icon.url if message.guild.icon else discord.Embed.Empty)
            embed.add_field(name="Status", value="OPEN")
            embed.add_field(name="Mode", value="1V1")
            embed.add_field(name="Server", value=mode)
            embed.set_footer(text=f"1v1 Request Created at {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

            # Send the embed with the view containing the accept button
            msg = await message.channel.send(embed=embed, view=view)

    await bot.process_commands(message)

@bot.event
async def on_button_click(interaction: discord.Interaction):
    await bot.process_commands(interaction)






bot.run('MTEyODI2MjczNjE2NjUzNTE5OQ.GinAIO.nUvcOutUkQWzC-6SWqYt8i3TBKU3kNnigMwM8w')