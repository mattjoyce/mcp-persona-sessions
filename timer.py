"""
Timer functionality for MCP server.

Provides tools for creating, checking, and stopping timers during interviews.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


@dataclass
class Timer:
    """Timer class for tracking elapsed time and progress."""
    name: str
    start_time: datetime
    target_duration: Optional[timedelta] = None

    def elapsed(self) -> timedelta:
        """Get elapsed time since timer started."""
        return datetime.now() - self.start_time
        
    def remaining(self) -> Optional[timedelta]:
        """Get remaining time if target duration was set."""
        if self.target_duration is None:
            return None
        return self.target_duration - self.elapsed()
    
    def progress_percentage(self) -> Optional[float]:
        """Get progress as percentage if target duration was set."""
        if self.target_duration is None:
            return None
        elapsed_seconds = self.elapsed().total_seconds()
        target_seconds = self.target_duration.total_seconds()
        return min(100, (elapsed_seconds / target_seconds) * 100)
    
    def progress_description(self) -> str:
        """Get a descriptive text about the progress."""
        if self.target_duration is None:
            return f"Running for {self.pretty_elapsed()}"
        
        percentage = self.progress_percentage()
        if percentage <= 10:
            return "Just getting started"
        elif percentage <= 30:
            return "In the early stages"
        elif percentage <= 50:
            return "About halfway through"
        elif percentage <= 75:
            return "Well past halfway"
        elif percentage <= 90:
            return "Nearing the end"
        else:
            return "Time to wrap up"
    
    def pretty_elapsed(self) -> str:
        """Get a formatted string of elapsed time."""
        delta = self.elapsed()
        minutes, seconds = divmod(delta.total_seconds(), 60)
        return f"{int(minutes)}m {int(seconds)}s"
    
    def pretty_remaining(self) -> Optional[str]:
        """Get a formatted string of remaining time."""
        if self.target_duration is None:
            return None
        
        delta = self.remaining()
        if delta.total_seconds() < 0:
            return "Time is up"
        
        minutes, seconds = divmod(delta.total_seconds(), 60)
        return f"{int(minutes)}m {int(seconds)}s"


class TimerManager:
    """Manager class for multiple timers."""
    
    def __init__(self):
        """Initialize with an empty timer dictionary."""
        self.timers: Dict[str, Timer] = {}

    def start(self, name: str = "default", minutes: int = 0) -> str:
        """
        Start a new timer.
        
        Args:
            name: Name of the timer
            minutes: Target duration in minutes (0 for no target)
            
        Returns:
            Status message
        """
        target_duration = timedelta(minutes=minutes) if minutes > 0 else None
        self.timers[name] = Timer(
            name=name, 
            start_time=datetime.now(), 
            target_duration=target_duration
        )
        
        if target_duration:
            return f"Timer '{name}' started with target duration of {minutes} minutes."
        else:
            return f"Timer '{name}' started without a target duration."

    def check(self, name: str = "default") -> str:
        """
        Check the status of a timer.
        
        Args:
            name: Name of the timer to check
            
        Returns:
            Status message with timer information
        """
        timer = self.timers.get(name)
        if not timer:
            return f"❌ No timer named '{name}' found."
            
        progress = timer.progress_description()
        elapsed = timer.pretty_elapsed()
        
        if timer.target_duration:
            remaining = timer.pretty_remaining()
            percentage = int(timer.progress_percentage())
            return f"Timer '{name}': {progress} ({elapsed} elapsed, {remaining} remaining, {percentage}% complete)"
        else:
            return f"Timer '{name}' has been running for {elapsed}."

    def stop(self, name: str = "default") -> str:
        """
        Stop a timer and remove it from the manager.
        
        Args:
            name: Name of the timer to stop
            
        Returns:
            Final status message
        """
        timer = self.timers.pop(name, None)
        if not timer:
            return f"❌ No timer named '{name}' to stop."
            
        if timer.target_duration:
            percentage = int(timer.progress_percentage())
            return f"Timer '{name}' stopped after {timer.pretty_elapsed()} ({percentage}% of target duration)"
        else:
            return f"Timer '{name}' stopped after {timer.pretty_elapsed()}."