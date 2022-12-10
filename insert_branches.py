import json
import sys

from branches.models import Branch, Operation, PhoneNumber, Schedule

with open("bcr_response.json") as src:
    processed_dict = json.load(src)

    entries = processed_dict["serviceResponse"]

    # Collect all possible operations
    operation_descs = set(op_desc for br in entries for op_desc in br["operations"])

    # Insert all operations
    operation_desc_to_id_map = {}
    for op_desc in operation_descs:
        op = Operation.objects.create(name=op_desc)
        operation_desc_to_id_map[op_desc] = op.id

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

        operation_ids = [
            operation_desc_to_id_map[op_desc] for op_desc in br_dict["operations"]
        ]
        branch.operations.add(*operation_ids)

        for phonenum_str in br_dict["telephone"]:
            PhoneNumber.objects.create(number=phonenum_str, branch=branch)
