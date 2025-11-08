import requests

URL = "https://api.ftcscout.org/graphql"
def make_request(eventCode, season):
    statsQuery = str(season)+"Trad" if season==2020 or season==2021 else season

    query = f"""
        query Query($season: Int!, $code: String!) {{
          eventByCode(season: $season, code: $code) {{
            teams {{
              teamNumber
              stats {{
                ... on TeamEventStats{statsQuery} {{
                  rank
                }}
              }}
              awards {{
                type
                placement
              }}
              matches {{
                match {{
                  description
                }}
                alliance
                onField
                allianceRole
              }}
              team {{
                name
              }}
            }}
            relatedEvents {{
              code
              divisionCode
            }}
          }}
        }}
    """

    variables = {
      "season": season,
      "code": eventCode
    }

    # Data to be sent in the request body
    payload = {
        "query": query,
        "variables": variables
    }

    data = None
    try:
        # Make the POST request with JSON data
        response = requests.post(URL, json=payload)

        # Check if the request was successful (status code 201 Created)
        if response.status_code == 200:
            data = response.json()
            print("POST Request Successful:")
        else:
            print(f"Error: {response.status_code}")

        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def getTeamsFromEvent(eventCode, season):
    eventCode = eventCode.upper()
    data = make_request(eventCode, season)
    teams = []

    related_events = data["data"]["eventByCode"]["relatedEvents"]
    if related_events and all([code["divisionCode"] is not None for code in related_events]):
        for event in related_events:
            new_data = make_request(event["code"], season)
            teams.extend(new_data["data"]["eventByCode"]["teams"])
    else:
        teams = data["data"]["eventByCode"]["teams"]

    # Removing empty teams
    teams = [team for team in teams if team["stats"]]

    # Removing unnecessary matches
    for team in teams:
        matches = team["matches"]
        # Filter out non-"M" matches
        team["matches"] = [match for match in matches 
                          if match["match"]["description"][0] != "Q"]

        # Adding poitns attribute to every team
        team["points"] = 0

    return teams
