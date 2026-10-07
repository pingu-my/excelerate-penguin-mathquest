"""Starter topic availability, not an official curriculum mapping."""
DIFFICULTIES = ['Beginner', 'Moderate', 'Challenging']
PATHS = ['Mixed Cambridge + Malaysian', 'Cambridge Primary', 'Malaysian Primary']
TOPICS = ['Whole Numbers', 'Operations', 'Fractions', 'Decimals', 'Percentages',
          'Money', 'Time', 'Measurement', 'Geometry', 'Ratio & Proportion',
          'Data Handling', 'Probability']

def available_topics(primary, syllabus):
    # All starter templates are shared skills; path is recorded in results.
    return [t for t in TOPICS if primary >= 5 or t not in
            ['Ratio & Proportion', 'Probability']]

POINTS = {'Beginner': [10, 8, 6, 5], 'Moderate': [20, 17, 14, 10],
          'Challenging': [30, 25, 20, 15]}
