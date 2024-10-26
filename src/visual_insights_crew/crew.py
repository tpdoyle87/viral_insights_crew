from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileWriterTool

@CrewBase
class VisualInsightsCrewCrew:
    """VisualInsightsCrew crew"""
    def __init__(self, inputs):
        self.inputs = inputs

    @agent
    def trending_video_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_video_analyst'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def social_media_investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_investigator'],
            tools=[SerperDevTool()],
            max_iter=3,
            verbose=False
        )

    @agent
    def exploratory_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['exploratory_specialist'],
            tools=[SerperDevTool()],
            max_iter=3,
            verbose=False
        )

    @agent
    def content_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_marketing_strategist'],
            tools=[SerperDevTool()],
            max_iter=3,
            verbose=False
        )

    @agent
    def niche_content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['niche_content_writer'],
            tools=[SerperDevTool()],
            verbose=False
        )

    @agent
    def trend_action_report_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_action_report_analyst'],
            tools=[SerperDevTool()],
            verbose=False
        )

    @agent
    def trend_action_tweet_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_action_tweet_analyst'],
            tools=[SerperDevTool()],
            verbose=False
        )

    @task
    def trending_video_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['trending_video_analysis'],
            output_file=f"tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/current_trends_analysis.txt"
        )

    @task
    def social_media_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_research_task'],
            output_file=f"tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/social_media_insights.txt"
        )

    @task
    def exploratory_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['exploratory_agent_task'],
            output_file=f"tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/market_insights.txt"
        )

    @task
    def content_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['content_marketing_strategy'],
            output_file=f'tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/marketing_strategy.txt'
        )

    @task
    def niche_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['niche_content_creation_task'],
            output_file=f'tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/niche_content_samples.txt'
        )

    @task
    def trend_action_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_action_report_task'],
            output_file=f'tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/trend_report.txt'
        )

    @task
    def trend_action_tweet_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_action_tweet_task'],
            output_file=f'tmp/{self.inputs['email']}_{self.inputs['niche']}_{self.inputs['platform']}/trend_tweet.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VisualInsightsCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
