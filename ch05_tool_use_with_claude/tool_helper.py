import json

from anthropic.types import ToolParam
from datetime import datetime, timedelta

class ToolHelper:

    def __init__(self):
        pass

    
    # Tool Function
    # Run a batch of tools
    def run_batch(self, invocations=[]):
        batch_output = []

        for invocation in invocations:
            name = invocation["name"]
            args = json.load(invocation["arguments"])
            
            tool_output = self.run_tool(name, args)

            batch_output.append({"tool_name": name, "output": tool_output})
        
        return batch_output

    batch_tool_schema = ToolParam({
        "name": "batch_tool",
        "description": "Invoke multiple other tool calls simultaneously",
        "input_schema": {
            "type": "object",
            "properties": {
                "invocations": {
                    "type": "array",
                    "description": "The tool calls to invoke",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the tool to invoke",
                            },
                            "arguments": {
                                "type": "string",
                                "description": "The arguments to the tool, encoded as a JSON string",
                            },
                        },
                        "required": ["name", "arguments"],
                    },
                }
            },
            "required": ["invocations"],
        },
    })
    

    # Run a single tool
    def run_tool(self, tool_name, tool_input):
        if tool_name == "get_current_datetime":
            return self.get_current_datetime(**tool_input)
        elif tool_name == "add_duration_to_datetime":
            return self.add_duration_to_datetime(**tool_input)
        elif tool_name == "set_reminder":
            return self.set_reminder(**tool_input)
        elif tool_name == "batch_tool":
            return self.run_batch(**tool_input)
        

    # Run all the tools in the message and return tool result blocks
    def run_tools(self, message):
        tool_requests = [
            block for block in message.content if block.type == "tool_use"
        ]

        tool_result_blocks = []

        for tool_request in tool_requests:
            try:
                tool_output = self.run_tool(tool_request.name, tool_request.input)
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": json.dumps(tool_output),
                    "is_error": False
                }
            except Exception as e:
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": f"Error: {e}",
                    "is_error": True
                }

            tool_result_blocks.append(tool_result_block)

        return tool_result_blocks
                

    # Tool Function
    # Get formatted current datetime
    def get_current_datetime(self, date_format="%Y-%m-%d %H:%M:%S"):
        if not date_format:
            raise ValueError("date_format cannot be empty")
        return datetime.now().strftime(date_format)    
    
    get_current_datetime_schema = ToolParam({
        "name": "get_current_datetime",
        "description": "Returns the current date and time formatted according to the specified format",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                    "default": "%Y-%m-%d %H:%M:%S"
                }
            },
            "required": []
        }
    })  
    

    # Tool Function
    # Add duration to a given datetime
    def add_duration_to_datetime(self, datetime_str, duration=0, unit="days", input_format="%Y-%m-%d"):
        date = datetime.strptime(datetime_str, input_format)
    
        if unit == "seconds":
            new_date = date + timedelta(seconds=duration)
        elif unit == "minutes":
            new_date = date + timedelta(minutes=duration)
        elif unit == "hours":
            new_date = date + timedelta(hours=duration)
        elif unit == "days":
            new_date = date + timedelta(days=duration)
        elif unit == "weeks":
            new_date = date + timedelta(weeks=duration)
        elif unit == "months":
            month = date.month + duration
            year = date.year + month // 12
            month = month % 12
            if month == 0:
                month = 12
                year -= 1
            day = min(
                date.day,
                [
                    31,
                    29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                    31,
                    30,
                    31,
                    30,
                    31,
                    31,
                    30,
                    31,
                    30,
                    31,
                ][month - 1],
            )
            new_date = date.replace(year=year, month=month, day=day)
        elif unit == "years":
            new_date = date.replace(year=date.year + duration)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")
    
        return new_date.strftime("%A, %B %d, %Y %I:%M:%S %p")

    add_duration_to_datetime_schema = ToolParam({
        "name": "add_duration_to_datetime",
        "description": "Adds a specified duration to a datetime string and returns the resulting datetime in a detailed format. This tool converts an input datetime string to a Python datetime object, adds the specified duration in the requested unit, and returns a formatted string of the resulting datetime. It handles various time units including seconds, minutes, hours, days, weeks, months, and years, with special handling for month and year calculations to account for varying month lengths and leap years. The output is always returned in a detailed format that includes the day of the week, month name, day, year, and time with AM/PM indicator (e.g., 'Thursday, April 03, 2025 10:30:00 AM').",
        "input_schema": {
            "type": "object",
            "properties": {
                "datetime_str": {
                    "type": "string",
                    "description": "The input datetime string to which the duration will be added. This should be formatted according to the input_format parameter.",
                },
                "duration": {
                    "type": "number",
                    "description": "The amount of time to add to the datetime. Can be positive (for future dates) or negative (for past dates). Defaults to 0.",
                },
                "unit": {
                    "type": "string",
                    "description": "The unit of time for the duration. Must be one of: 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'. Defaults to 'days'.",
                },
                "input_format": {
                    "type": "string",
                    "description": "The format string for parsing the input datetime_str, using Python's strptime format codes. For example, '%Y-%m-%d' for ISO format dates like '2025-04-03'. Defaults to '%Y-%m-%d'.",
                },
            },
            "required": ["datetime_str"],
        },
    })
    

    # Tool Function
    # Set a reminder
    def set_reminder(self, content, timestamp):
        print(f"----\nSetting the following reminder for {timestamp}:\n{content}\n----")
    
    set_reminder_schema = ToolParam({
        "name": "set_reminder",
        "description": "Creates a timed reminder that will notify the user at the specified time with the provided content. This tool schedules a notification to be delivered to the user at the exact timestamp provided. It should be used when a user wants to be reminded about something specific at a future point in time. The reminder system will store the content and timestamp, then trigger a notification through the user's preferred notification channels (mobile alerts, email, etc.) when the specified time arrives. Reminders are persisted even if the application is closed or the device is restarted. Users can rely on this function for important time-sensitive notifications such as meetings, tasks, medication schedules, or any other time-bound activities.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The message text that will be displayed in the reminder notification. This should contain the specific information the user wants to be reminded about, such as 'Take medication', 'Join video call with team', or 'Pay utility bills'.",
                },
                "timestamp": {
                    "type": "string",
                    "description": "The exact date and time when the reminder should be triggered, formatted as an ISO 8601 timestamp (YYYY-MM-DDTHH:MM:SS) or a Unix timestamp. The system handles all timezone processing internally, ensuring reminders are triggered at the correct time regardless of where the user is located. Users can simply specify the desired time without worrying about timezone configurations.",
                },
            },
            "required": ["content", "timestamp"],
        },
    })


    #---------------------------------#

    article_summary_schema = ToolParam({
        "name": "article_summary",
        "description": "Creates a summary of an article with its key insights.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the article being summarized",
                },
                "author": {
                    "type": "string",
                    "description": "The name of the author who wrote the article",
                },
                "key_insights": {
                    "type": "string",
                    "description": "Key insights extracted from the article",
                },
            },
            "required": ["title", "author", "key_insights"],
        },
    })
