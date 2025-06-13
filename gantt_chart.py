import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

# Set font for better display
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['axes.unicode_minus'] = False

# Project dates based on IRP schedule
project_start = datetime(2025, 5, 26)  # IRP Start
project_end = datetime(2025, 8, 29)    # Final Report deadline
today = datetime(2025, 6, 13)          # Today

# Calculate weeks from start
def date_to_week(date):
    return (date - project_start).days / 7

# Project timeline data with actual dates - reorganized for better flow
tasks = [
    # Phase 1: Foundation and Setup
    {"name": "Literature Review & Analysis", "start_date": datetime(2025, 5, 26), "duration": 10, "phase": "Foundation", "color": "#2E8B57"},
    {"name": "Development Environment Setup", "start_date": datetime(2025, 5, 26), "duration": 7, "phase": "Foundation", "color": "#2E8B57"},
    {"name": "GitHub Repository Setup", "start_date": datetime(2025, 5, 28), "duration": 5, "phase": "Foundation", "color": "#2E8B57"},
    {"name": "EdNet Dataset Preprocessing", "start_date": datetime(2025, 6, 2), "duration": 10, "phase": "Foundation", "color": "#32CD32"},
    {"name": "Baseline KMaP Implementation", "start_date": datetime(2025, 6, 9), "duration": 10, "phase": "Foundation", "color": "#32CD32"},
    {"name": "Experimental Framework Design", "start_date": datetime(2025, 6, 14), "duration": 7, "phase": "Foundation", "color": "#32CD32"},
    
    # Phase 2: Core Implementation
    {"name": "Sentence-BERT Integration", "start_date": datetime(2025, 6, 16), "duration": 12, "phase": "Core Implementation", "color": "#FF8C00"},
    {"name": "Embedding Fusion Development", "start_date": datetime(2025, 6, 23), "duration": 10, "phase": "Core Implementation", "color": "#FF8C00"},
    {"name": "Semantic Similarity Validation", "start_date": datetime(2025, 6, 30), "duration": 8, "phase": "Core Implementation", "color": "#FFA500"},
    {"name": "Adaptive Forgetting Mechanism", "start_date": datetime(2025, 7, 7), "duration": 12, "phase": "Core Implementation", "color": "#FF6347"},
    {"name": "Personalized Forgetting Profiles", "start_date": datetime(2025, 7, 14), "duration": 10, "phase": "Core Implementation", "color": "#FF6347"},
    {"name": "Integration Testing", "start_date": datetime(2025, 7, 21), "duration": 7, "phase": "Core Implementation", "color": "#FF4500"},
    
    # Phase 3: Advanced Features
    {"name": "Gated MoE Architecture", "start_date": datetime(2025, 7, 28), "duration": 14, "phase": "Advanced Features", "color": "#DC143C"},
    {"name": "Dynamic Student Profiling", "start_date": datetime(2025, 8, 4), "duration": 12, "phase": "Advanced Features", "color": "#DC143C"},
    {"name": "Behavioral Pattern Analysis", "start_date": datetime(2025, 8, 11), "duration": 10, "phase": "Advanced Features", "color": "#B22222"},
    {"name": "System Integration & Testing", "start_date": datetime(2025, 8, 18), "duration": 8, "phase": "Advanced Features", "color": "#8B0000"},
    
    # Phase 4: Evaluation and Documentation
    {"name": "Comprehensive Evaluation", "start_date": datetime(2025, 8, 25), "duration": 4, "phase": "Evaluation", "color": "#4169E1"},
    {"name": "Performance Analysis", "start_date": datetime(2025, 8, 26), "duration": 3, "phase": "Evaluation", "color": "#1E90FF"},
    {"name": "Final Report Writing", "start_date": datetime(2025, 8, 15), "duration": 14, "phase": "Evaluation", "color": "#6495ED"},
    {"name": "Documentation & Presentation", "start_date": datetime(2025, 8, 22), "duration": 7, "phase": "Evaluation", "color": "#87CEEB"},
]

# Convert dates to week positions
for task in tasks:
    task["start_week"] = date_to_week(task["start_date"])
    task["duration_weeks"] = task["duration"] / 7

# Create wider landscape figure for better horizontal proportion
fig, ax = plt.subplots(figsize=(14, 8))

# Define y-positions for tasks
y_positions = list(range(len(tasks)))
y_positions.reverse()

