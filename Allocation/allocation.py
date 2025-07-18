import pandas as pd
import random
from collections import deque
import math

def main():
    fl = "FSC Signups.csv"
    df = pd.read_csv(fl)

    #Data Cleanup. Need to manually look at the data to see what is missing
    df["Personality"] = df["Personality"].fillna("M XXX")
    df["Pre-U Education"] =  df["Pre-U Education"].fillna("Others")

    #Create a joint group for the unique combinations of this
    df["Grouping"] = df["Personality"] + "-" + df["Gender"] + "-" + df["Course of study :"]

    #Split people into groups based on their groupings. Forming 2 grps for each gender as subsequently maintaining gender ratio is the most important
    grp_M, grp_F = gengroup(df, "Male"), gengroup(df, "Female")

    #Based on the respective grouping, form sets corresponding to each group containing the ids of the people who belong in it
    M_id_Q, F_id_Q = loadq(grp_M), loadq(df, grp_F)

    group_size = 10  # Replace with your desired group size
    total_students = len(df)
    n_groups = total_students // group_size + (1 if total_students % group_size > 0 else 0)

    groupings, id_to_group = alloc(M_id_Q, F_id_Q, total_students, group_size)

    df["Ori Grouping"] = df["Id"].map(id_to_group)

   #The rest will now create relevent spreadsheets with the groupings and individuals details.
   #TODO Replace these with your actual column names
    summary_cols = ["Ori Grouping", "Name", "Student/Application Number", "Telegram handle (eg @shr221)"]
    shirt_size_col = "Shirt Size"
    Maj_col = "Course of study :"

    summary_df = df[summary_cols].sort_values(by="Ori Grouping")

    shirt_summary = df.groupby(["Ori Grouping", shirt_size_col]).size().unstack(fill_value=0)
    gender_summary = df.groupby(["Ori Grouping", "Gender"]).size().unstack(fill_value=0)
    Maj_summary = df.groupby(["Ori Grouping", Maj_col]).size().unstack(fill_value=0)

    with pd.ExcelWriter("grouped_participants.xlsx", engine="xlsxwriter") as writer:

        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        shirt_summary.to_excel(writer, sheet_name="Shirt Size Summary")
        gender_summary.to_excel(writer, sheet_name="Gender Summary")
        Maj_summary.to_excel(writer, sheet_name="Maj Summary")

        for group_name, group_df in df.groupby("Ori Grouping"):
            sheet_name = str(group_name)
            group_df.to_excel(writer, sheet_name=sheet_name, index=False)



def draw_person(id_queues_by_group):
    group_names = list(id_queues_by_group.keys())
    weights = [len(q) for q in id_queues_by_group.values()]

    if not group_names or sum(weights) == 0:
        return None, None

    selected_group = random.choices(group_names, weights=weights, k=1)[0]
    person_id = id_queues_by_group[selected_group].popleft()

    if not id_queues_by_group[selected_group]:
        del id_queues_by_group[selected_group]

    return selected_group, person_id

def alloc(M_id_Q, F_id_Q, total, grp_size):
    groups = []
    id_to_group = {}

    n_groups = total // grp_size + (1 if total % grp_size > 0 else 0)

    male_ratio = sum(len(queue) for queue in M_id_Q.values()) / total

    males_per_group = math.floor(male_ratio * grp_size + 0.5)
    females_per_group = grp_size - males_per_group

    for i in range(n_groups - 1):
        group_ids = []

        for j in range(females_per_group):
            k, person_id = draw_person(F_id_Q)
            if person_id:
                group_ids.append(person_id)
                id_to_group[person_id] = i + 1

        for j in range(males_per_group):
            k, person_id = draw_person(M_id_Q)
            if person_id:
                group_ids.append(person_id)
                id_to_group[person_id] = i + 1

        groups.append(group_ids)

    remaining_ids = []
    for group_dict in [M_id_Q, F_id_Q]:
        for queue in group_dict.values():
            remaining_ids.extend(queue)
    for i in remaining_ids:
        id_to_group[i] = n_groups
    groups.append(remaining_ids)

    return groups, id_to_group


def gengroup(df, gender):
    x_df = df[df['Gender'] == gender]
    return {ptype: x_df[x_df["Grouping"]] 
            for ptype in x_df["Grouping"].unique}

def loadq(p_grp):
    return {ptype: deque(random.sample(df["Id"].tolist(), len(df)))
    for ptype, df in p_grp.items()}

if __name__ == "__main__":
    main()

