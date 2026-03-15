from core.tools import tool_file
import os


web_tool = """ TODO make web_serch() """

class ResearchService:
    def __init__(self):
        self.web_tool = web_tool

    def prepare_topic(self, term: str) -> dict:
        # 1. Check if JSON exists
        file_path = f"core/data/topic_files/main_topic.json"
        if os.path.exists(file_path):
            return tool_file.load_topic_data(file_path)
        
        videos = tool_file.get_youtube_videos(term, max_results=2)
        overview = tool_file.summarize_topic(term)
        subtopics = tool_file.generate_subtopics(term)
        links = tool_file.web_search(term)
        

        # 5. Save JSON
        data = {
            "overview": overview,
            "videos": videos,
            "subtopics": subtopics,
            "links": links,
        }
        tool_file.save_json(file_path, data)
        return data


    def prepare_subtopic(self, term: str) -> dict:
        if self._exists(term):
            return self._load(term)

        videos = self.youtube_tool.search(term, top_k=2)
        links = self.web_tool.search(term, top_k=5)
        overview = self.chat_service.summarize_topic(term)

        data = {
            "overview": overview,
            "videos": videos,
            "links": links
        }
        self._save(term, data)
        return data