# Plot the Gantt chart bars
for i, task in enumerate(tasks):
    y_pos = y_positions[i]
    start_week = task["start_week"]
    duration_weeks = task["duration_weeks"]
    color = task["color"]
    
    # Create rectangle for the task
    rect = patches.Rectangle((start_week, y_pos-0.35), duration_weeks, 0.7, 
                           linewidth=0.8, edgecolor='white', facecolor=color, alpha=0.85)
    ax.add_patch(rect)

# Calculate total project weeks
total_weeks = date_to_week(project_end)

# Customize the plot
ax.set_xlim(-0.5, total_weeks + 0.5)
ax.set_ylim(-1.5, len(tasks))

# Create better date labels for x-axis
week_dates = []
week_labels = []
for i in range(0, int(total_weeks) + 2, 2):
    date = project_start + timedelta(weeks=i)
    week_dates.append(i)
    week_labels.append(date.strftime('%m/%d'))

ax.set_xlabel('Timeline (2025)', fontsize=11, fontweight='bold')
ax.set_xticks(week_dates)
ax.set_xticklabels(week_labels, rotation=0, ha='center', fontsize=9)

# Set y-axis with better formatting
ax.set_yticks(y_positions)
task_names = [task["name"] for task in tasks]
ax.set_yticklabels(task_names, fontsize=8, ha='right')

# Add phase background colors with better organization
phase_colors = {
    "Foundation": "#E8F5E8",
    "Core Implementation": "#FFF8DC", 
    "Advanced Features": "#FFE4E1",
    "Evaluation": "#F0F8FF"
}

# Group tasks by phase for background
phase_groups = {}
for i, task in enumerate(tasks):
    phase = task["phase"]
    if phase not in phase_groups:
        phase_groups[phase] = []
    phase_groups[phase].append(i)

# Add phase backgrounds
for phase, task_indices in phase_groups.items():
    if task_indices:
        y_min = min([y_positions[i] for i in task_indices]) - 0.5
        y_max = max([y_positions[i] for i in task_indices]) + 0.5
        height = y_max - y_min
        
        rect = patches.Rectangle((-0.5, y_min), total_weeks + 1, height, 
                               linewidth=0, facecolor=phase_colors[phase], alpha=0.3)
        ax.add_patch(rect)

# Add "Today" line with better visibility - this shows current progress
today_week = date_to_week(today)
ax.axvline(x=today_week, color='#FF4444', linestyle='-', alpha=0.9, linewidth=3)

# Position the progress text to avoid blocking dates - move it to the side
ax.text(today_week + 0.3, len(tasks) * 0.8, 'Current Progress\n(June 13)', rotation=0, 
       fontsize=8, ha='left', va='center', color='#FF4444', fontweight='bold',
       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#FF4444', alpha=0.9))

# Add more visible grid
ax.grid(True, axis='both', alpha=0.6, linestyle='-', linewidth=0.8, color='lightgray')
ax.set_axisbelow(True)

# Add title with better formatting
plt.suptitle('IRP Project Timeline: Cognitive-Enhanced Knowledge Tracing Framework', 
            fontsize=13, fontweight='bold', y=0.95)
plt.title('May 26 - August 29, 2025', fontsize=11, pad=10)

# Add compact legend with phase colors
legend_elements = []
phase_display_names = {
    "Foundation": "Phase 1: Foundation",
    "Core Implementation": "Phase 2: Core Implementation", 
    "Advanced Features": "Phase 3: Advanced Features",
    "Evaluation": "Phase 4: Evaluation"
}

for phase, color in phase_colors.items():
    legend_elements.append(patches.Patch(color=color, alpha=0.8, 
                                       label=phase_display_names[phase]))

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.99, 0.99), 
         fontsize=8, framealpha=0.95, edgecolor='gray')

# Add phase dividers
current_phase = ""
for i, task in enumerate(tasks):
    if task["phase"] != current_phase:
        current_phase = task["phase"]
        if i > 0:  # Not the first phase
            y_line = y_positions[i] + 0.5
            ax.axhline(y=y_line, color='gray', linestyle='-', alpha=0.4, linewidth=1)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Adjust layout for better fit with wider format
plt.tight_layout()
plt.subplots_adjust(left=0.25, right=0.95, top=0.88, bottom=0.12)

# Save the figure with high quality
plt.savefig('project_gantt_chart.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none', pad_inches=0.1)
plt.show()

print("[甘特图生成] 调整后的宽版甘特图已生成，进度标记不再遮挡日期") 