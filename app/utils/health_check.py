from fastapi import HTTPException
import shutil

def check_required_tools(tools: list[str]) -> bool:
    """
    Check if the required tools are installed on the system.

    Args:
        tools (list[str]): List of tool names to check.

    Returns:
        bool: True if all tools are installed.

    Raises:
        HTTPException: If any of the tools are not found.
    """
    for tool in tools:
        if shutil.which(tool) is None:
            raise HTTPException(
                status_code=500,
                detail=f"{tool} is not installed. Please install it to use this service.",
            )
        


    
    
    return True
