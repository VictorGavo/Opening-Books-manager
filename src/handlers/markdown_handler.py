# Handles markdown file generation and updates
import os
import datetime
import re
from string import Template

def read_template(template_path):
    """
    Reads the markdown template file.
    
    Args:
        template_path: Path to the template file
        
    Returns:
        str: The template content
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        return None

def format_date(date_format="%Y-%m-%d"):
    """
    Returns the current date formatted according to the specified format.
    
    Args:
        date_format: The format string for the date
        
    Returns:
        str: Formatted date string
    """
    return datetime.datetime.now().strftime(date_format)

def get_previous_day(date_str, date_format="%Y-%m-%d"):
    """
    Returns the previous day's date.
    
    Args:
        date_str: Current date string
        date_format: The format string for the date
        
    Returns:
        str: Previous day's date string
    """
    current_date = datetime.datetime.strptime(date_str, date_format)
    previous_date = current_date - datetime.timedelta(days=1)
    return previous_date.strftime(date_format)

def get_next_day(date_str, date_format="%Y-%m-%d"):
    """
    Returns the next day's date.
    
    Args:
        date_str: Current date string
        date_format: The format string for the date
        
    Returns:
        str: Next day's date string
    """
    current_date = datetime.datetime.strptime(date_str, date_format)
    next_date = current_date + datetime.timedelta(days=1)
    return next_date.strftime(date_format)

def get_week_number(date_str, date_format="%Y-%m-%d"):
    """
    Returns the week number for the given date.
    
    Args:
        date_str: Date string
        date_format: The format string for the date
        
    Returns:
        str: Year and week number (e.g., "2025-W12")
    """
    date = datetime.datetime.strptime(date_str, date_format)
    year = date.strftime("%Y")
    week = date.strftime("%W")
    return f"{year}-W{week}"

def process_template_variables(template_content, date_str):
    """
    Processes template variables like date formatting, previous/next day links, etc.
    
    Args:
        template_content: The template content
        date_str: Current date string
        
    Returns:
        str: Template with processed variables
    """
    # Replace date-related variables
    content = template_content
    
    # Replace tp.date.now
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    content = content.replace('<% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>', now)
    
    # Replace tp.file.title with date_str
    content = content.replace('<%tp.file.title%>', date_str)
    
    # Replace moment-based date calculations
    prev_day = get_previous_day(date_str)
    next_day = get_next_day(date_str)
    week_num = get_week_number(date_str)
    
    # Previous day
    content = content.replace('<% moment(tp.file.title,\'YYYY-MM-DD\').add(-1,\'days\').format("YYYY-MM-DD") %>', prev_day)
    
    # Next day
    content = content.replace('<% moment(tp.file.title,\'YYYY-MM-DD\').add(1,\'days\').format("YYYY-MM-DD") %>', next_day)
    
    # Week number
    content = content.replace('<% moment(tp.file.title,\'YYYY-MM-DD\').format("YYYY-[W]WW") %>', week_num)
    
    return content

def create_daily_note_from_sod(sod_data, template_path, date_str=None):
    """
    Creates a daily note markdown file from SOD form data.
    
    Args:
        sod_data: Dictionary containing SOD form data
        template_path: Path to the template file
        date_str: Date string for the note (defaults to today)
        
    Returns:
        str: The generated markdown content
    """
    if date_str is None:
        date_str = format_date()
    
    # Read template
    template_content = read_template(template_path)
    if not template_content:
        return None
    
    # Process template variables
    content = process_template_variables(template_content, date_str)
    
    # Map SOD form data to template sections
    if "What am I looking forward to the most today?" in sod_data:
        highlight = sod_data["What am I looking forward to the most today?"]
        content = content.replace("What am I looking forward to the most today?", 
                                 f"What am I looking forward to the most today?\n{highlight}")
    
    if "Today's Big 3" in sod_data:
        big_3_text = sod_data["Today's Big 3"]
        # Try to split the text into lines and format as list items
        big_3_items = big_3_text.strip().split('\n')
        big_3_formatted = ""
        
        for i, item in enumerate(big_3_items, 1):
            if i <= 3:  # Only use the first 3 items
                big_3_formatted += f"{i}. {item.strip()}\n"
        
        # Replace the placeholder in the template
        content = content.replace("1. \n2. \n3. ", big_3_formatted)
    
    # Gratitude section
    if "3 things I'm grateful for in my life:" in sod_data:
        grateful_life = sod_data["3 things I'm grateful for in my life:"]
        content = content.replace("**3 things I'm grateful for in my life:**\n- ", 
                                 f"**3 things I'm grateful for in my life:**\n- {grateful_life}")
    
    if "3 things I'm grateful about myself:" in sod_data:
        grateful_self = sod_data["3 things I'm grateful about myself:"]
        content = content.replace("**3 things I'm grateful for about myself:**\n- ", 
                                 f"**3 things I'm grateful for about myself:**\n- {grateful_self}")
    
    # Morning Mindset section
    mindset_fields = [
        "I'm excited today for:",
        "One word to describe the person I want to be today would be __ because:",
        "Someone who needs me on my a-game today is:",
        "What's a potential obstacle/stressful situation for today and how would my best self deal with it?",
        "Someone I could surprise with a note, gift, or sign of appreciation is:",
        "One action I could take today to demonstrate excellence or real value is:",
        "One bold action I could take today is:",
        "An overseeing high performance coach would tell me today that:",
        "The big projects I should keep in mind, even if I don't work on them today, are:",
        "I know today would be successful if I did or felt this by the end:"
    ]
    
    for field in mindset_fields:
        if field in sod_data:
            # Create a pattern that matches the field name followed by a blank line or colon
            pattern = f"\\*\\*{re.escape(field)}\\*\\*\\s*\n"
            replacement = f"**{field}**\n{sod_data[field]}\n"
            content = re.sub(pattern, replacement, content)
    
    return content

def update_daily_note_with_eod(eod_data, existing_content, date_str=None):
    """
    Updates an existing daily note with EOD form data.
    
    Args:
        eod_data: Dictionary containing EOD form data
        existing_content: Existing markdown content
        date_str: Date string for the note (defaults to today)
        
    Returns:
        str: The updated markdown content
    """
    if date_str is None:
        date_str = format_date()
    
    content = existing_content
    
    # Update Rating section
    if "Rating" in eod_data:
        rating = eod_data["Rating"]
        # Replace the meta-bind input with a static value
        content = re.sub(r'```meta-bind\nINPUT\[progressBar\(minValue\(1\), maxValue\(10\)\):Rating\]\n```', 
                         f'```meta-bind\nINPUT[progressBar(minValue(1), maxValue(10), value({rating})):Rating]\n```', 
                         content)
    
    # Update Summary section
    if "Summary" in eod_data:
        summary = eod_data["Summary"]
        content = content.replace('`INPUT[textArea():Summary]`', 
                                 f'{summary}')
    
    # Update Story section
    if "Story" in eod_data:
        story = eod_data["Story"]
        content = content.replace('`INPUT[textArea():Story]`', 
                                 f'{story}')
    
    # Update Accomplishments section
    if "Accomplishments" in eod_data:
        accomplishments = eod_data["Accomplishments"]
        # Find the Accomplishments section and add the content
        accomplishments_pattern = r'### Accomplishments\n\n%% What did I get done today\? %%\n\n```tasks'
        accomplishments_replacement = f'### Accomplishments\n\n%% What did I get done today? %%\n\n{accomplishments}\n\n```tasks'
        content = re.sub(accomplishments_pattern, accomplishments_replacement, content)
    
    # Update Obstacles section
    if "Obstacles" in eod_data:
        obstacles = eod_data["Obstacles"]
        obstacles_pattern = r'### Obstacles\n%% What was an obstacle I faced, how did I deal with it, and what can I learn from for the future\? %%'
        obstacles_replacement = f'### Obstacles\n%% What was an obstacle I faced, how did I deal with it, and what can I learn from for the future? %%\n\n{obstacles}'
        content = re.sub(obstacles_pattern, obstacles_replacement, content)
    
    # Update Energies section
    if "What did you do to re-energize? How did it go?" in eod_data:
        reenergize = eod_data["What did you do to re-energize? How did it go?"]
        content = content.replace("**What did I do to re-energize? How did it go?**\n\n- ", 
                                 f"**What did I do to re-energize? How did it go?**\n\n- {reenergize}")
    
    # Update energy ratings
    energy_fields = ["Physical", "Mental", "Emotional", "Spiritual"]
    for field in energy_fields:
        if field in eod_data:
            rating = eod_data[field]
            pattern = f'```meta-bind\nINPUT\\[progressBar\\(minValue\\(1\\), maxValue\\(10\\)\\):{field}\\]\n```'
            replacement = f'```meta-bind\nINPUT[progressBar(minValue(1), maxValue(10), value({rating})):{field}]\n```'
            content = re.sub(pattern, replacement, content)
    
    # Update Improvements section
    if "What can I do tomorrow to be 1% better?" in eod_data:
        improvements = eod_data["What can I do tomorrow to be 1% better?"]
        improvements_pattern = r'### Improvements\n%% What can I do tomorrow to be 1% better\? %%'
        improvements_replacement = f'### Improvements\n%% What can I do tomorrow to be 1% better? %%\n\n{improvements}'
        content = re.sub(improvements_pattern, improvements_replacement, content)
    
    return content

def file_exists(file_path):
    """
    Checks if a file exists.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if the file exists, False otherwise
    """
    return os.path.isfile(file_path)

def read_file_content(file_path):
    """
    Reads the content of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: The file content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_file_content(file_path, content):
    """
    Writes content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False
