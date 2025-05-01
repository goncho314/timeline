from datetime import datetime
import yaml
import pandas as pd
import plotly.express as px
import shutil


if __name__ == "__main__":
    print("Running script...")

    # Cargar los ficheros YAML
    # with open("data/sprints.yml", "r") as f:
    #     sprints_data = yaml.safe_load(f)["sprints"]
    # with open("data/jira.yml", "r") as f:
    #     jira_data = yaml.safe_load(f)["workpackages"]
    #
    # # Normalizar sprints y corregir formato de fecha si es necesario
    # sprints = []
    # for sprint in sprints_data:
    #     sprints.append({
    #         "name": f"SP {sprint['name']}",
    #         "capacity1": sprint["capacity1"],
    #         "capacity2": sprint["capacity2"],
    #         "start": datetime.strptime(str(sprint["start"]), "%Y-%m-%d"),
    #         "end": datetime.strptime(str(sprint["end"]), "%Y-%m-%d")
    #     })
    #
    # # Extraer PBIs del backlog con la info necesaria
    # pbis = []
    # for wp in jira_data:
    #     for pbi in wp["pbis"]:
    #         for sprint_number in pbi["sprint"]:
    #             sprint_name = f"SP {sprint_number}"
    #             sprint_info = next((s for s in sprints if s["name"] == sprint_name), None)
    #             if sprint_info:
    #                 pbis.append({
    #                     "task": f"{pbi['name']} ({pbi['key']})",
    #                     "start": sprint_info["start"],
    #                     "end": sprint_info["end"],
    #                     "sprint": sprint_name,
    #                     "points": pbi["points"]
    #                 })
    #
    # # Convertir a DataFrame
    # df = pd.DataFrame(pbis)
    # df.head()
    #
    # fig = px.timeline(
    #     df,
    #     x_start="start",
    #     x_end="end",
    #     y="task",
    #     color="sprint",
    #     title="Gantt chart - Scrum Backlog",
    #     labels={"task": "Backlog Item"},
    # )
    #
    # fig.update_yaxes(autorange="reversed")  # para que el primer ítem aparezca arriba
    # fig.update_layout(height=800)
    #
    # # Exportar a HTML
    # fig.write_html("cronograma_scrum.html")