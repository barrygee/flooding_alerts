#!/usr/bin/env python
from crew import CrewaiFloodingAlertsAndWarningsCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'Flood alerts and warnings',
        'format': 'JSON',
        'location': 'Trent',
    }
    result = CrewaiFloodingAlertsAndWarningsCrew().crew().kickoff(inputs=inputs)
    print(result)