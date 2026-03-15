from core.tools import tool_file
import os


web_tool = """ TODO make web_serch() """

class ResearchService:
    def __init__(self):
        self.web_tool = web_tool

    def prepare_topic(self, term: str) -> dict:
        # 1. Check if JSON exists
        file_path = f"core/data/topic_files/main_topic.json"
        videos = tool_file.get_youtube_videos(term, max_results=2)
        overview = tool_file.summarize_topic(term)
        subtopics = tool_file.generate_subtopics(term)
        links = tool_file.web_search(term)
        
        # Save JSON
        data = {
            "overview": overview,
            "videos": videos,
            "subtopics": subtopics,
            "links": links,
        }
        tool_file.save_json(file_path, data)
        return data


    def prepare_subtopic(self, term: str) -> dict:
        file_path = f"core/data/topic_files/subtopics/{term}.json"
        if os.path.exists(file_path):
            return tool_file.load_topic_data(file_path)
        
        if os.path.exists("core/data/topic_files/main_topic.json"):
            result = tool_file.load_topic_data("core/data/topic_files/main_topic.json")
            subtopics = result["subtopics"]

        videos = tool_file.get_youtube_videos(term, max_results=2)
        overview = tool_file.summarize_topic(term)
        subtopics = subtopics
        links = tool_file.web_search(term)

        # Save JSON
        data = {
            "overview": overview,
            "videos": videos,
            "subtopics": subtopics,
            "links": links,
        }
        tool_file.save_json(file_path, data)
        return data
