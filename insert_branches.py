import json

from branches.models import Branch, Operation, PhoneNumber, Schedule

operation_desc_to_id_map = {}


def insert_operation(**operation_args):
    op = Operation.objects.create(**operation_args)
    operation_desc_to_id_map[operation_args["name"]] = op.id
    return op


with open("bcr_operations.json") as src:
    processed_dict = json.load(src)
    entries = processed_dict["serviceResponse"]

    # Insert all operations
    for op_dict in entries:
        insert_operation(
            name=op_dict["operationType"],
            description=op_dict["operationDescription"],
            appointment_duration=op_dict["durationMinutes"],
        )

with open("bcr_response.json") as src:
    processed_dict = json.load(src)

    entries = processed_dict["serviceResponse"]

    # Insert branches
    for br_dict in entries:
        appt_dict = br_dict["appointmentsSchedule"]

        mf_schedule = Schedule.objects.create(
            start_hour=appt_dict["scheduleMonFriStart"]["hour"],
            start_minute=appt_dict["scheduleMonFriStart"]["minute"],
            end_hour=appt_dict["scheduleMonFriEnd"]["hour"],
            end_minute=appt_dict["scheduleMonFriEnd"]["minute"],
        )

        satsun_schedule = Schedule.objects.create(
            start_hour=appt_dict["scheduleSatSunStart"]["hour"],
            start_minute=appt_dict["scheduleSatSunStart"]["minute"],
            end_hour=appt_dict["scheduleSatSunEnd"]["hour"],
            end_minute=appt_dict["scheduleSatSunEnd"]["minute"],
        )

        break_schedule = Schedule.objects.create(
            start_hour=appt_dict["lunchBreakStart"]["hour"],
            start_minute=appt_dict["lunchBreakStart"]["minute"],
            end_hour=appt_dict["lunchBreakEnd"]["hour"],
            end_minute=appt_dict["lunchBreakEnd"]["minute"],
        )

        branch = Branch.objects.create(
            branch_id=br_dict["branchId"],
            name=br_dict["brn"],
            street=br_dict["br_street"],
            city=br_dict["br_city"],
            county=br_dict["location"]["address"]["county"],
            latitude=br_dict["location"]["latitude"],
            longitude=br_dict["location"]["longitude"],
            mf_schedule=mf_schedule,
            is_weekend_open=appt_dict["isWeekendOpen"],
            is_sunday_open=appt_dict["isSundayOpen"],
            satsun_schedule=satsun_schedule,
            has_break=appt_dict["hasLunchBreak"],
            break_schedule=break_schedule,
        )

        operation_ids = []
        for op_name in br_dict["operations"]:
            try:
                operation_ids.append(operation_desc_to_id_map[op_name])
            except KeyError:
                op = insert_operation(
                    name=op_name, description=op_name, appointment_duration=20
                )
                operation_ids.append(op.id)

        branch.operations.add(*operation_ids)

        for phonenum_str in br_dict["telephone"]:
            PhoneNumber.objects.create(number=phonenum_str, branch=branch)
