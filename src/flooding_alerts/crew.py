from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentations for more information on how to use them
from crewai_tools import ScrapeWebsiteTool

scrape_tool = ScrapeWebsiteTool(
    website_url="https://check-for-flooding.service.gov.uk/alerts-and-warnings"
)

@CrewBase
class CrewaiFloodingAlertsAndWarningsCrew():
	"""CrewaiFloodingAlertsAndWarnings crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[scrape_tool],
			verbose=True
		)

	@agent
	def data_formatter(self) -> Agent:
		return Agent(
			config=self.agents_config['data_formatter'],
			verbose=True
		)

	@agent
	def data_filterer(self) -> Agent:
		return Agent(
			config=self.agents_config['data_filterer'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def data_formatting_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_formatting_task'],
			agent=self.data_formatter(),
			output_file='data.json',
			context=[self.research_task()]
		)
	
	@task
	def data_filter_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_filter_task'],
			agent=self.data_filterer(),
			output_file='filtered-data.json',
			context=[self.data_formatting_task()]
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiFloodingAlertsAndWarnings crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)