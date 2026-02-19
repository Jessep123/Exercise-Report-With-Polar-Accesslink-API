import streamlit as st
import pandas as pd

polar_sport_mapping = {
    "AEROBICS": "Aerobics",
    "AGILITY": "Dog agility",
    "AMERICAN_FOOTBALL": "Football",
    "AQUATICS": "Aqua fitness",
    "BACKCOUNTRY_SKIING": "Backcountry skiing",
    "BADMINTON": "Badminton",
    "BALLET_DANCING": "Ballet",
    "BALLROOM_DANCING": "Ballroom",
    "BASEBALL": "Baseball",
    "BASKETBALL": "Basketball",
    "BEACH_TENNIS": "Beach tennis",
    "BEACH_VOLLEYBALL": "Beach volley",
    "BIATHLON": "Biathlon",
    "BODY_AND_MIND": "Body&Mind",
    "BOOTCAMP": "Bootcamp",
    "BOXING": "Boxing",
    "CALISTHENICS": "Calisthenics",
    "CIRCUIT_TRAINING": "Circuit training",
    "CORE": "Core",
    "CRICKET": "Cricket",
    "CROSS_TRAINER": "Cross-trainer",
    "CROSS_COUNTRY_RUNNING": "Cross-country running",
    "CROSS-COUNTRY_SKIING": "Skiing",
    "CYCLING": "Cycling",
    "CLIMBING": "Climbing",
    "CURLING": "Curling",
    "DANCING": "Dancing",
    "DOWNHILL_SKIING": "Downhill skiing",
    "DUATHLON": "Duathlon",
    "DUATHLON_CYCLING": "Cycling",
    "DUATHLON_RUNNING": "Running",
    "E_BIKE": "Electric biking",
    "ESPORTS": "Esports",
    "FIELD_HOCKEY": "Field hockey",
    "FINNISH_BASEBALL": "Finnish baseball",
    "FITNESS_BOXING": "Fitness boxing",
    "FITNESS_DANCING": "Fitness dancing",
    "FITNESS_MARTIAL_ARTS": "Fitness martial arts",
    "FITNESS_RACING": "Fitness Racing",
    "FITNESS_STEP": "Step workout",
    "FLOORBALL": "Floorball",
    "FREE_MULTISPORT": "Multisport",
    "FRISBEEGOLF": "Disc golf",
    "FUNCTIONAL_TRAINING": "Functional training",
    "FUTSAL": "Futsal",
    "GOLF": "Golf",
    "GRAVEL": "Gravel cycling",
    "GROUP_EXERCISE": "Group exercise",
    "GYMNASTICK": "Gymnastics",
    "HANDBALL": "Handball",
    "HIIT": "High-intensity interval training",
    "HIKING": "Hiking",
    "ICE_HOCKEY": "Ice hockey",
    "ICE_SKATING": "Ice skating",
    "INDOOR_CYCLING": "Indoor cycling",
    "INDOOR_ROWING": "Indoor rowing",
    "INLINE_SKATING": "Inline skating",
    "JAZZ_DANCING": "Jazz",
    "JOGGING": "Jogging",
    "JUDO_MARTIAL_ARTS": "Judo",
    "JUMP_ROPE": "Rope skipping",
    "KETTLEBELL": "Kettlebell",
    "KICKBIKE": "Kickbiking",
    "KICKBOXING_MARTIAL_ARTS": "Kickboxing",
    "LATIN_DANCING": "Latin",
    "LES_MILLS_BARRE": "LES MILLS BARRE",
    "LES_MILLS_BODYATTACK": "LES MILLS BODYATTACK",
    "LES_MILLS_BODYBALANCE": "LES MILLS BODYBALANCE",
    "LES_MILLS_BODYCOMBAT": "LES MILLS BODYCOMBAT",
    "LES_MILLS_BODYJAM": "LES MILLS BODYJAM",
    "LES_MILLS_BODYPUMP": "LES MILLS BODYPUMP",
    "LES_MILLS_BODYSTEP": "LES MILLS BODYSTEP",
    "LES_MILLS_CXWORKS": "LES MILLS CXWORX",
    "LES_MILLS_GRIT_ATHLETIC": "LES MILLS GRIT Athletic",
    "LES_MILLS_GRIT_CARDIO": "LES MILLS GRIT Cardio",
    "LES_MILLS_GRIT_STRENGTH": "LES MILLS GRIT Strength",
    "LES_MILLS_RPM": "LES MILLS RPM",
    "LES_MILLS_SHBAM": "LES MILLS SH'BAM",
    "LES_MILLS_SPRINT": "LES MILLS SPRINT",
    "LES_MILLS_TONE": "LES MILLS TONE",
    "LES_MILLS_TRIP": "LES MILLS TRIP",
    "MOBILITY_DYNAMIC": "Mobility (dynamic)",
    "MOBILITY_STATIC": "Mobility (static)",
    "MODERN_DANCING": "Modern",
    "MOTORSPORTS_CAR_RACING": "Car racing",
    "MOTORSPORTS_ENDURO": "Enduro",
    "MOTORSPORTS_HARD_ENDURO": "Hard Enduro",
    "MOTORSPORTS_MOTOCROSS": "Motocorss",
    "MOTORSPORTS_ROADRACING": "Road racing",
    "MOTORSPORTS_SNOCROSS": "Snocross",
    "MOUNTAIN_BIKING": "Mountain biking",
    "NORDIC_WALKING": "Nordic walking",
    "OBSTACLE_COURSE_RACING": "Obstacle course racing",
    "OFFROADDUATHLON": "Off-road duathlon",
    "OFFROADDUATHLON_CYCLING": "Mountain biking",
    "OFFROADDUATHLON_RUNNING": "Trail running",
    "OFFROADTRIATHLON": "Off-road triathlon",
    "OFFROADTRIATHLON_CYCLING": "Mountain biking",
    "OFFROADTRIATHLON_RUNNING": "Trail running",
    "OFFROADTRIATHLON_SWIMMING": "Open water swimming",
    "OPEN_WATER_SWIMMING": "Open water swimming",
    "ORIENTEERING": "Orienteering",
    "ORIENTEERING_MTB": "Mountain bike orienteering",
    "ORIENTEERING_SKI": "Ski orienteering",
    "OTHER_INDOOR": "Other indoor",
    "OTHER_OUTDOOR": "Other outdoor",
    "PADEL": "Padel racing",
    "PARASPORTS_HAND_CYCLING": "Handcycling",
    "PARASPORTS_SLED_HOCKEY": "Sled hockey",
    "PARASPORTS_WATER_SKIING": "Adaptive water skiing",
    "PARASPORTS_WHEELCHAIR": "Wheelchair racing",
    "PARASPORTS_WHEELCHAIR_BASKETBALL": "Wheelchair basketball",
    "PARASPORTS_WHEELCHAIR_TENNIS": "Wheelchair tennis",
    "PICKLEBALL": "Pickleball",
    "PILATES": "Pilates",
    "POOL_SWIMMING": "Pool swimming",
    "RIDING": "Riding",
    "RINGETTE": "Ringette",
    "ROAD_BIKING": "Road cycling",
    "ROAD_RUNNING": "Road running",
    "ROLLER_BLADING": "Roller skating",
    "ROLLER_SKIING_CLASSIC": "Classic roller skiing",
    "ROLLER_SKIING_FREESTYLE": "Freestyle roller skiing",
    "ROWING": "Rowing",
    "RUGBY": "Rugby",
    "RUCKING": "Rucking",
    "RUNNING": "Running",
    "SHOW_DANCING": "Show",
    "SHOOTING_SPORT_INDOOR": "Shooting (indoor)",
    "SHOOTING_SPORT_OUTDOOR": "Shooting (outdoor)",
    "SKATEBOARDING": "Skateboarding",
    "SKATING": "Skating",
    "SKIERG": "Ski machine",
    "SNOWBOARDING": "Snowboarding",
    "SNOWSHOE_TREKKING": "Snowshoe trekking",
    "SOCCER": "Soccer",
    "SPINNING": "Spinning",
    "SUP": "SUP",
    "SQUASH": "Squash",
    "STAIR_WORKOUT": "Stair workout",
    "STREET_DANCING": "Street",
    "STRENGTH_TRAINING": "Strength training",
    "STRETCHING": "Stretching",
    "SWIMMING": "Swimming",
    "TABLE_TENNIS": "Table tennis",
    "TAEKWONDO_MARTIAL_ARTS": "Taekwondo",
    "TELEMARK_SKIING": "Telemark skiing",
    "TENNIS": "Tennis",
    "TRACK_AND_FIELD_RUNNING": "Track&field running",
    "TRAIL_RUNNING": "Trail running",
    "TREADMILL_RUNNING": "Treadmill running",
    "TRIATHLON": "Triathlon",
    "TRIATHLON_CYCLING": "Cycling",
    "TRIATHLON_RUNNING": "Running",
    "TRIATHLON_SWIMMING": "Open water swimming",
    "TROTTING": "Trotting",
    "ULTIMATE": "Ultimate",
    "ULTRARUNNING_RUNNING": "Ultra running",
    "VERTICALSPORTS_WALLCLIMBING": "Climbing (indoor)",
    "VERTICALSPORTS_OUTCLIMBING": "Climbing (outdoor)",
    "VOLLEYBALL": "Volleyball",
    "WALKING": "Walking",
    "WATER_EXERCISE": "Water sports",
    "WATER_RUNNING": "Water running",
    "WATERSPORTS_CANOEING": "Canoeing",
    "WATERSPORTS_KAYAKING": "Kayaking",
    "WATERSPORTS_KITESURFING": "Kitesurfing",
    "WATERSPORTS_SAILING": "Sailing",
    "WATERSPORTS_SURFING": "Surfing",
    "WATERSPORTS_WAKEBOARDING": "Wakeboarding",
    "WATERSPORTS_WATERSKI": "Water skiing",
    "WATERSPORTS_WINDSURFING": "Windsurfing",
    "XC_SKIING_CLASSIC": "Classic XC skiing",
    "XC_SKIING_FREESTYLE": "Freestyle XC skiing",
    "YOGA": "Yoga",
}


