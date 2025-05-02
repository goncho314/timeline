import json
from datetime import datetime
from itertools import groupby


COLSPAN = 2
BASE_LINK = "https://jira.example.com/browse/"


def get_sprints() -> list[dict]:
    with open("data/sprints.json", "r") as f:
        return json.load(f)["sprints"]


def get_workpackages() -> list[dict]:
    with open("data/workpackages.json", "r") as f:
        return json.load(f)["workpackages"]


def get_jira() -> list[dict]:
    with open("data/stories.json", "r") as f:
        return json.load(f)["stories"]


def get_style() -> str:
    with open("html/style.txt", "r") as f:
        return f.read()


def \
        get_workpackages_and_stories(sprints: list[dict]) -> list[dict]:
    stories = get_jira()
    workpackages_dict = {workpackage["id"]: workpackage for workpackage in get_workpackages()}
    sorted_stories = sorted(stories, key=lambda story: (story["workpackage"], story["sprint"]))
    grouped_workpackages = groupby(sorted_stories, key=lambda story: story["workpackage"])
    workpackages = []
    for workpackage_id, stories in grouped_workpackages:
        stories = list(stories)
        start_sprint = min(story["sprint"] for story in stories)
        workpackage = workpackages_dict[workpackage_id]
        grouped_stories = {key: list(value) for key, value in groupby(stories, key=lambda story: story["sprint"])}
        columns = []
        for sprint in sprints:
            stories = grouped_stories.get(sprint.get("id"), [])
            if not stories:
                columns.append(None)
            else:
                columns.append({'points': sum(story["points"] for story in stories),
                                'stories': stories})
        workpackages.append({
            'workpackage': workpackage,
            'sprint_stories': columns,
            'start_sprint': start_sprint
        })
    return workpackages


def build_header(sprints: list[dict]) -> str:
    html = '<thead>'
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    empty_cell = f'<th class="no-border" colspan="2">{dt}</th>\n'
    html_sprints = '<tr>' + empty_cell
    html_dates = '<tr>' + empty_cell
    html_points = '<tr>' + empty_cell

    for sprint in sprints:
        start_date = datetime.strptime(sprint["start"], "%Y-%m-%d")
        end_date = datetime.strptime(sprint["end"], "%Y-%m-%d")
        html_sprints += f'<th colspan="{COLSPAN}">{sprint["name"]}</th>\n'
        html_dates += f'<th>{start_date.strftime("%d-%b")}</th>' \
                      f'<th>{end_date.strftime("%d-%b")}</th>\n'
        html_points += f'<th>{sprint["capacity1"]}</th>' \
                       f'<th>{sprint["capacity2"]}</th>\n'

    row_end = '</tr>'
    html_sprints += row_end
    html_dates += row_end
    html_points += row_end
    html += html_sprints + html_dates + html_points + '</thead>'
    return html


def build_body(workpackages: list[dict]) -> str:
    html = '<tbody>'
    for i, workpackage in enumerate(workpackages, start=1):
        row = f'<tr>' \
              f'<td class="tg-{i}pky rounded" colspan="{COLSPAN}"><a href="{BASE_LINK}{workpackage["workpackage"]["id"]}">{workpackage["workpackage"]["id"]}<br>{workpackage["workpackage"]["name"]}</td>\n'
        for sprint in workpackage["sprint_stories"]:
            if sprint is None:
                row += f'<td class="no-border" colspan="{COLSPAN}"></td>\n'
            else:
                points = sprint["points"]
                stories = sprint["stories"]
                row += f'<td class="tg-{i}pky rounded" colspan="{COLSPAN}">\n'
                row += '<div class="dropdown">\n'
                row += '<span class="icon">&#43;</span>\n'
                row += '<div class="dropdown-content">\n'
                for story in stories:
                    row += f'<a href="{BASE_LINK}{story["id"]}">{story["id"]} {story["name"]}</a>\n'
                row += '</div>\n'
                row += '</div>\n'
                row += f'{points} ' + ('point' if points == 1 else 'points')
                row += '</td>\n'
        html += row
    html += '</tbody>'
    return html


def build_page() -> str:
    sprints = get_sprints()
    workpackages_and_stories = get_workpackages_and_stories(sprints)
    sorted_workpackages = sorted(workpackages_and_stories, key=lambda workpackage: (workpackage["start_sprint"], workpackage["start_sprint"]))

    style = get_style()
    html = f'{style}' \
           f'<table id="timeline">' \
           f'{build_header(sprints)}' \
           f'{build_body(sorted_workpackages)}'
    html += '</table>'
    return html


if __name__ == "__main__":
    page = build_page()
    # with open(f"public/result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html", "w") as output:
    with open(f"public/index.html", "w") as output:
        output.write(page)
