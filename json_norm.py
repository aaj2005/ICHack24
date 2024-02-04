import tensorflow as tf
from tensorflow import keras
import numpy as np
from pandas import json_normalize
import pandas as pd
import json
import os


def normalize_json(body):
    protoper_data = body
    prot_data = protoper_data['data']
    protoper = json_normalize(prot_data)
    selected_columns = ['active_durations_data.activity_seconds',
                        'calories_data.BMR_calories',
                        'calories_data.net_activity_calories',
                        'distance_data.summary.distance_meters',
                        'distance_data.summary.steps',
                        'heart_rate_data.summary.avg_hr_bpm',
                        'heart_rate_data.summary.max_hr_bpm',
                        'heart_rate_data.summary.min_hr_bpm',
                        'heart_rate_data.summary.resting_hr_bpm',
                        'movement_data.avg_cadence_rpm',
                        'movement_data.avg_speed_meters_per_second',
                        'movement_data.max_cadence_rpm',
                        'movement_data.max_speed_meters_per_second',
                        'oxygen_data.avg_saturation_percentage',
                        'power_data.avg_watts',
                        'power_data.max_watts'
                        # , 'power_data.decline_hr_HRR'
                        ]

    protoper = protoper[selected_columns]

    column_mapping = {
        'active_durations_data.activity_seconds': 'active_seconds',
        'calories_data.BMR_calories': 'BMR_calories',
        'calories_data.net_activity_calories': 'activity_calories',
        'distance_data.summary.distance_meters': 'distance_meters',
        'distance_data.summary.steps': 'steps',
        'heart_rate_data.summary.avg_hr_bpm': 'avg_hr_bpm',
        'heart_rate_data.summary.max_hr_bpm': 'max_hr_bpm',
        'heart_rate_data.summary.min_hr_bpm': 'min_hr_bpm',
        'heart_rate_data.summary.resting_hr_bpm': 'resting_hr_bpm',
        'movement_data.avg_cadence_rpm': 'avg_cadence_rpm',
        'movement_data.avg_speed_meters_per_second': 'avg_speed_meters_per_second',
        'movement_data.max_cadence_rpm': 'max_cadence_rpm',
        'movement_data.max_speed_meters_per_second': 'max_speed_meters_per_second',
        'oxygen_data.avg_saturation_percentage': 'avg_saturation_percentage',
        'power_data.avg_watts': 'avg_watts',
        'power_data.max_watts': 'max_watts'
    }

    protoper.rename(columns=column_mapping, inplace=True)
    return protoper

# protoper = "protoper.json"
# with open(protoper, 'r') as file:
#     protoper_data = json.load(file)
# prot_data = protoper_data["data"]
#
# protoper = json_normalize(prot_data)