def activity_options(data: pd.DataFrame):
    #Helper function for dictionary expression
    def activity_string(entry):
        import time

        #Using below map to change names of exercises into something nicer to look at
        sport_map = {'RUNNING': 'Run',
                'INDOOR_CYCLING': 'Watt bike',
                'STRENGTH_TRAINING': 'Weights',
                'HIIT': 'HIIT',
                'HIKING': 'Hike'}
        
        activity_title = sport_map[entry[1]]

        #Formatting date to display day
        formatted_date = entry[2].strftime('%a %d %b')

        minutes = time.strftime('%H:%M:%S', time.gmtime(entry[3]))

        #Returning formatted f string for dictionary expression
        return f'{activity_title:<10} - {formatted_date} - {minutes}'
    
    data = data.sort_values(by = 'start_time', ascending=False)

    activity_options = {activity_string(entry)
            : entry[0]
            for entry in zip(data.index, data['detailed_sport_info'], data['start_time'], data['duration'])
            }
    
    return activity_options

#Function to executre above processing and create formatted selection box
def activity_options_selectbox(data: pd.DataFrame):
    activity_dic = activity_options(data = data)
    selected_activity = st.selectbox('Select Activity', options = list(activity_dic.keys()))

    activity_id = activity_dic[selected_activity]

    return data.loc[activity_id], data[data.index == activity_id], activity_id


