import os


def print_csv(result):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    initial_run = result[0]
    rows = []
    for letter in abc:
        if letter in initial_run:
            row = [letter]
            for run in result:
                row.append(str(run[letter]["duration"]))
            if len(row) > 0:
                rows.append(row)

    direct_cost_row = ["Питомі витрати"]
    for run in result:
        direct_cost_row.append(str(run['direct_cost']))
    rows.append(direct_cost_row)

    overhead_cost_row = ["Непрямі витрати"]
    for run in result:
        overhead_cost_row.append(str(run['total_overhead']))
    rows.append(overhead_cost_row)

    project_cost_row = ["Загальні витрати"]
    for run in result:
        project_cost_row.append(str(run['project_cost']))
    rows.append(project_cost_row)

    duration_row = ["Загальна тривалість"]
    for run in result:
        duration_row.append(str(run['duration']))
    rows.append(duration_row)

    with open("report.csv", "w", encoding='utf-8') as f:
        for row in rows:
            f.write(",".join(row) + os.linesep)


def print_html(result):
    first_row_headers = [
        "<td rowspan='2'>Операція</td>"
        "<td colspan='3'>Початково</td>"
    ]
    for i in range(1, len(result)):
        first_row_headers.append(f"<td colspan='2'>Ітерація #{i}</td>")

    second_row_headers = [
        "<td>Тривалість</td>",
        "<td>Терм. витрати</td>",
        "<td>Звич. витрати</td>"
    ]
    for _ in result[1:]:
        second_row_headers.append("<td>мінус днів</td>")
        second_row_headers.append("<td>Тривалість</td>")

    initial_run = result[0]
    data_rows = []
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for letter in abc:
        row = []
        if letter in initial_run:
            row.append(f"<td>{letter}</td>")
        if letter in initial_run:
            row.append(
                f"<td>{initial_run[letter]['duration']}</td>" +
                f"<td>{initial_run[letter]['crash_cost']}</td>" +
                f"<td>{initial_run[letter]['normal_cost']}</td>"
            )
        for run in result[1:]:
            if letter in run:
                row.append(
                    f"<td>{run[letter]['saved_days']}</td>"
                    f"<td>{run[letter]['duration']}</td>"
                )
        if len(row) > 0:
            data_rows.append("<tr>" + "".join(row) + "</tr>")
    cost_data = []
    saving_data = []
    direct_cost_data = []
    overhead_cost_data = []
    project_cost_data = []
    project_duration_data = []
    for i, run in enumerate(result):
        colspan = 3 if i == 0 else 2
        cost_data.append(f"<td colspan='{colspan}'>{run['cost']}</td>")
        saving_data.append(f"<td colspan='{colspan}'>{run['savings']}</td>")
        direct_cost_data.append(f"<td colspan='{colspan}'>{run['direct_cost']}</td>")
        overhead_cost_data.append(f"<td colspan='{colspan}'>{run['total_overhead']}</td>")
        project_cost_data.append(f"<td colspan='{colspan}'>{run['project_cost']}</td>")
        project_duration_data.append(f"<td colspan='{colspan}'>{run['duration']}</td>")

    report = f"""
    <table border="1">
    <thead>
    <tr>
        {"".join(first_row_headers)}
    </tr>
    <tr>
        {"".join(second_row_headers)}
    </tr>
    </thead>
    <tbody>
        {"".join(data_rows)}
    <tr>
        <td>Термінова ціна</td>
        {"".join(cost_data)}
    </tr>
    <tr>
        <td>Непряма економія</td>
        {"".join(saving_data)}
    </tr>
    <tr>
        <td>Питомі витрати</td>
        {"".join(direct_cost_data)}
    </tr>
    <tr>
        <td>Непрямі витрати</td>
        {"".join(overhead_cost_data)}
    </tr>
    <tr>
        <td>Загальні витрати</td>
        {"".join(project_cost_data)}
    </tr>
    <tr>
        <td>Тривалість проекту</td>
        {"".join(project_duration_data)}
    </tr>
    </tbody>
</table>
    """

    with open("report.html", "w", encoding='utf-8') as f:
        f.write(report)
