from flask_restful import Resource
from flask_jwt_extended import jwt_required
from slugify import slugify

from zou.app.services import (
    entities_service,
    files_service,
    names_service,
    playlists_service,
    projects_service,
    user_service,
    tasks_service,
)

import re
from .xml_generator import create_xml_timeline
from zou.app.utils import xml_utils

class PlaylistXmlExport(Resource):
    @jwt_required()
    def get(self, playlist_id):

        user_service.block_access_to_vendor()
        playlist = playlists_service.get_playlist(playlist_id)
        user_service.check_playlist_access(playlist, supervisor_access=True)
        project = projects_service.get_project(playlist["project_id"])
        
        task_ids = []
        for shot in playlist["shots"]:
            preview_file = files_service.get_preview_file(shot["preview_file_id"])
            task_ids.append(preview_file["task_id"])
        self.task_comment_map = tasks_service.get_last_comment_map(task_ids)

        playlist_name = playlist["name"]
        project_fps = project["fps"]
        tracks = []
        for shot in playlist["shots"]:
            tracks.append(self.build_track(shot))

        xml_content = create_xml_timeline(playlist_name, project_fps, tracks)
        return xml_utils.build_xml_response(xml_content, slugify(playlist_name))
        
    
    def build_track(self, shot):
        entity = entities_service.get_entity(shot["entity_id"])
        name, _ = names_service.get_full_entity_name(shot["entity_id"])
        duration = entity["nb_frames"] if entity["nb_frames"] else 24

        if entity["data"]:
            width, height = entity["data"]["resolution"].split("x")
        else:
            width, height = 1920, 1080

        comment = tasks_service.get_comment_by_preview_file_id(shot["preview_file_id"])
        shot_path = re.findall(r"\`(.*?)\`", comment["text"])[0]
        
        return {
            "name": name,
            "duration": duration,
            "width": width,
            "height": height,
            "pathurl": shot_path.replace('\\', '/')
        }