def activity_summary(selected_activity: pd.DataFrame):   
        row = st.columns(3)

        #Markdown colour based on HR number
        def hr_colour(hr):
            if hr < 119:
                colour = 'grey'
            elif hr >=119 and hr < 139:
                colour = 'blue'
            elif hr >= 139 and hr <= 158:
                colour = 'green'
            elif hr > 158 and hr <= 178:
                colour = 'orange'
            elif hr > 179:
                colour = 'red'
            return colour

        #Avergage heartrate tile
        col1_tile = row[0].container(height=120)
        col1_tile.markdown('#### Average HR', text_alignment  = 'center')
        col1_tile.markdown(f':{hr_colour(selected_activity['heart_rate_avg'])}[{selected_activity['heart_rate_avg']}]', 
                           text_alignment= 'center')
        #Max heartrate tile
        col2_tile = row[1].container(height=120)
        col2_tile.markdown('#### Max HR', text_alignment  = 'center')
        col2_tile.markdown(f':{hr_colour(selected_activity['heart_rate_max'])}[{selected_activity['heart_rate_max']}]', 
                           text_alignment= 'center')
        #Cardio load tile
        col3_tile = row[2].container(height=120)
        col3_tile.markdown('#### Cardio Load', text_alignment  = 'center')
        col3_tile.markdown(f'{selected_activity['heart_rate_max']}', 
                           text_alignment= 'center')