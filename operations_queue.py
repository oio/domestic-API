"""
Resource-based Command Queue System for Roby Bot

This module implements a resource-based command queue system for managing sequential execution
of commands that use the same underlying resources (LLM or image generation).
"""

import asyncio
import logging
from typing import Dict, List, Callable, Any, Tuple, Literal

logger = logging.getLogger(__name__)

# Define resource types
ResourceType = Literal["llm", "image"]

class ResourceQueue:
	"""
	Manages a queue of commands for a specific resource type.
	
	This class handles the queuing of commands that need to be executed one after
	another for a particular resource type (LLM or image generation).
	"""
	
	def __init__(self):
		"""Initialize the resource queues."""
		# One queue per resource type
		self.queues: Dict[ResourceType, asyncio.Queue] = {
			"llm": asyncio.Queue(),
			"image": asyncio.Queue()
		}
		
		# Keep track of the processing tasks
		self.tasks: Dict[ResourceType, asyncio.Task] = {}
		
		# Start the queue processors
		for resource_type in self.queues:
			self.tasks[resource_type] = asyncio.create_task(
				self._process_queue(resource_type)
			)
			logger.info(f"Started processor for {resource_type} queue")
	
	async def _process_queue(self, resource_type: ResourceType):
		"""
		Process commands in the resource queue one by one.
		
		Args:
			resource_type: The resource type queue to process
		"""
		queue = self.queues[resource_type]
		logger.info(f"Started queue processor for {resource_type} resource")
		
		while True:
			try:
				# Get the next command from the queue
				func, args, kwargs, future = await queue.get()
				
				try:
					# Execute the command
					logger.info(f"Processing {resource_type} command from queue")
					result = await func(*args, **kwargs)
					future.set_result(result)
				except Exception as e:
					logger.error(f"Error executing {resource_type} command: {e}")
					future.set_exception(e)
				finally:
					# Mark the task as done
					queue.task_done()
				
			except asyncio.CancelledError:
				logger.info(f"Queue processor for {resource_type} was cancelled")
				break
			except Exception as e:
				logger.error(f"Error in queue processor for {resource_type}: {e}")
				# Don't break the loop on error
	
	async def add_to_queue(self, resource_type: ResourceType, func: Callable, *args, **kwargs) -> Any:
		"""
		Add a command to the appropriate resource queue and await its execution.
		
		Args:
			resource_type: The resource type (llm or image)
			func: The async function to execute
			*args: Positional arguments for the function
			**kwargs: Keyword arguments for the function
			
		Returns:
			The result of the command execution
		"""
		# Get the queue for this resource type
		queue = self.queues[resource_type]
		
		# Create a future to get the result
		future = asyncio.Future()
		
		# Add the command to the queue
		await queue.put((func, args, kwargs, future))
		logger.info(f"Added {resource_type} command to queue (queue size: {queue.qsize()})")
		
		# Wait for the command to be processed
		return await future

# Create a global instance of the resource queue
resource_queue = ResourceQueue()

async def queue_llm(func: Callable, *args, **kwargs) -> Any:
	"""
	Queue an LLM-based function for execution.
	
	Args:
		func: The async function to execute
		*args: Positional arguments for the function
		**kwargs: Keyword arguments for the function
		
	Returns:
		The result of the function execution
	"""
	return await resource_queue.add_to_queue("llm", func, *args, **kwargs)

async def queue_image(func: Callable, *args, **kwargs) -> Any:
	"""
	Queue an image generation function for execution.
	
	Args:
		func: The async function to execute
		*args: Positional arguments for the function
		**kwargs: Keyword arguments for the function
		
	Returns:
		The result of the function execution
	"""
	return await resource_queue.add_to_queue("image", func, *args, **kwargs)

async def queue_multi_resource(funcs_with_resources: List[Tuple[ResourceType, Callable, List, Dict]]) -> List[Any]:
	"""
	Queue multiple resource-dependent functions in sequence.
	
	This function is useful for commands like agents that need to use both LLM and image generation.
	The functions will be executed in the order provided, waiting for each to complete before starting the next.
	
	Args:
		funcs_with_resources: List of tuples containing (resource_type, func, args, kwargs)
		
	Returns:
		List of results from each function execution
	"""
	results = []
	
	for resource_type, func, args, kwargs in funcs_with_resources:
		result = await resource_queue.add_to_queue(resource_type, func, *args, **kwargs)
		results.append(result)
	
	return results