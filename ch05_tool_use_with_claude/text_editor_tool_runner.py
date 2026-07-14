# Process TextEditorTool Call Requests

import json

from text_editor_tool import TextEditorTool


class TextEditorToolRunner:

    def __init__(self):
        self.text_editor_tool = TextEditorTool()


    # Run a single tool
    def run_tool(self, tool_name, tool_input):
        if tool_name == "str_replace_based_edit_tool":
            command = tool_input["command"]
            
            if command == "view":
                return self.text_editor_tool.view(
                    tool_input["path"], tool_input.get("view_range")
                )
            elif command == "str_replace":
                return self.text_editor_tool.str_replace(
                    tool_input["path"], tool_input["old_str"], tool_input["new_str"]
                )
            elif command == "create":
                return self.text_editor_tool.create(tool_input["path"], tool_input["file_text"])
            elif command == "insert":
                return self.text_editor_tool.insert(
                    tool_input["path"],
                    tool_input["insert_line"],
                    tool_input["new_str"],
                )
            elif command == "undo_edit":
                return self.text_editor_tool.undo_edit(tool_input["path"])
            else:
                raise Exception(f"Unknown text editor command: {command}")
        else:
            raise Exception(f"Unknown tool name: {tool_name}")
    

    # Run tools
    def run_tools(self, message):
        tool_requests = [block for block in message.content if block.type == "tool_use"]
        tool_result_blocks = []
    
        for tool_request in tool_requests:
            try:
                tool_output = self.run_tool(tool_request.name, tool_request.input)
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": json.dumps(tool_output),
                    "is_error": False,
                }
            except Exception as e:
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": f"Error: {e}",
                    "is_error": True,
                }
    
            tool_result_blocks.append(tool_result_block)
    
        return tool_result_blocks
