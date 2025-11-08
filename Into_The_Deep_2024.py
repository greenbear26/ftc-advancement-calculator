import streamlit
import sys
import pandas

import request
import utils.general as general
import utils.doubleelim.eightalliance as eightalliance
import utils.doubleelim.sixalliance as sixalliance
import utils.doubleelim.fouralliance as fouralliance
import utils.doubleelim.twoalliance as twoalliance

def countAwards(teams):
    general.countAwards(teams)

def countRanking(teams):
    general.countRanking(teams)

def countAdvancement(teams):
    if len(teams) > 40:
        eightalliance.countAdvancement(teams)
    elif len(teams) > 20:
        sixalliance.countAdvancement(teams)
    elif len(teams) > 10:
        fouralliance.countAdvancement(teams)
    else:
        twoalliance.countAdvancement(teams)

def countAlliance(teams):
    if len(teams) > 40:
        eightalliance.countAlliance(teams)
    elif len(teams) > 20:
        sixalliance.countAlliance(teams)
    elif len(teams) > 10:
        fouralliance.countAlliance(teams)
    else:
        twoalliance.countAlliance(teams)


def main():
    manual = "https://www.firstinspires.org/resource-library/ftc/game-and-season-info"
    streamlit.title(":blue[FTC 2024: Into the Deep] Advancement Points Calculator")
    streamlit.write("This program will calculate the points that teams at a\
                    given competition would get using the 2025 points ranking\
                    system. The calculation follows the\
                    specifics detailed in the 2025 [competition manual](%s), \
                    with these small tweaks:" % manual)
    streamlit.write("- Second picks on alliances at worlds will receive 1 less \
                    point per pick based on the order they were picked. Ex. The\
                    second pick of the 8th alliance receives 7 more points\
                    than the second pick of the 1st alliance because of the \
                    snake draft.")
    streamlit.write("- Teams on alliances at worlds who don't play in any \
                    elimination matches do not get points for alliance \
                    advancement, but do get points for being on the alliance.")

    event_code = streamlit.text_input("Event Code")
    try:
        teams = request.getTeamsFromEvent(event_code, 2024)
    except:
        ftc_events = "https://ftc-events.firstinspires.org/2024#allevents"
        streamlit.write("Event code not valid. Refer to [FTCEvents](%s) for valid\
                        event codes." % ftc_events)
        return
    
    countAwards(teams)
    countRanking(teams)
    countAdvancement(teams)
    countAlliance(teams)

    teams.sort(key=lambda team: team["points"], reverse=True)

    dataframe = pandas.DataFrame({
        "Team Number": [team["teamNumber"] for team in teams],
        "Team Name": [team["team"]["name"] for team in teams],
        "Points": [team["points"] for team in teams]
    })

    streamlit.dataframe(dataframe, hide_index=True)

    streamlit.write("###### Created by Rishi Ponnapalli")


if __name__ == "__main__":
    main()
