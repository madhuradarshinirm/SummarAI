from google.adk import Agent

root_agent = Agent(
    name="simple_summarizer",
    model="gemini-2.0-flash",
    description="Summarizes text",
    instruction="""
    You are a helpful assistant.
    Summarize the user's text clearly and briefly.
    """
)